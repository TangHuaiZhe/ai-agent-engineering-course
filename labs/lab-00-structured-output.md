# Lab 00｜结构化抽取验证与模型评测基座

**对应 Module 02** · 不依赖模型 API Key 的基础实验 · 推荐 1–3 小时。

## 实验目的

建立一个独立于模型的 Output Validator，明确“格式符合 Schema”和“内容可被业务信任”之间的界线。

## 第一步：运行验证器

~~~bash
python3 examples/structured_output_lab.py
python3 -m unittest tests.test_structured_output_lab -v
~~~

示例会对一条有效的模拟财务数据进行校验；所有公司、数值与来源均为**教学用虚构信息**。

## 第二步：实现失败用例

在 [tests/test_structured_output_lab.py](../tests/test_structured_output_lab.py) 阅读现有测试，并新增至少三个边界案例：

- \`fiscal_year\` 为 \`true\`：在 Python 中 \`bool\` 是 \`int\` 的子类，必须使用精确类型判断。
- \`value\` 为 \`NaN\`、\`Infinity\` 或文本形式的数字。
- \`source_id\` 看似合法，但不在当前批准的证据集合中。
- 公司、指标、年份都符合格式，但与实际来源内容不一致（需要业务校验）。

## 第三步：设计 20 条评测数据

分别包含：规范数据、缺失字段、字段类型错误、无来源、单位错误、文档中含混淆描述、恶意指令、跨年度口径冲突。每条记录 expected 与评判依据。

## 第四步（可选）：真实模型对比

自行使用已授权的模型 API，针对上述 20 条案例比较：

- 自由文本 Prompt。
- 要求返回 JSON 的 Prompt。
- API 支持情况下的 Structured Outputs。

统一保存模型 ID、Prompt 版本、日期、Token 消耗、总延迟与判定标准。**不要声称本地模拟器执行了模型推理**。

## 验收

- [ ] 不合法类型、未知字段和无依据的来源 ID 会被拒绝。
- [ ] 能解释为什么严格类型通过后还需要引用、币种、口径检查。
- [ ] 至少增加一个会失败的测试，并正确修复实现或数据。
- [ ] 提供最小评测集与错误分类表。

**评分（100）：** 参数校验 30、错误类型 20、证据完整性 20、评测设计 20、复盘 10。

[返回 Module 02](../modules/02-llm-foundations/README.md)