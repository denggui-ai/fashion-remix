# fashion-remix 文件核对清单

根目录：`fashion-remix/`；合并后共24个文件：原19个＋4份director参考＋1个恢复脚本。
所有原文件保留；空目录占位文件0行，角色模板中的填写位是有意保留。行数含空行。

|文件路径|是否存在|行数|关键内容一句话|状态|
|---|---|---:|---|---|
|`fashion-remix/.gitignore`|是|4|忽略系统文件、缓存、日志与环境文件|完整|
|`fashion-remix/CHECKLIST.md`|是|48|合并后24文件、实际行数、验证范围和边界|完整|
|`fashion-remix/LICENSE`|是|21|MIT许可全文及指定作者署名|完整|
|`fashion-remix/README.md`|是|122|三模式用法、固定作者安装地址、工具依赖和旧版归档范围|完整|
|`fashion-remix/SKILL.md`|是|185|三模式分流、意图优先级、完成条件、3张拓扑和10条元规则|完整|
|`fashion-remix/agents/openai.yaml`|是|7|时尚重塑名称、fashion标签和三模式UI描述|完整|
|`fashion-remix/assets/.gitkeep`|是|0|保留空素材目录|完整|
|`fashion-remix/examples/demo-sha-seng.md`|是|91|三套完整时尚老沙方案、提示词与编号续改|完整|
|`fashion-remix/references/audiences/chinese-general.md`|是|29|华人普通受众的识别假设和传播表达|完整|
|`fashion-remix/references/characters/README.md`|是|28|添加角色方法与角色目录|完整|
|`fashion-remix/references/characters/_template.md`|是|50|新角色十字段、依据与候选锚点模板|完整|
|`fashion-remix/references/characters/sha-seng.md`|是|49|沙僧十字段、符号线索、混淆与转译关系|完整|
|`fashion-remix/references/core/anchor-grading.md`|是|34|本轮SABC、冲突取舍与辨识复查|完整|
|`fashion-remix/references/core/audit.md`|是|46|四视角反偏见审计与确定性说明|完整|
|`fashion-remix/references/core/axes.md`|是|28|八个颠覆轴及可选构思触发器|完整|
|`fashion-remix/references/core/compile.md`|是|48|唯一方案卡、提示词与修订定义，连接共享记录|完整|
|`fashion-remix/references/core/deconstruct.md`|是|28|十字段含义、观察方法与未知处理|完整|
|`fashion-remix/references/core/systems.md`|是|51|26个关系入口与碰撞公式|完整|
|`fashion-remix/references/director/conversation-state.md`|是|108|共享任务、文字快照、图片父版及真实资产恢复|完整|
|`fashion-remix/references/director/creative-direction.md`|是|68|承接已选方案、自由经典画面与多人摄影执行|完整|
|`fashion-remix/references/director/input-and-qc.md`|是|83|输入职责、检查、授权次数及完整交付状态|完整|
|`fashion-remix/references/director/photography-methods.md`|是|131|15类摄影关系及已定命题的摄影实现|完整|
|`fashion-remix/scripts/inspect_task.py`|是|205|原样迁入的只读任务、资产与父版检查脚本|完整|
|`fashion-remix/scripts/run-demo.sh`|是|53|实际读取示例、选择提示词与用法说明|完整|

## 重点核对

- [x] 主入口包含三种模式；文字迭代、真实编辑、零生图回退分别处理。
- [x] 已选方案优先；自由图片任务才默认经典画面，不重写已选原创构思。
- [x] 策划定义统一采用core；摄影执行与恢复采用director，同一方案转成图继续同一任务。
- [x] 3张Mermaid和10条元规则保留；库外角色继续可用。
- [x] 相对引用与脚本深度已更新；全部本地链接须经交付核验。
- [x] README用户名为denggui-ai；MIT署名为denggui-ai (饭饭是条狗子)。
- [x] 原示例和恢复脚本均保留；开发验证证据另存，不随公开运行包分发；已验证范围见README。
- [x] 原图库与旧源8文件保留；旧安装7文件完整归档，新安装不在本次发布中更新。

## 完成范围

“完整”指文件与定义齐备；路径、结构、示例和原资产读取按实际核验报告，不代表真实生图、隐式触发、公众辨识或传播效果已验证。
发布目标为denggui-ai/fashion-remix的v1.1.0源码与标签；本机安装和第一提示词单张生成已验证，隐式触发检查2/3命中本Skill，详细限制见README。
52张图库保留项目原位，不属于本包；旧安装已归档至隐藏父目录，本包不附带私人素材或开发日志。
