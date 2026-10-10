# fashion-remix 文件核对清单

根目录：`fashion-remix/`；共28个文件：原24个（19个策划包＋4份director参考＋1个恢复脚本）＋风格入口＋三份角色资料。
所有原文件保留；空目录占位文件0行，角色模板中的填写位是有意保留。行数含空行。

|文件路径|是否存在|行数|关键内容一句话|状态|
|---|---|---:|---|---|
|`fashion-remix/.gitignore`|是|4|忽略系统文件、缓存、日志与环境文件|已具备|
|`fashion-remix/CHECKLIST.md`|是|61|28文件、实际行数、验证范围和边界|已具备|
|`fashion-remix/LICENSE`|是|21|MIT许可全文及指定作者署名|已具备|
|`fashion-remix/README.md`|是|149|三模式与风格名用法、固定作者安装地址、工具依赖和旧版归档范围|已具备|
|`fashion-remix/SKILL.md`|是|189|三模式分流、风格模板路由、意图优先级、完成条件、3张拓扑（含风格入口节点）和10条元规则|已具备|
|`fashion-remix/agents/openai.yaml`|是|7|时尚重塑名称、fashion标签和三模式UI描述|已具备|
|`fashion-remix/assets/.gitkeep`|是|0|保留空素材目录|已具备|
|`fashion-remix/examples/demo-sha-seng.md`|是|125|三套方案、原提示词、Q1/Q2状态与编号续改|已具备|
|`fashion-remix/references/audiences/chinese-general.md`|是|40|受众假设、角色保留建议与提示词落实|已具备|
|`fashion-remix/references/characters/README.md`|是|42|添加角色方法、四人角色目录、定妆门与识别卡|已具备|
|`fashion-remix/references/characters/_template.md`|是|78|十字段、候选锚点、默认SABC空表、三层调用及识别卡填法|已具备|
|`fashion-remix/references/characters/sha-seng.md`|是|91|十字段、默认身份形貌层、识别卡（已定妆）、两套带范围分级、混淆与转译|已具备|
|`fashion-remix/references/characters/wu-kong.md`|是|75|悟空：默认86版造型线索的三层资料、分级、混淆与站内来源差异|已具备|
|`fashion-remix/references/characters/zhu-ba-jie.md`|是|82|八戒：定妆基线 R4-3（父版 R4）的三层资料、识别卡（含不借项）、分级与混淆|已具备|
|`fashion-remix/references/characters/tang-seng.md`|是|81|唐僧：定妆基线 R1 的三层资料、识别卡、分级与混淆|已具备|
|`fashion-remix/references/core/anchor-grading.md`|是|41|默认与本轮SABC、调整权限及冲突顺序|已具备|
|`fashion-remix/references/core/audit.md`|是|46|四视角反偏见审计与确定性说明|已具备|
|`fashion-remix/references/core/axes.md`|是|35|八轴、偏好排序、可选权重与六触发器|已具备|
|`fashion-remix/references/core/compile.md`|是|73|方案卡（含方向、风格、看图注意）、正面限定、提示词命名边界与同步修订|已具备|
|`fashion-remix/references/core/deconstruct.md`|是|32|十字段、沙僧／悟空对照与未知处理|已具备|
|`fashion-remix/references/core/systems.md`|是|51|26个关系入口与碰撞公式|已具备|
|`fashion-remix/references/director/conversation-state.md`|是|108|共享任务、文字快照、图片父版及真实资产恢复|已具备|
|`fashion-remix/references/director/creative-direction.md`|是|68|承接已选方案与风格模板、择一后的经典画面与多人摄影执行|已具备|
|`fashion-remix/references/director/input-and-qc.md`|是|99|输入职责、检查、授权次数及完整交付状态|已具备|
|`fashion-remix/references/director/photography-methods.md`|是|135|15类摄影关系及已定命题的摄影实现|已具备|
|`fashion-remix/references/styles/README.md`|是|219|六套模板（四首选两候选）、v2 验证状态、衣装模式、四人配置、拓展候选、定妆门与系列编排|已具备|
|`fashion-remix/scripts/inspect_task.py`|是|205|原样迁入的只读任务、资产与父版检查脚本|已具备|
|`fashion-remix/scripts/run-demo.sh`|是|100|离线示例与显式live策划；单次文字实测完成|已具备|

## 重点核对

- [x] 主入口包含三种模式；文字迭代、真实编辑、零生图回退分别处理。
- [x] 已选方案与点名风格模板优先；完全自由的图片任务由导演在风格模板与经典画面间择一并说明，不重写已选原创构思。
- [x] 策划定义统一采用core；摄影执行与恢复采用director，同一方案转成图继续同一任务。
- [x] 3张Mermaid和10条元规则保留；库外角色继续可用。
- [x] 风格名请求直接进入模板，不改选电影；经典画面请求不被模板劫持；四人资料按三层调用。
- [x] 相对引用与脚本深度已更新；全部本地链接须经交付核验。
- [x] README用户名为denggui-ai；MIT署名为denggui-ai (饭饭是条狗子)。
- [x] 原示例和恢复脚本均保留；开发验证证据另存，不随公开运行包分发；已验证范围见README。
- [x] 原图库与旧源8文件保留；旧安装7文件完整归档；历史v1.1.1仅发布24文件源码与标签，本轮未发布。

## 范围与旧要求处理

“已具备”只指文件包含相应用途内容，不等于旧清单逐字实现或所有行为验证通过；路径、结构、示例和原资产读取按实际核验报告，不将单次实测扩大为稳定成功、公众辨识或传播效果。
本清单对应基于v1.1.1的未公开发布修订；新增分级／偏好／状态、身份交接、显式live入口、风格入口与四人角色资料，本机部署以实际安装核验为准。原独立新会话检查2/3命中；同会话补测进入修改、父版正确且背景达成，主体细节有重绘，保留IMAGES_PARTIAL。详细范围见README。
52张图库保留项目原位，不属于本包；旧安装已归档至隐藏父目录，本包不附带私人素材或开发日志。

- 原18文件清单中的内容缺项已补充：带范围默认分级、SABC空表、悟空对照、受众保留建议、偏好排序与可选用户权重、最终提示词命名范围、Q1/Q2状态摘要。
- 不按300–500行机械扩写主入口；Codex UI保留当前合同支持的字段，未增加未经支持的category／entry或占位图标。6个触发器继续集中在axes，三份完整提示词继续集中在示例，避免重复维护。
- 静态演示默认离线；真实策划必须显式--live --model。离线脚本合同21/21通过（含mock），3项有限文字场景符合预期；真实CLI保留最初失败／审批拒绝，明确授权后单次执行45.293秒返回三份文字，无工具／生图事件，独立核对完成；不扩大为辨识、传播效果或稳定性通过。

当前开发版新增身份／核心衣装的策划到生图交接；角色默认仅供构思，历史示例不冒称辨识已验证。单次对照身份与现代剪裁改善，负重关系仍弱，保留IMAGES_PARTIAL；不作单变量归因。

当前开发版补充失败修正交接、摄影调整依据及争议目标确认；只对用户已明确否定的核心问题等待确认，普通新图保持原流程。13项有限文字场景符合约定，图片复核仍有比例漏判；未安装、未发布或追加生图，原失败记录保留。
