# AI Daily Hub · 多栏目技术日报归档

**网站**：[AI Daily Hub](https://aisuperteacher.github.io/ai-daily-hub/)  
**学习中心**：[按主题学习与回看课程](https://aisuperteacher.github.io/ai-daily-hub/study/)  
**栏目总览**：[查看全部归档栏目](https://aisuperteacher.github.io/ai-daily-hub/tasks.html)

本仓库保存和展示已经提交的公开技术日报、资讯周报与学习报告（完整 HTML）。网站支持栏目切换、历史日期选择、全文搜索及独立打开原始报告。

## 仓库当前内容

根据 `manifest.json`，当前共 **10 个栏目、19 份完整 HTML 报告**。

| 栏目 | 栏目 ID | 已归档报告 |
|---|---|---:|
| [全球 AI 大模型与 Agent 官方日报](https://aisuperteacher.github.io/ai-daily-hub/?topic=official-ai) | `official-ai` | 10 |
| [全球 AI、科技与机器人政策趋势日报](https://aisuperteacher.github.io/ai-daily-hub/?topic=ai-policy) | `ai-policy` | 1 |
| [AI Coding 工具日报](https://aisuperteacher.github.io/ai-daily-hub/?topic=ai-coding) | `ai-coding` | 1 |
| [GitHub 热榜日报](https://aisuperteacher.github.io/ai-daily-hub/?topic=github-trending) | `github-trending` | 1 |
| [AI 短剧制作技术雷达](https://aisuperteacher.github.io/ai-daily-hub/?topic=ai-video) | `ai-video` | 1 |
| [企业架构与 AI-native 精选](https://aisuperteacher.github.io/ai-daily-hub/?topic=architecture) | `architecture` | 1 |
| [自媒体平台政策周报](https://aisuperteacher.github.io/ai-daily-hub/?topic=creator-policy) | `creator-policy` | 1 |
| [每日科技工作简报](https://aisuperteacher.github.io/ai-daily-hub/?topic=tech-brief) | `tech-brief` | 1 |
| [AI / Cloud 活动与奖励](https://aisuperteacher.github.io/ai-daily-hub/?topic=offers) | `offers` | 1 |
| [每日 AI 五词精讲](https://aisuperteacher.github.io/ai-daily-hub/?topic=learning) | `learning` | 1 |

上述数字只统计仓库已经收录的完整 HTML，**不代表所有历史日期均已归档**。栏目、路径及每期报告均可在 [manifest.json](./manifest.json) 核对。

## 目录结构

```text
/
├── index.html                       # 日报首页：栏目、日期与全文搜索
├── tasks.html                       # 仓库已有栏目总览
├── manifest.json                    # 栏目及归档报告索引
├── channels/                        # 栏目入口
├── reports/                         # 归档的独立完整 HTML
│   ├── YYYY-MM-DD.html              # 官方 AI 日报旧路径
│   ├── official-ai/
│   ├── ai-policy/
│   ├── ai-coding/
│   ├── github-trending/
│   ├── ai-video/
│   ├── architecture/
│   ├── creator-policy/
│   ├── tech-brief/
│   ├── offers/
│   ├── learning/
├── scripts/
│   ├── add_report.py                # 导入 HTML 与更新索引
│   └── reconcile_archive.py         # 检查完整性与核对索引
└── .github/workflows/
    └── publish-pages.yml           # GitHub Pages 发布工作流
```

## 发布与校验

向 `main` 分支提交 HTML、索引或站点页面的相关改动时，仓库中的 [Publish AI Daily Hub](./.github/workflows/publish-pages.yml) 工作流负责校验报告、整理索引、构建静态站点并部署 GitHub Pages；此外设有每日一次的索引检查。

- [查看 GitHub Actions 执行记录](https://github.com/aisuperteacher/ai-daily-hub/actions)
- [归档校验脚本](./scripts/reconcile_archive.py)
- [手动导入报告脚本](./scripts/add_report.py)

**边界**：GitHub Pages 展示的是仓库中已经提交的文件，工作流不会凭空生成未提交的日报内容。

## 查看历史报告

在 [日报首页](https://aisuperteacher.github.io/ai-daily-hub/) 按栏目与日期浏览；每期报告都有独立 HTML 路径。历史文件缺失时不以摘要、运行通知或过期链接冒充完整原文。


## 学以致用 · 学习中心

[学习中心](https://aisuperteacher.github.io/ai-daily-hub/study/) 按主题整理完整学习 HTML，支持正文关键词搜索、分类、历史版本、在线交互、独立打开与下载。课程目录为 [`study/catalog.json`](./study/catalog.json)。浏览器只记录最近打开的课程，不把访问记录作为掌握证明。

原始课程按内容哈希保存在 `study/lessons/`；相同文件合并来源别名，不同内容保留版本。每日 AI 五词精讲沿用 `reports/learning/` 的原路径，其已发布报告由构建过程加入学习目录。

新增学习页的筛选、完整性检查、导入和发布约定见 [`study/ARCHIVING.md`](./study/ARCHIVING.md)。使用 `scripts/add_lesson.py` 导入课程，`scripts/build_learning_index.py` 刷新并验证目录。GitHub Actions 只发布实际提交的课程，不能自行读取 ChatGPT Library。
