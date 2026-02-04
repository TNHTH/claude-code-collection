---
name: daily-news
description: Generates a daily hard-core tech newsletter for automation students, integrating multi-source search, intelligent filtering, and Obsidian archiving. Automates the workflow of searching, filtering, drafting, and archiving news into the user's Obsidian vault.
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

# Read the current user state/context
python .claude/skills/daily-news/scripts/session_manager.py --action read_state
```

**Note**: Do not guess the path. Always use the script output.

### 2. Search Strategy (Multi-Source)
Search for news from **Yesterday** (T-1 day).
*   **Primary Tool**: Use `mcp__tavily-search__tavily_search` (if available) for broad coverage.
*   **Secondary Tool**: Use `WebFetch` or `WebSearch` for specific details if Tavily misses details.
*   **Fallback**: If search fails, retry up to 3 times with exponential backoff.
*   **Keywords**: "AI technology breakthrough", "Robotics automation news", "Semiconductor supply chain", "Hangzhou local policy automation".

### 3. Intelligent Filtering (Priority Logic)
Filter results based on the following priority list:
1.  **Technological Disruption (Highest)**: New algorithms, model releases (e.g., GPT-5, Claude 4), major open source projects.
2.  **Global Affairs**: Elections in major powers, wars, sanctions affecting tech.
3.  **Supply Chain**: Chip availability, raw material prices, logistics.
4.  **Localization**: Hangzhou/Yangtze Delta policies, local job market.
5.  **Living Cost**: Housing, food prices in Hangzhou.

**Exclude**: Pure commercial financing news (unless massive), vague macro predictions, PR fluff without data.

### 4. Content Generation
Generate the Markdown content following the "Content Generation Standard v3.4".

**Good Example (Fact)**:
> "OpenAI released GPT-5 with 2M token context context window (15.6x larger than GPT-4), API price reduced to $0.03/1K tokens."

**Bad Example (Vague)**:
> "OpenAI released a new model that is much better and cheaper."

**Structure**:
1.  **YAML Frontmatter**: (See format below)
2.  **Key Facts**: 6-9 items, cold and objective.
3.  **Trends**: 3-5 items, analysis of shifts.
4.  **Impact**: 3-12 month projection.
5.  **Personal**: Connection to "Automation Major" or "Hangzhou".
6.  **Risks**: Warnings.

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
