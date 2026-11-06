# AI Daily Hub

集中归档 AI 大模型 / Agent 技术官方日报，并逐步承载其他 AI Coding、GitHub 热榜、AI 短剧、企业架构和优惠活动定时任务。

## 网站

GitHub Pages（启用后）：https://aisuperteacher.github.io/ai-daily-hub/

主页 `index.html` 为自包含日报中心，支持按日期切换、跨日报搜索、单日导出。历史原文另存于 `reports/YYYY-MM-DD.html`，保留独立可打开的完整日刊。

## 部署

在 GitHub 仓库 **Settings → Pages → Build and deployment** 中选择 **Deploy from a branch**，分支选 **main**，目录选 **/(root)**，点击 **Save**。首次构建完成后即可使用上面的 Pages 地址。

当前报告只收录能够核对文件完整性的日期，不会编造历史文件。新增报告需在 `reports/` 保存原文并更新主页索引/清单。未来迁移到 GitHub Actions 之前，ChatGPT 已有定时任务保持原调度，不自动停用。

## 扩展计划

- `reports/`：全球 AI 大模型与 Agent 官方日报
- `workflows/`：后续可分模块迁移的工作流
- `scripts/`：后续日报生成、归档和完整性校验

**安全**：不要把模型 API Key、订阅令牌、私有业务数据或未脱敏日志提交到公开仓库。使用 GitHub Actions Secrets 保存私密凭据。
