# AI Daily Hub · 多栏目技术日报中心

**GitHub Pages（需 Pages 部署成功）**：https://aisuperteacher.github.io/ai-daily-hub/

本仓库展示可核对来源的**完整原始技术日报与周报**。保留已有首页、栏目切换、日期筛选和搜索功能。历史补档按报告实际日期展示，绝不以摘要或一段运行通知冒充完整原文。

## 2026-11-06 实时任务核查

ChatGPT 自动化管理接口本次返回 **12 项已启用、0 项暂停**。其中 9 项属于适合公开的内容发布栏目，另外 3 项不全部属于日报：

| 自动化任务 | 状态 | 执行计划（北京时间） | 完整 HTML 入库 |
|---|---|---|---:|
| 全球 AI 大模型与 Agent 技术官方日报 | 已启用 | 每日 08:00 | 10 |
| AI Dev Tools Daily Brief | 已启用 | 每日 07:00 | 0 |
| GitHub 热榜日报 | 已启用 | 每日 07:00 | 0 |
| AI 短剧技术日报 | 已启用 | 每日 07:00 | 1 |
| Distributed & AI Architecture Weekly - Monday | 已启用 | 每周一 08:00 | 0 |
| 自媒体政策周报 | 已启用 | 每周日 08:00 | 0 |
| 每日科技工作简报 | 已启用 | 每日 08:00 | 0 |
| AI/Cloud 活动奖励巡检 | 已启用 | 每日 08:00 | 0 |
| 每日 AI 五词精讲 | 已启用 | 每日 08:00 | 0 |
| Business 48月优惠 | 已启用 | 每日巡检 | 不公开：可能涉及账号及地区专属优惠 |
| 知识库日期自测 + Dropbox 增量备份 | 已启用 | 每日 05:00 | 不公开：私人备份 |
| 全球 AI 大模型与 Agent 技术官方日报｜日期归档 — Auto update | 已启用 | 每小时（独立的 ChatGPT Page 控制器） | 不属于日报 |

> **说明**：状态以本次接口查询为准，而非以过去的任务运行成功与否推断。表中计划时间按任务定义展示；定时任务可能延迟运行。既有文档中“暂停”状态已据此纠正。页面栏目数与自动化任务数不同，因为后 3 项不进入公开的日报分类。

## GitHub 自动归档和部署（2026-11-06 已配置）

- 9 项公开日报/周报的**独立 ChatGPT 自动化提示词**均增加了完整 HTML 的 GitHub 提交、manifest 合并、并发冲突重试及回读验证规则，且原有执行计划、启用状态和全文交付要求不变。
- **绝对分离**：`全球 AI 大模型与 Agent 技术官方日报`（任务 ID `6aa07a92a9fc8191ae71ba51b32a7075`）独立生成和归档官方 AI 日报；`全球 AI 大模型与 Agent 技术官方日报｜日期归档 — Auto update`（任务 ID `Automation_da61d44543e08191b799f1b239903674`）是 ChatGPT Page 的独立控制器，未被更改，不参与 GitHub 写入。
- [查看 12 项任务独立清单](./tasks.html)；公开网页可从首页顶部访问。
- [GitHub Pages 部署工作流](./.github/workflows/publish-pages.yml) 在 `main` 分支相应文件变更时自动运行，另每天 03:17 UTC（北京时间 11:17）对归档索引进行核验和补齐。仅构建并上传公开文件。
- [归档校验与补齐脚本](./scripts/reconcile_archive.py) 检查已入库 HTML 的完整性、路径、索引统计；检查并收录符合要求且未入索引的完整 HTML，不以摘要造假。
- **首次部署实测成功**：GitHub Actions `Publish AI Daily Hub` run [42154234855](https://github.com/aisuperteacher/ai-daily-hub/actions/runs/42154234855)，9 个栏目、11 份完整 HTML 均通过校验，Pages 部署步骤成功。
- **尚未端到端验证的部分**：新提示词在 ChatGPT 定时执行时能否访问 GitHub connector 并提交完整文件，需要下一次实际运行后检查该期报告是否进入仓库。提示词不授予新的 GitHub 权限，且 GitHub Pages 不会自动拉取 ChatGPT 的私有历史对话。
- **历史缺失**：已检查当前可访问的 ChatGPT 文件库及 Dropbox 历史备份，无法找回其他栏目原始完整 HTML；旧的截断运行结果或失效 sandbox 链接不可当作完整报告导入。

## 现有历史报告

当前已入库 **11 份完整 HTML**：

- 全球 AI 官方日报：2026-10-30 至 2026-11-06，共 8 份；加上 **2026-10-15 13 家厂商完整报告**、**2026-10-03 至 10-07 OpenAI / Anthropic 补档**，共 10 份。
- AI 短剧技术雷达：2026-10-03 至 10-06 的一份合集报告。
- 其他栏目：已有自动化执行记录，但在本次可以取得的文件库中仍未找到对应完整原始报告。**不将自动化最后消息、截断文字、失效的 sandbox 链接上传为完整日报。**

## 重要说明：历史并未全部找回

ChatGPT 定时任务查询通常仅提供最新一次的运行记录和最新输出，并非可遍历的全部历史运行日志；部分最新输出还是 12,000 字截断文本，或仅包含到期的临时 HTML 文件链接。仓库当前没有这些旧文件的可验证完整副本，**因此不能宣称所有历史日报已全部迁移**。

若之后从原会话、文件库或备份中取回完整 HTML，可使用 `scripts/add_report.py` 安全导入；添加后应核查完整性、原始日期、来源与敏感信息，再更新 `manifest.json`。

## 静态网站和自动化的区别

- **GitHub Pages** 只负责发布 `main` 分支的网页、搜索和按日期浏览；GitHub 文件存在不等于 Pages 网页已经部署。
- **ChatGPT 12 个原自动化**：本次没有改动启停、提醒、频率或执行提示词；也未将其迁到 GitHub Actions。
- **GitHub Actions 未来自动归档**：还需要单独配置经过授权的日报产出/文件同步机制。无法通过 Pages 单独直接获取 ChatGPT 私有会话和临时文件。
- **公开边界**：不上传 Dropbox 备份、个人账号优惠结算、API Key、Cookie、Token、私有工作数据、内部项目材料或未脱敏工作空间内容。

## 路径

```text
/
├── index.html
├── manifest.json
├── channels/
├── reports/YYYY-MM-DD.html
├── reports/official-ai/2026-10-15_13_providers.html
├── reports/official-ai/2026-10-07_catchup.html
├── reports/ai-video/
└── scripts/add_report.py
```

[查看首页](https://aisuperteacher.github.io/ai-daily-hub/) · [GitHub 仓库](https://github.com/aisuperteacher/ai-daily-hub)
