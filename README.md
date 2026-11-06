# AI Daily Hub · 多栏目技术日报中心

**官网（需 GitHub Pages 已启用）**：https://aisuperteacher.github.io/ai-daily-hub/

这是一个以**完整报告原文**为核心的静态归档网站。支持栏目切换、日期选择、全文搜索、独立打开每篇 HTML，手机浏览器可使用。站点无需前端依赖、CDN 或外部字体。

## 栏目与迁移状态

> 表中“运行中 / 暂停”反映 2026-11-06 所检查的 **ChatGPT 自动化任务状态**，不是 GitHub Actions 的任务。网站栏目建立不代表生成任务已经迁移到 GitHub；任务开关不会因站点发布而改变。

| 栏目 | ChatGPT 状态 | 已导入完整报告 | 任务频率 |
|---|---|---:|---|
| [全球 AI 大模型与 Agent 官方日报](./channels/official-ai.html) | 运行中 | 8 期 | 北京时间每日 08:00 |
| [AI Coding 工具日报](./channels/ai-coding.html) | 暂停 | 0 期 | 原计划：每日 07:00（北京时间） |
| [GitHub 热榜日报](./channels/github-trending.html) | 暂停 | 0 期 | 原计划：每日 07:00（北京时间） |
| [AI 短剧制作技术雷达](./channels/ai-video.html) | 暂停 | 1 期 | 原计划：每日 07:00（北京时间） |
| [企业架构与 AI-native 精选](./channels/architecture.html) | 周一运行中；周四暂停 | 0 期 | 周一运行中 · 周四已暂停 |
| [自媒体平台政策周报](./channels/creator-policy.html) | 运行中 | 0 期 | 每周日（北京时间） |
| [每日科技工作简报](./channels/tech-brief.html) | 暂停 | 0 期 | 原计划：每日 08:00（北京时间） |
| [AI / Cloud 活动与奖励](./channels/offers.html) | 暂停 | 0 期 | 原计划：每日巡检（北京时间） |
| [每日 AI 五词精讲](./channels/learning.html) | 暂停 | 0 期 | 原计划：每日 08:00（北京时间） |

当前共 **9 个公开栏目、9 份完整 HTML 报告**。其中全球 AI 官方日报收录 2026-10-30 至 2026-11-06 的 8 期；AI 短剧另收录 2026-10-03—10-06 的完整历史补档。其他栏目虽有历史自动化运行记录，但对应完整 HTML 目前无法在本次可访问文件库中取得；**不能把运行消息、失效沙箱链接或截断的 12K 字符当作完整日报**。

所有栏目都有独立可分享链接，例如：
- [AI Coding 日报](./channels/ai-coding.html)
- [GitHub 热榜](./channels/github-trending.html)
- [企业架构精选](./channels/architecture.html)
- [自媒体政策周报](./channels/creator-policy.html)
- [AI 短剧](./channels/ai-video.html)

## 目录结构

```text
/
├── index.html                   # 多栏目网页：路由、日期和跨日报搜索
├── manifest.json                # 公开栏目和历史报告索引
├── channels/<topic>.html        # 可分享的各栏目入口
├── reports/YYYY-MM-DD.html      # 现有官方 AI 技术日报
├── reports/<topic>/*.html       # 其他专题完整原文
└── scripts/add_report.py        # 安全导入报告、更新索引
```

## 继续导入其他任务的日报

从原定时任务会话获得**完整 HTML 文件**，先检查日期、版权、密钥、个人资料和报告内容是否适合公开，再执行：

```bash
python scripts/add_report.py \
  --topic ai-coding \
  --date 2026-11-06 \
  --file /path/to/full-report.html \
  --title "AI Coding 工具日报｜2026-11-06"

git add manifest.json reports/ai-coding/2026-11-06.html
git commit -m "Archive full AI Coding report 2026-11-06"
git push origin main
```

添加完整 HTML 后，下一次 GitHub Pages 发布即可自动在对应栏目显示新日期。脚本只检查基本 HTML 完整性，**发布前还须人工复核它是否包含真实完整正文、来源和脱敏内容**。

## Pages 与 GitHub Actions 的职责

- **GitHub Pages**：只负责展示和静态文件托管，不能在每天 07:00 自行运行模型巡检。
- **ChatGPT 定时任务**：当前仍按原状态运行或暂停；本仓库不会修改其计划时间、时区或启用状态。
- **GitHub Actions**：如果未来迁移任务执行，需要为各栏目开发获取官方增量、模型调用、来源校验、生成报告、验证和提交的实际工作流，并在 Secrets 中保存 API 密钥。尚未配置这些执行流，**不要声称日后内容会自动增加**。
- **历史补录**：可直接导入对应日期的完整 HTML，但要保留原始发布时间并避免重编发布日期。

## 公开发布安全策略

本仓库为公开仓库。**知识库截止日期自检、Dropbox 增量备份、特定项目 CI 监控等带个人文件和内部环境信息的结果不会直接上公网**；不公开 API Keys、Cookies、访问令牌、私有业务数据、内部连接信息或敏感配置。AI/Cloud 活动栏目只适合发布可公开核实的优惠信息，账户专享价格需另行处理。

## 验证

GitHub 仓库内文件能够回读不代表公网 Pages 已经部署成功。确认 Pages 的 **Settings → Pages** 指向 `main` 分支 `/(root)`，再从手机或桌面浏览器实际打开上面的站点链接进行可视化检查。
