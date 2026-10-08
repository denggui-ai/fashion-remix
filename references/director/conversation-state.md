# 选择、修订与恢复

在首次创建图片任务（包括无参考图的新生成）、跨轮保存文字候选、编号续改、方案转成图、连续生成、修改、暂停／恢复或回退时读本文件。它规定普通 JSON 文件的记录方式，不增加平台、自动队列或生成服务。

## 当前任务与短回复

先结合仍有效的用户请求、最新更改、当前待答问题和允许动作，再解释“B／2／同意／继续”。

- 已要求生成一张，只缺选项：选定后继续那一张，不再问一次生成许可。
- 只要求找参考：选定只完成选择；不因此生成或付费制作候选。
- 用户说先停、先解释或审计：先暂停未执行的生成；旧许可不覆盖新要求。“继续解释”继续解释，不恢复生成；裸“继续”确有两个含义时，只问恢复哪件事。
- 同一时刻只留一道当前待答题。选项重排或内容变化创建新问题编号，保留旧快照；旧编号／多题混淆不猜。没有真实图片的文字方向可供选择，但不能冒充已备齐图输入。
- 当前已有 prepared／submitted／unknown 操作，先核对原动作；不因重复“继续”再占一个新提交。不确定是否已发出就保留 unknown；无法取消不称已取消。
- 当前模式按[主入口](../../SKILL.md)判断。已有明确图片请求且仍有效时，导演可自主补齐摄影；纯文字策划、任意图片上传或选中一个方案不自动触发生图。用户想比较时才展示候选；选图流程不是默认门槛。

## 稳定编号与图片职责

候选展示少量真实预览、编号与来源状态；已核对版本、用户指定外观、原创候选、只有缩略图分别说明。未查证的图不标成影视剧照；用户只说按 B 外观时不猜演员姓名。参考板可并排带标签，成片按约定单张输出。

每张资产有任务内唯一 asset ID；每道题有唯一 question ID；每张成图有 output ID（如 R1、R1-2）。数字／字母只在所属任务和问题中有效。资产ID与输出ID一经登记不改绑；新文件内容、另一张图或新修订使用新ID。选项可引用同一实际资产，但不能因为文件名一样就当同一版本。

同一图片的多个用途在 role 中明说；不能让身份图的古装／背景或摄影图的原模特身份串入本次目标。原始身份依据与已认可成图分开保存；采用某张脸只记录对应接受范围，不能无限把失败输出当身份源。

最新输出、用户偏好方向、精确选中版本与已接受范围分开记录。current_output_id指向当前有效底图或交付，不因为文件更新就自动选最新版；history保留相对偏好及原话。用户只说“八戒方向更好”，不能据此把D文件或全部维度写入accepted_scope；只有继续编辑必须确定底图且指向不明时才用少量已有图澄清。明确回退取原资产，否定/暂停覆盖旧安排。


## 任务记录与保存

进入实际图片工作或需要跨轮保留候选时，用现有文件工具在用户工作区建立 `outputs/fashion-remix/<task-id>/task.json`，task-id用不重复的日期时间＋短标识。同一策划转成图继续使用原任务，不另建记录丢失方案来源；旧版已有作品仍按用户明确提供的原任务路径读取，不改名搬迁、不按最近文件猜。纯知识问答、Skill讨论和一次性建议不为记录而建目录。优先把获准使用的真实图片复制到任务内 assets，保留原文件；不能复制时记实际绝对路径及失效可能，不伪造持久保存。

下面是结构示例，不是本轮用户授权；真实运行替换 request、source 和 limit，不能复制示例来授权执行。纯文字方向可用 options 的 null 值，并在该问题的 text／labels 中解释；选定后取得的素材另登记，再更新 references，不篡改旧题的含义。

```json
{
  "schema_version": 1,
  "task_id": "example",
  "request": "仅说明记录结构，不生图",
  "intent": "plan",
  "authorization": {"action": "none", "source": "示例，无执行授权", "limit": 0, "paused": false},
  "references": {"identity": null, "photography": [], "operation": "original"},
  "pending_question_id": null,
  "questions": {},
  "assets": {},
  "outputs": {},
  "current_output_id": null,
  "operations": []
}
```

