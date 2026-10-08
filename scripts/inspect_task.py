#!/usr/bin/env python3
"""Read-only task/asset inspection. Does not save, authorize, or generate images."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


class RecordError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def require(condition, message):
    if not condition:
        raise RecordError("INVALID_RECORD", message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(record):
    require(isinstance(record, dict), "record must be an object")
    require(type(record.get("schema_version")) is int and record["schema_version"] == 1,
            "unsupported schema_version")
    for key in ("task_id", "request", "intent"):
        require(text(record.get(key)), key + " is required")
    require(record["intent"] in {"browse", "plan", "generate", "edit", "restore", "export", "audit"},
            "unknown intent")
    for key in ("authorization", "references", "questions", "assets", "outputs"):
        require(isinstance(record.get(key), dict), key + " must be an object")
    auth = record["authorization"]
    require(auth.get("action") in {"none", "generate", "edit"}, "invalid action")
    require(text(auth.get("source")), "authorization source is required")
    require(type(auth.get("limit")) is int and auth["limit"] >= 0, "limit must be a nonnegative integer")
    require(type(auth.get("paused")) is bool, "paused must be boolean")
    assets, outputs = record["assets"], record["outputs"]
    for aid, asset in assets.items():
        require(text(aid) and isinstance(asset, dict), "invalid asset")
        require(text(asset.get("role")) and text(asset.get("source")), "asset role/source required: " + aid)
        require(asset.get("availability") in {"available", "missing", "thumbnail_only"}, "invalid availability: " + aid)
        require(asset.get("path") is None or text(asset["path"]), "invalid path: " + aid)
        sha = asset.get("sha256")
        require(sha is None or (isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha)), "invalid digest: " + aid)
        if asset["availability"] == "available":
            require(text(asset.get("path")) and sha is not None, "available asset needs path and digest: " + aid)
    refs = record["references"]
    require(refs.get("operation") in {"original", "replicate", "translate"}, "invalid photography operation")
    require(refs.get("identity") is None or refs["identity"] in assets, "unknown identity asset")
    require(isinstance(refs.get("photography"), list), "photography must be a list")
    require(all(isinstance(a, str) and a in assets for a in refs["photography"]), "unknown photography asset")
    for qid, question in record["questions"].items():
        require(text(qid) and isinstance(question, dict), "invalid question")
        require(":" not in qid, "question id cannot contain ':'")
        options = question.get("options")
        require(isinstance(options, dict) and len(options) > 0, "question needs options: " + qid)
        require(all(text(k) and (v is None or (isinstance(v, str) and v in assets)) for k, v in options.items()),
                "question refers to unknown asset: " + qid)
    pending = record.get("pending_question_id")
    require(pending is None or (isinstance(pending, str) and pending in record["questions"]), "unknown pending question")
    for oid, output in outputs.items():
        require(text(oid) and isinstance(output, dict), "invalid output")
        require(isinstance(output.get("asset_id"), str) and output["asset_id"] in assets, "unknown output asset: " + oid)
        parent = output.get("parent_id")
        require(parent is None or (isinstance(parent, str) and parent in outputs), "unknown parent: " + oid)
        require(isinstance(output.get("accepted_scope"), list) and all(text(x) for x in output["accepted_scope"]),
                "accepted_scope must be a list: " + oid)
        seen, cursor = set(), oid
        while cursor is not None:
            require(cursor not in seen, "parent cycle: " + oid)
            seen.add(cursor)
            node = outputs.get(cursor)
            require(isinstance(node, dict), "invalid parent: " + oid)
            cursor = node.get("parent_id")
            require(cursor is None or (isinstance(cursor, str) and cursor in outputs), "unknown parent: " + oid)
    current = record.get("current_output_id")
    require(current is None or (isinstance(current, str) and current in outputs), "unknown current output")
    operations = record.get("operations")
    require(isinstance(operations, list), "operations must be a list")
    ids = set()
    for op in operations:
        require(isinstance(op, dict) and text(op.get("id")), "invalid operation")
        require(op["id"] not in ids, "duplicate operation id")
        ids.add(op["id"])
        require(op.get("kind") in {"generate", "edit"}, "invalid operation kind")
        require(op.get("state") in {"prepared", "submitted", "returned", "unknown", "failed", "not_submitted"},
                "invalid submission state")
        inputs = op.get("input_ids")
        require(isinstance(inputs, list) and all(isinstance(a, str) and a in assets for a in inputs), "unknown operation input")
        base, out = op.get("base_output_id"), op.get("output_id")
        require(base is None or (isinstance(base, str) and base in outputs), "unknown edit baseline")
        require(out is None or (isinstance(out, str) and out in outputs), "unknown operation output")
        if op["kind"] == "edit":
            require(base is not None and outputs[base]["asset_id"] in inputs, "edit must include baseline asset")
            if out is not None:
                require(outputs[out].get("parent_id") == base, "edit parent must match baseline")
        if op["state"] == "returned":
            require(out is not None, "returned operation needs output")
        if op["state"] == "not_submitted":
            require(out is None, "unsubmitted operation cannot have a returned output")
            require(text(op.get("cancellation_evidence")),
                    "unsubmitted cancellation needs recorded evidence")
    return record


def resolve_asset(record, task_path, aid):
    if aid not in record["assets"]:
        raise RecordError("ASSET_UNKNOWN", "asset id is not recorded")
    asset = record["assets"][aid]
    if asset["availability"] != "available":
        raise RecordError("ASSET_NOT_READY", "asset is missing or thumbnail-only")
    raw = asset["path"]
    image_suffixes = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".heic", ".tif", ".tiff", ".bmp"}
    if "://" in raw or Path(raw).suffix.lower() not in image_suffixes:
        raise RecordError("ASSET_PATH_INVALID", "expected a local image file")
    try:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = task_path.parent / path
        path = path.resolve()
    except RuntimeError as exc:
        raise RecordError("ASSET_PATH_INVALID", "local image path could not be resolved") from exc
    if path.suffix.lower() not in image_suffixes:
        raise RecordError("ASSET_PATH_INVALID", "resolved target must be a local image file")
    if not path.is_file():
        raise RecordError("ASSET_MISSING", "recorded image is not available; no substitute selected")
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1048576), b""):
            hasher.update(chunk)
    actual = hasher.hexdigest()
    if actual != asset["sha256"]:
        raise RecordError("ASSET_CHANGED", "image bytes differ from the recorded version")
    return {"asset_id": aid, "path": str(path), "sha256": actual, "role": asset["role"],
            "scope": "asset_bytes_only", "permission_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--asset", metavar="ASSET_ID")
    selector.add_argument("--candidate", metavar="QUESTION_ID:OPTION")
    selector.add_argument("--output", metavar="OUTPUT_ID")
    selector.add_argument("--parent", metavar="OUTPUT_ID")
    args = parser.parse_args()
    try:
        for selected in (args.asset, args.candidate, args.output, args.parent):
            require(selected is None or text(selected), "selector id cannot be empty")
        task = args.task.resolve()
        record = validate(json.loads(task.read_text(encoding="utf-8"), object_pairs_hook=unique_object))
        occupied = sum(op["state"] != "not_submitted" for op in record["operations"])
        limit = record["authorization"]["limit"]
        budget_status = "over_limit" if occupied > limit else (
            "exhausted" if occupied == limit else "within_limit")
        result = {"scope": "record_structure_only", "task_id": record["task_id"],
                  "reserved_or_submitted": occupied,
                  "remaining": max(0, limit - occupied),
                  "budget_status": budget_status, "over_by": max(0, occupied - limit),
                  "permission_verified": False}
        if args.candidate is not None:
            qid, separator, choice = args.candidate.partition(":")
            if not separator or qid != record.get("pending_question_id"):
                raise RecordError("STALE_QUESTION", "candidate must name the current pending question")
            options = record["questions"][qid]["options"]
            if choice not in options:
                raise RecordError("OPTION_UNKNOWN", "option is not in the recorded snapshot")
            if options[choice] is None:
                raise RecordError("ASSET_NOT_READY", "text option has no image asset")
            result.update(resolve_asset(record, task, options[choice]))
        elif args.output is not None or args.parent is not None:
            oid = args.output if args.output is not None else args.parent
            if oid not in record["outputs"]:
                raise RecordError("OUTPUT_UNKNOWN", "output id is not recorded")
            if args.parent is not None:
                oid = record["outputs"][oid].get("parent_id")
                if oid is None:
                    raise RecordError("NO_PARENT", "output has no recorded parent")
            result.update(resolve_asset(record, task, record["outputs"][oid]["asset_id"]))
            result["output_id"] = oid
        elif args.asset is not None:
            result.update(resolve_asset(record, task, args.asset))
        print(json.dumps({"ok": True, **result}, ensure_ascii=False))
        return 0
    except RecordError as exc:
        print(json.dumps({"ok": False, "code": exc.code, "message": str(exc)}, ensure_ascii=False))
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"ok": False, "code": "INVALID_RECORD", "message": type(exc).__name__}, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    sys.exit(main())
