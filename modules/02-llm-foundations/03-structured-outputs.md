# 02.3｜Structured Outputs：格式约束与语义正确性是两件事

## 核心区分

1. **自由文本**：模型给人看的自然语言，程序解析易碎。
2. **JSON 风格提示**：要求模型返回 JSON，但不保证字段、类型或额外内容符合业务要求。
3. **Structured Outputs**：在模型或 API 支持时，使用明确的结构定义约束响应形状。
4. **业务校验（Business Validation）**：宿主代码独立检查格式以外的规则、来源、日期、单位和权限。

一个“合法 JSON”可能仍包含错误数据。例如 \`{"revenue": 1000, "currency":"USD"}\` 在没有来源、期间、单位的前提下仍然不能用于研究结论。

## 本课程的输出契约

用最小财务指标抽取对象：

~~~json
{
  "company": "Example Inc.",
  "fiscal_year": 2025,
  "metric": "revenue",
  "value": 120.5,
  "unit": "million",
  "currency": "USD",
  "source_id": "annual-report-2025-p42"
}
~~~

确定性校验至少覆盖：

- 固定字段集合，拒绝未知字段。
- \`fiscal_year\` 为整数而非字符串或布尔值。
- \`value\` 为有限数；NaN / Infinity 不可接受。
- \`unit\` 和 \`currency\` 必须属于允许的枚举。
- \`source_id\` 必须与已获取证据的 ID 对应。
- 特定指标的数值允许区间、单位换算和跨报告一致性由业务层单独实现。

**拒绝非法输出比静默猜测并纠正更重要。**

## Schema 不会替你解决的问题

即使 Schema 验证全部通过，也可能：

- 把净利润误写为营业收入。
- 把“千元”当作“百万元”。
- 把不同公司、不同财年的数据混在一起。
- 捏造一个看似合法的 \`source_id\`。
- 将财报调整后的数字误认为原始口径。

因此，**结构化输出降低解析失败，不等于消除幻觉或事实错误**。

## Structured Outputs 与 Tool Calling 的区别

Structured Outputs 规定的是模型**最终返回的内容形状**；Tool Calling 规定的是模型**可以请求的动作及其参数**。ToolCall 只有在宿主授权、参数校验并实际执行后才产生真实结果。

课程 [Module 03](../03-agent-architecture/README.md) 中的 Agent Loop 使用代码约束工具执行。

## 实验

~~~bash
python3 examples/structured_output_lab.py
python3 -m unittest tests.test_structured_output_lab -v
~~~

阅读 validator，尝试篡改 \`value\`、\`fiscal_year\`、\`source_id\`，并记录失败码。然后额外添加一个“字段类型正确但公司身份错误”的案例，理解**Schema 验证之外仍需业务核验**。

[上一讲](02-prompt-and-reliability.md) · [下一讲](04-cost-latency-evals.md)