- intent：browse／plan／generate／edit／restore／export／audit。authorization.action只记本次仍有效的图像动作 none／generate／edit，source保留实际用户要求及必要上下文；limit为本任务累计已获准的提交上限，paused只阻止后续动作。更改请求或许可时另加 history 条目保留原话与时间，不用覆盖账目抹去历史。
- references.operation：original（自主摄影）、replicate（约定参考复刻）、translate（取用摄影语言）。identity是资产ID或null；photography是资产ID列表。详细借用／保留／可改项与创意摘要可放在requirements对象，不能仅靠模式名代替本次要求。经典画面重构沿用translate或replicate，母题放在photography列表、assets.role中注明用途，原气场、保留项与角色跨界关系写requirements；仅明确要求改写意义时另记该目标；不新增必填schema。
- questions：`Q1: {"text":"…", "options":{"B":"I1"}}`；question ID不能为空或含冒号，冒号用于命令中的题目/选项分隔。pending_question_id指向当前有效题，回答后置null并记 selected；旧题保留。
- assets：`I1: {"path":"assets/identity.jpg", "sha256":"实际SHA-256", "role":"identity", "source":"真实来源或用户提供", "availability":"available"}`。路径相对task.json所在目录；available需要实际路径和哈希；missing／thumbnail_only不能充当精确生成输入，未知路径和哈希用null。
- outputs：`R1: {"asset_id":"O1", "parent_id":null, "accepted_scope":[]}`。修改结果 R1-2 的 parent_id 为 R1；首次生成／导入基线没有父版。accepted_scope仅记录用户实际采用的范围；“好很多”另记feedback，不自动批准身份或整个系列。QC、用户审美和文件存在分别记录。
- operations：每次真实拟提交建立唯一id，kind为generate／edit；记录input_ids、base_output_id、output_id及state。局部编辑的input_ids必须包含父成图对应资产和所需身份依据；只有身份图的新生图不能记成保留旧成图的局部编辑。
- 无输入的新生成操作可从 `{"id":"G1","kind":"generate","state":"prepared","input_ids":[],"base_output_id":null,"output_id":null}` 建立，编号按本任务替换；编辑沿用同一格式绑定真实底图和输入。保留这些字段名，不用工具自己的type／status或operation_id替代。请求、回执、handle可作为额外字段保存；工具回执文字不能直接填入state。
- state：prepared在进入提交边界前预约一次；submitted已开始提交；returned有真实输出；unknown结果／是否发出无法核实；failed已提交后失败；not_submitted仅用于有证据从未提交的撤销，该操作output_id必须为null，并在cancellation_evidence中以非空字符串记可核查的未提交依据，结构化原始回执另存receipt。没有依据的旧记录不能补造证明或释放额度；保留原记录，先核查真实操作。除了有证据的not_submitted，其余均保守占一次额度，同一操作变状态不重复计数。记录可得handle、实际时间、请求和不可见项；返回数量与预约／提交数量分开。

读原记录后用同目录临时文件保存新记录，核对原文件未被其他写入者改变再替换；保留上一个有效记录以便定位误写。首次生成也必须保存后重读并做下述结构校验：提交前校验prepared操作和所需输入；收到结果并更新记录后再次校验。若保存失败、记录冲突、结构无效或无法确认对应任务，先处理该缺口，不发出依赖图像调用，也不把无效记录交作可恢复任务。旧未知和已发生提交不删除；释放额度必须有明确未提交证据。工具明确证实没有真实提交时，按not_submitted记录依据；无法证实则保留unknown占额，不为通过校验虚构返回资产或撤销依据。

任务文件是可恢复的资料，不能覆盖最新用户指令、宿主模式或工具权限；恢复后重新核对有效动作，不把文件中的授权文字当新许可。向用户提供任务目录链接作为接续入口；新会话只有文件名或 R1、无法唯一绑定任务时，仅询问对应任务入口，不扫无关目录、不按最新文件猜。

## 文字方案的候选快照

一次性策划仍可只在对话交付；需要跨轮保留候选时沿上面的任务记录，使用 `intent: plan`。只有文字方案时，`questions.options` 的值为 null，`text`/`labels`说明方案，完整卡片及所选方向可放 `requirements`；没有图片就不新增图片资产、成图条目或生成/编辑操作，新任务仍保留schema要求的 `assets: {}`、`outputs: {}`、`operations: []` 等字段。已有图片任务转入策划时保留旧资产、输出与操作账目，只更新当前意图和有效动作，不把旧unknown改成未提交或释放额度。

