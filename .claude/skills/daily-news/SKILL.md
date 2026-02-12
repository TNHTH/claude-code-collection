---
name: daily-news
description: |
  每日科技新闻生成器。触发词：每日新闻、daily news、今日要闻、科技快讯、昨天发生了什么、新闻简报、tech news。
  Generates a daily hard-core tech newsletter for automation students, integrating multi-source search, intelligent filtering, and Obsidian archiving.
---

# Daily News Skill

This skill automates the creation of a daily tech newsletter, specifically tailored for an automation engineering student in Hangzhou. It handles the entire pipeline from finding news to saving it in the correct location with proper metadata.

## When to Use This Skill

Use this skill when the user asks for "daily news", "daily brief", "tech news", or "what happened yesterday". It is designed to run once per day to generate a summary of the previous day's key events.

## Workflow Instructions

To execute this skill, follow these steps strictly:

### 1. Initialize Session & Context
First, use the provided Python script to ensure the environment is ready and to retrieve the correct paths and state.

```bash
# Get the canonical output path for today's news (handles Windows paths automatically)
python .claude/skills/daily-news/scripts/session_manager.py --action get_path

# Get robust date calculations (Today vs Yesterday)
python .claude/skills/daily-news/scripts/session_manager.py --action get_dates

# Read the current user state/context
python .claude/skills/daily-news/scripts/session_manager.py --action read_state
```

**Note**: Do not guess paths or dates. Always use the script output.

### 2. Search Strategy (SOP v5.1)
Execute the following 4-phase search strategy strictly.

**CRITICAL DATE LOGIC**: Use the `yesterday` value from Step 1 for all searches.
*   *Search Date*: `{yesterday}` (from `get_dates` output)
*   *Report Date*: `{today}` (from `get_dates` output)

**Phase 1: Macro & Breadth (The "News" Filter)**
*   **Tools**: `mcp__tavily-search__tavily_search` AND `WebSearch` (Run in parallel).
*   **Query A (Tavily)**: `tech news {yesterday} AI robotics semiconductor -finance` (Focus: Major industry events).
*   **Query B (WebSearch)**: `tech news summary {yesterday} automation industry` (Focus: Broad summaries).
*   **Goal**: Create a list of **6-9 candidate topics** (Breadth is key here).

**Phase 2: Depth Verification (Firecrawl)**
*   **Tool**: `mcp__firecrawl__firecrawl_search`.
*   **Target**: Pick 1-2 core hardware/tech topics from Phase 1 (e.g., "AMD new FPGA", "DeepSeek V4 specs").
*   **Query**: Specific technical query (e.g., `AMD Kintex UltraScale+ Gen 2 datasheet specs`).
*   **Goal**: Verify hard numbers (e.g., bandwidth, process node) from official sources.

**Phase 3: Niche Mining (GitHub)**
*   **Tool**: `mcp__github__search_repositories`.
*   **Query**: `query: "AI" created:{yesterday} sort:stars`.
*   **Goal**: Find 1-2 fresh open-source projects (Agents, Tools) that mainstream news misses.

**Phase 4: Localization (WebSearch)**
*   **Tool**: `WebSearch`.
*   **Query**: `Hangzhou local policy {yesterday} automation` OR `Hangzhou robotics jobs {yesterday}`.
*   **Goal**: Find local policy changes or hiring trends relevant to the user.

### 3. Intelligent Filtering (Priority Logic)
Filter results based on the following priority list to select **6-9 Key Facts**:
1.  **Technological Disruption (Highest)**: New algorithms, model releases, major open source projects.
2.  **Global Affairs**: Elections, wars, sanctions affecting tech.
3.  **Supply Chain**: Chip availability, raw material prices.
4.  **Localization**: Hangzhou/Yangtze Delta policies.
5.  **Living Cost**: Housing, food prices in Hangzhou.

**Exclude**: Pure commercial financing news (unless massive), vague macro predictions.

### 4. Content Generation
Generate the Markdown content following the "Content Generation Standard v5.0 (The Daily Brief)".

**Template Structure**:
```markdown
---
date: {YYYY}-{MM}-{DD} (Today's Date)
tags: [每日时事, 自动化, 硬核科技, 趋势分析, {Topic_Tags}]
title: {YYYY}年{M}月{D}日（周{X}）每日要闻
created: {YYYY}-{MM}-{DD} {HH}:{mm}:{ss}
week: {Current_Week_Number}
status: finished
---

## 🕒 昨日速览 (Quick View)
*Summary of T-1 events...*

## 📰 硬核事实 (Key Facts)
*(Target: 6-9 items. Mix of Global Tech + Local Automation)*

1.  **[🏷️ {Category}] {Title}**
    *   **核心信息**: {Hard Facts, Numbers, Specs}
    *   **🔗 关联**: {Broad Relevance to Automation/Career/Industry}

2.  **[🏷️ {Category}] {Title}**
    ...

## 📈 信号与趋势 (Signals & Trends)
*   **信号**: {Weak signals or emerging patterns observed today}
*   **趋势**: {Long-term shifts reinforced by today's events}

## 🎯 影响推演 (Future Impact)
*   **短期**: {Immediate actions or changes for next week/month}
*   **长期**: {Career/Industry shifts for next 1-3 years}

## 🛠️ 开源利器 (GitHub Spotlight)
*挖掘自今日 GitHub Trending*
*   **项目**: [{Name}]({Link}) (🌟 {Stars})
    *   **一句话介绍**: {Concise Description}
    *   **对你的价值**: {Why it matters}

## ✅ 行动建议 (Action Items)
- [ ] **💡 每日一思 (Daily Spark)**: {A quick <5 min thought experiment or calculation}
- [ ] **关注**: {Specific Company/Tech}
```

**Content Guidelines**:
-   **Volume**: Aim for 6-9 Key Facts to ensure breadth.
-   **Analysis**: "Signals & Trends" and "Impact" sections are MANDATORY and must be distinct.
-   **Relevance**: Keep "Broad Relevance" in Key Facts.
-   **GitHub**: Dedicate the GitHub section to 1-2 high-quality tools found in Phase 3.

### 5. Archiving
Write the generated content to the file path obtained in Step 1.

```bash
# Use Write tool to save the content
Write(path_from_step_1, content)
```

### 6. Update State
After successful generation, update the state file.

```bash
python .claude/skills/daily-news/scripts/session_manager.py --action update_state --key last_generated --value "{YYYY-MM-DD}"
```

## Reference Formats

### YAML Frontmatter Template
```yaml
---
date: {YYYY}-{MM}-{DD}
tags: [每日时事, 自动化, 硬核科技, 趋势分析]
title: {YYYY}年{M}月{D}日（周{X}）每日要闻
created: {YYYY}-{MM}-{DD} {HH}:{mm}:{ss}
week: {Current_Week_Number}
status: finished
---
```

## Troubleshooting

-   **Path Issues**: If the path looks wrong, trust the `session_manager.py` output. It handles `os.path.join` correctly for the OS.
-   **State File Corrupt**: The script handles this by returning an empty JSON. Proceed with default settings.
-   **Search Failure**: If all searches fail, generate a "Study Suggestion" edition based on the user's current curriculum (found in state).
