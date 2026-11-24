# GitHub Pages 部署与维护

课程网站使用 **MkDocs Material + GitHub Actions**，从现有课程 Markdown 自动生成静态站点。仓库原始 Markdown 是唯一内容来源。

## 课程网站地址

https://tanghuaizhe.github.io/ai-agent-engineering-course/

## 首次启用：需要仓库管理员操作一次

1. 打开 [Settings → Pages](https://github.com/TangHuaiZhe/ai-agent-engineering-course/settings/pages)。
2. 在 **Build and deployment → Source** 中选择 **GitHub Actions**。
3. 打开 [Actions → Publish course to GitHub Pages](https://github.com/TangHuaiZhe/ai-agent-engineering-course/actions/workflows/pages.yml)。
4. 如果第一次 Push 在启用 Pages 之前就触发了 Workflow，使用 **Run workflow** 重新运行。
5. 确认 Build 和 Deploy 两个 Job 成功之后，再访问上面的地址。

仅向仓库添加 GitHub Actions Workflow，并不一定能自动开启 GitHub Pages 服务。

## 本地预览

Python 3.11 或以上，推荐 3.12：

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
python scripts/prepare_site.py
mkdocs serve
~~~

本地构建和测试：

~~~bash
python3 -m unittest discover -s tests -v
python3 scripts/prepare_site.py
mkdocs build --strict
~~~

## 自动发布的工作方式

每次向 main 分支推送更新时，GitHub Actions 自动：

1. 安装固定版本文档生成器。
2. 运行课程单元测试。
3. 暂存 Markdown：根目录 README 生成站点 index，其余保持课程目录结构，示例代码作为静态资源。
4. 执行严格 MkDocs 构建。
5. 上传并部署 GitHub Pages 静态文件。

站点 URL 保留 /ai-agent-engineering-course/ 项目子路径，避免网站资源引用错误。

## 故障排查

| 问题 | 处理 |
|---|---|
| Get Pages site failed / Not Found | 先到 Settings → Pages 将 Source 设为 GitHub Actions |
| Resource not accessible by integration | 检查 Pages 权限、OIDC 权限和组织的 GitHub Actions 策略 |
| mkdocs build --strict 报错 | 修复导航路径和 Markdown 内部链接 |
| 访问网址 404 | 先确认两个 Job 都成功、Pages 已开启和发布 URL 正确 |
| 代码示例链接无效 | 检查 prepare_site.py 的 COPY_EXTENSIONS |
| 更新文档后网站未改变 | 检查 Actions 最新运行和部署的提交版本 |

## 安全注意事项

- GitHub Pages 提供公开静态内容，不承载 Agent 后端。
- 不得提交 API Key、凭证或私人文件；构建网站不需要任何模型密钥。

## 源文件

- [网站配置](https://github.com/TangHuaiZhe/ai-agent-engineering-course/blob/main/mkdocs.yml)
- [文档依赖](https://github.com/TangHuaiZhe/ai-agent-engineering-course/blob/main/requirements-docs.txt)
- [发布工作流](https://github.com/TangHuaiZhe/ai-agent-engineering-course/blob/main/.github/workflows/pages.yml)
- [课程首页](../README.md)