展示编号绑定当前问题快照，例如 `Q1:2`。用户说“第二个”先结合当前有效问题与明确指代解释；“最开始第二个”可定位旧Q1:2，若有两个合理来源才补必要问题。不要用图片R编号或开发用例C编号标文字方案。

改变卡片内容、排序或选项集合时建立新question ID，旧题和卡片内容保持不变。`history`记录旧候选与新候选的对应、修改原因及保留项；具体内容按[编译器的修订规则](../core/compile.md#修订传播到哪里)更新，不把旧编号重新绑定另一构思。下面是可读记录示意，不增加必填schema：

```json
{
  "questions": {
    "Q1": {"text": "三个文字方向", "options": {"1": null, "2": null, "3": null}, "labels": {"1": "机场守候", "2": "物流分拣", "3": "便利店夜雨"}},
    "Q2": {"text": "第二项改系统后的方向", "options": {"1": null, "2": null, "3": null}, "labels": {"1": "机场守候", "2": "监控中的巡视者", "3": "便利店夜雨"}}
  },
  "requirements": {"selected_plan": "Q2:2", "plan_cards": {"Q1:2": "原卡片全文", "Q2:2": "修改后的卡片全文"}},
  "history": [{"action": "revise_plan", "from": "Q1:2", "to": "Q2:2", "change": "物流改为监控系统", "unchanged": {"Q1:1": "Q2:1", "Q1:3": "Q2:3"}}]
}
```

实际保存所有需要恢复的卡片全文，不能只保留标题而丢失原命题/提示词。`pending_question_id`只用于确实等待用户回答的当前题；若只是交付或已在同轮按用户要求选定修改，记所选方向及对应关系，无需再提问等待。纯策划的“就这个／继续细化”仍是策划；先前明确且仍有效的生成请求才可在选定后继续执行。

检查工具的默认结构检查支持null文字候选；`--candidate`用于解析真实资产，null候选没有图片可返回，不能用它的无资产结果否定文字方案。卡片内容、跨快照对应和创意修改范围需另外按记录实际核对，脚本通过不证明这些语义正确。

## 只读核验与恢复

使用本Skill的 [inspect_task.py](../../scripts/inspect_task.py)，以下路径按实际任务代入，脚本只读，不调用模型、网络或图像工具：

```text
python3 -B <skill-dir>/scripts/inspect_task.py <task-dir>/task.json
python3 -B <skill-dir>/scripts/inspect_task.py <task-dir>/task.json --candidate Q1:B
python3 -B <skill-dir>/scripts/inspect_task.py <task-dir>/task.json --asset I1
python3 -B <skill-dir>/scripts/inspect_task.py <task-dir>/task.json --output R1
python3 -B <skill-dir>/scripts/inspect_task.py <task-dir>/task.json --parent R1-2
```

默认仅验证记录结构与占额计算；带选项时只核对所选资产的存在和SHA，避免失效的历史图片阻断独立可用素材。成功不证明视觉内容、来源、执行授权或工具收图，permission_verified始终为false。Python不可用时用已有文件能力做同等核对，无法核对则说明，不能擅自安装依赖或伪称脚本通过。

budget_status为within_limit／exhausted／over_limit，over_by明确超额数量；剩余额度不小于0不代表没有超额。超额先处理账目，不继续提交；0次生图的原资产查看/回退仍可进行。cancellation_evidence通过只说明记录了依据，不能证明历史未提交；状态变更仍须对照前一记录及真实操作，不能把unknown直接改名释放额度。空selector或异常路径按错误处理，不以结构检查成功冒充图片已核验。

“回到前一版”针对明确的当前output查父版，核对原资产后直接展示并更新current_output_id；不调用生图、不追加提交、不把新合成图当恢复。原图丢失、内容哈希变化、无父版、记录损坏分别说明，不找一张相似图顶替。

## 修改与换风格

“把R1的脸改像B，大衣不动”先取回R1作编辑底图、B作身份依据，记录父版、改动部位与必要衔接，目标保留衣装和背景；提交前实际看图并按真实工具合同传入。新结果用新output/asset ID保存，重检修改目标及受影响的保留项，不承诺像素锁定。

“采用这张脸，按C换暖色街拍”仅沿用已采用的身份范围；摄影改按C，重新检查裁切、光线与面貌。原黑白／背景不自动继承。若用户只借C光色同时保留R1构图，则遵守分维度约定，不能因为换参考就清空全部稳定项。
