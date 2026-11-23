# 示例代码

## 1. 确定性模拟 Agent（零外部依赖）

```bash
python3 examples/deterministic_loop.py
python3 -m unittest discover -s tests -v
```

它故意不用 LLM，展示一个 Agent Loop 必须具备的状态、工具分发、最大步骤和失败处理。真实 Agent 中的决策器可以替换为模型调用，但安全约束仍应由代码强制执行。

## 2. 真实模型的 Tool Calling（选做）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai
export OPENAI_API_KEY='your-key-from-a-secret-manager'
export OPENAI_MODEL='a-model-available-to-your-account'
python3 examples/openai_tool_agent.py
```

该示例只暴露两个算术工具，不读取文件、不调用 Shell、不访问网络上的用户数据。**模型选择由环境变量显式配置**。示例 API 按 Responses 风格编写；供应商 SDK 有演进时请核对官方文档。
