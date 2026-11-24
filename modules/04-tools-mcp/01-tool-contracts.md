# 04.1｜Tool Calling：模型发起请求，但宿主决定是否执行

## 两个不同的动作

LLM 生成的 Tool Call 是“请求”，不是“完成”。例如：

~~~json
{"name": "search_filing", "arguments": {"company": "Example Inc."}}
~~~

真正执行前，宿主必须检查工具是否存在、用户是否有权限访问该公司的资料、Schema 和业务规则是否通过、是否超过预算。处理器实际完成后，才能把结果作为 Observation 交给模型。

## 一个完整的 Tool Contract

设计工具时至少写明：

| 项目 | 示例 |
|---|---|
| name | \`search_filing\` |
| description | 查询某公司已公开财报，返回来源标识 |
| input | \`company_id\`（字符串）、\`fiscal_year\`（整数） |
| output | 文档 ID、来源 URL、日期、摘要 |
| side_effect | 无，默认只读 |
| permissions | 仅可访问允许公开的文档 |
| timeout / retry | 超时 10 秒；对可重试错误有限次数重试 |
| error codes | invalid_arguments / not_found / unavailable |
| provenance | 来源 URL、报告时间、检索时间 |

**Schema 能帮助格式检查，但不能代替资源级鉴权**。例如 \`{"doc_id":"private-42"}\` 符合字符串 Schema，不意味着当前用户可以读取它。

## 三种工具失败

1. **参数错误**：模型可以根据受控错误修改参数。
2. **临时故障**：例如请求 503，宿主可使用退避和有界重试。
3. **策略拒绝**：权限不足、需要审批、试图访问未授权工具；不能由模型靠重试消除。

对于有副作用的操作，不可以仅靠重试次数来保证一致性。

## 本讲练习

为一个文档检索工具和一个“归档研究报告”工具写下 Tool Contract，分别说明：

- 允许哪些调用者、文件及路径？
- 重复提交会发生什么？
- 哪些错误可重试，哪些不可重试？
- 不可信网页是否能提供执行新工具的权限？（不能）

[下一讲](02-mcp-protocol.md)