# Dynamic Rules

> Auto-generated rules from dialogue patterns
> Format: YAML (see dialogue_optimizer.md Layer 3)
> Maintenance: Auto-merge when ≥ 20 rules

## Active Rules

```yaml
- id: DR-002
  created: 2026-01-17
  frequency: 1
  category: tool_usage
  title: "工具失败自动切换"
  content: "哪个好用用哪个，一个失败了就换另一个方法。不要只报告失败，要自动切换"
  rationale: "用户指出git push失败后，我没有切换到mcp__github__push_files。用户明确'哪个好用用哪个，一个失败了就换另一个方法'"
  impact:
    token_saving: "0%"
    reliability: high
    priority: highest
  status: active
  examples:
    good: "git push失败 → 自动切换mcp__github__push_files → 完成"
    bad: "git push失败 → 报告'推送失败'，等待用户指示"

- id: DR-003
  created: 2026-01-18
  frequency: 3
  category: user_preference
  title: "用户要求'具体化'时的响应策略"
  content: "当用户明确要求'具体点'、'讲详细点'、'不要泛化'时，优先给出具体案例、可执行建议、数据支撑。大幅减少或完全删除通用解释、理论框架、背景原理。但如果用户的后续问题表明需要理论支撑，则补充简要说明。"
  rationale: "用户通常要求具体化是为了快速获得可执行建议，但有时候也需要理解背后的原理。一刀切地删除所有理论会导致用户无法理解建议背后的逻辑。"
  impact:
    token_saving: "20-30%"
    user_satisfaction: high
    priority: high
  status: active
  examples:
    good: "用户说'讲具体点的配偶建议' → 直接给出ENFP/INFJ具体画像+行为模式+如何识别。如果用户后续问'为什么是ENFP'，再补充认知功能理论。"
    bad: "用户说'讲具体点的配偶建议' → 先讲MBTI理论（10分钟），再讲认知功能（10分钟），最后才给具体建议。用户已经在对话中明确表示'讲的不要太泛化'，但仍提供大量泛化内容。"

- id: DR-004
  created: 2026-01-18
  frequency: 1
  category: accuracy
  title: "引用用户私人信息前必须验证来源"
  content: "引用用户的私人经历、日记内容、人名关系前，必须先用Grep/Glob工具验证信息确实存在于用户文件中。如果无法验证，则明确说明'我从之前对话中了解到...'或'我无法确认这个信息的来源'。"
  rationale: "本次对话中人名引用来源错误，用户指出后才意识到未经验证。这是一个严重的准确性问题，会损害用户信任。"
  impact:
    token_saving: "5%"
    error_prevention: critical
    user_trust: critical
    priority: highest
  status: active
  examples:
    good: "引用前先用Grep搜索关键词，确认存在后再引用。例如：Grep('某人名') → 找到日记 → 引用原文。"
    bad: "基于记忆或之前对话历史直接引用，未验证当前文件库。例如：直接说'你在日记中说某段位太高'，但实际文件中找不到这条内容。"

- id: DR-005
  created: 2026-01-18
  frequency: 2
  category: efficiency
  title: "多文档生成时的内容重复处理策略"
  content: "当生成多个可能包含重叠内容的文档时，评估用户需求：（1）如果用户需要独立文档（每个文档可单独使用），则允许必要的重复。（2）如果用户需要节省token/避免冗余，则使用引用替代重复。（3）默认情况下，优先考虑用户的独立使用需求，其次考虑token节省。"
  rationale: "原规则'避免重复'太死板，有时候用户需要每个文档都是完整的。应该根据用户需求灵活处理。例如：个人分析总览和MBTI深度分析，如果总览是快速入口，就应该包含完整内容；如果总览是索引，就应该引用详细文档。"
  impact:
    token_saving: "10-20%"
    user_experience: high
    priority: medium
  status: active
  examples:
    good: "生成个人分析总览时，先评估用户是需要'快速了解的入口'还是'完整的独立文档'。根据需求决定是否重复MBTI分析内容。"
    bad: "无论用户需求如何，都强制避免重复，导致'个人分析总览'无法独立使用，必须跳转才能看到完整信息。"

- id: DR-007
  created: 2026-01-19
  frequency: 1
  category: accuracy
  title: "结合用户个人特征而非泛化理论"
  content: "分析用户问题时，必须结合用户的具体情况、日记内容、行为模式，不能只讲理论框架（如'INTJ都是这样'）。引用用户的原话和案例，而非泛化的理论描述。避免'攻略游戏'式的建议，聚焦于'适合什么类型'和'什么情况不要错过'。"
  rationale: "用户指出'你确定是针对我来分析的不是根据intj来分析的，我的一些个性你有考虑到吗'。用户只需要知道适合什么类型+遇到什么类型不要错过，不需要'怎么攻略'的行动建议。之前的分析太理论化，没有结合用户的实际情况（被动社交、工具性为主、焦虑螺旋、AI依赖等）。"
  impact:
    relevance: critical
    user_trust: high
    accuracy: critical
    priority: highest
  status: active
  examples:
    good: "你真正需要的人：1.温和主动的技术同行（理解你的AI追求，不会强势控制）2.成熟理性的思考者（能聊自由意志，不会同辈比较）。遇到这些信号不要错过：对方主动找你>2次、能聊深度话题>30分钟、温和且靠谱。"
    bad: "INTJ最适合INFJ或ENFJ。INFJ的主导功能是Ni，能理解你的深度思考。ENFJ的Fe功能能主动发起，弥补你的被动。建议你参加哲学读书会、技术会议来遇到这些人。（太理论化，没有结合用户的实际情况）"


- id: DR-008
  created: 2026-02-10
  frequency: 2
  category: architecture
  title: "纯Skill架构规范 (Skill-Only Architecture)"
  content: "系统采用纯Skill架构，不使用预定义Agent文件。1. Skill (能力层): 位于 .claude/skills/，是被动调用的能力封装。通过Skill工具或Slash Command触发，按需加载。2. 子任务分派: Claude Code主模型自行判断是否需要Task工具分派子任务，无需预定义Agent角色。3. 复杂知识分层: SKILL.md保持<300行核心定义，长内容放子目录（如frameworks/、templates/）。"
  rationale: "2026-02-10迁移：删除全部6个Agent文件，唯一知识已迁移至对应Skill。Claude Code主模型的自动路由能力使预定义Agent冗余。纯Skill架构更轻量、无context膨胀。"
  impact:
    architecture_clarity: critical
    development_standard: high
  status: active
  examples:
    good: "心理咨询需求 → 主模型直接加载counselor Skill处理。复杂子任务 → 主模型用Task工具分派，无需预定义Agent。"
    bad: "为每个场景预定义Agent prompt文件（冗余+维护成本高），或把所有知识塞进SKILL.md（>500行导致加载慢）。"

- id: DR-027
  created: 2026-02-10
  frequency: 1
  category: content_quality
  title: "Markdown元数据完整性原则 (Metadata Integrity Protocol)"
  content: "在生成Markdown文档时，如果包含YAML Frontmatter（---包裹的元数据），它必须位于文件的绝对首行（第1行）。严禁在Frontmatter之前插入任何字符（包括空格、空行、WikiLink、标题或注释）。WikiLink必须放在Frontmatter之后。"
  rationale: "Obsidian及静态生成器仅解析文件头部的Frontmatter。前置内容会导致元数据失效，破坏Tag和别名系统。"
  impact:
    file_validity: critical
    obsidian_compatibility: critical
  status: active
  examples:
    good: "---\ntags: [news]\n---\n[[Link]]"
    bad: "[[Link]]\n---\ntags: [news]\n---"

- id: DR-009
  created: 2026-01-20
  frequency: 1
  category: context_management
  title: "每个对话结束时记录到临时文档"
  content: "每个对话结束时，必须将对话记录追加到对应的临时文档中。文档位置：.claude-temp/{话题名}_{日期}/对话记录_{序号}.md。这样每个对话都不害怕超过上下文限制，可以随时恢复上下文。"
  rationale: "用户要求'记得以后每个对话都这样，这样每个对话都不害怕超过上下文限制了'。当对话因上下文限制被压缩后，可以通过读取临时文档快速恢复之前的对话内容。"
  impact:
    context_continuity: critical
    user_experience: high
    data_persistence: critical
    priority: highest
  status: active
  examples:
    good: "某话题对话 → .claude-temp/某话题对话记录_20260119/对话记录_01.md → 每次对话后追加记录 → 压缩后可快速恢复"
    bad: "长时间对话 → 上下文满了 → 被压缩 → 用户问'我们之前聊到哪了' → AI说'我也不知道' → 对话断裂"

- id: DR-010
  created: 2026-01-20
  frequency: 1
  category: accuracy
  title: "禁止武断下结论，必须基于充分证据"
  content: "在信息不足的情况下，禁止给出具体百分比、明确判断或绝对结论。当用户表示'不知道'、'不清楚'时，不要替用户做决定或给出标准答案，而是通过苏格拉底式提问帮助用户自己发现答案。对于需要判断的内容，必须说明'基于有限信息'、'可能'、'需要更多信息'。"
  rationale: "用户指出在分析某人符合度时直接给出'80%符合'的结论太武断。用户明确表示'我也不知道我喜欢什么性格的女生'，但AI却直接判断理想型是ESFJ/ENFJ。用户三次强调'不要武断下结论'。"
  impact:
    accuracy: critical
    user_trust: critical
    analysis_quality: high
    priority: highest
  status: active
  examples:
    good: "用户：我理想型是什么样的？\nAI：你提到喜欢'好看+不脾气大+关系好'的女生。我们可以慢慢探索：①你之前遇到过的女生中，谁让你觉得最舒服？为什么？②你和朋友相处时，什么样的相处模式让你觉得开心？③你绝对不能接受什么样的行为？"
    bad: "用户：我理想型是什么样的？\nAI：你的理想型是ESFJ。某人80%符合你的理想型。你应该去找ESFJ类型的女生。（用户只提供了少量信息，AI就给出了绝对判断）"

- id: DR-011
  created: 2026-01-22
  frequency: 1
  category: efficiency
  title: "方案设计先给列表，确认后再详细"
  content: "当用户要求'分析哪些可以优化/添加'时，先给简洁列表（不超过1KB），询问用户'哪些你觉得有用？'，等用户确认后再详细设计。禁止直接创建详细方案。"
  rationale: "本次对话创建17KB详细方案，但用户只需要'看看有什么'，浪费15KB token。应该先给简洁列表（<1KB），确认用户需求后再详细设计。"
  impact:
    token_saving: "85-95%"
    user_satisfaction: high
    priority: high
  status: active
  examples:
    good: "用户：分析哪些可以优化？\nAI：我发现可添加X/Y/Z（简洁列表<1KB），你觉得哪些有用？"
    bad: "用户：分析哪些可以优化？\nAI：创建17KB详细方案，包含完整代码示例和文件内容"

- id: DR-012
  created: 2026-01-22
  frequency: 1
  category: documentation
  title: "文档时间戳包含时分秒"
  content: "所有创建的文档必须包含完整时间戳（YYYY-MM-DD HH:MM:SS），格式：'创建时间: 2026-01-22 14:30:00'。只用日期（2026-01-22）是不够的。"
  rationale: "用户明确指出文档只有日期无法分辨修改先后，需要精确到秒的时间戳。"
  impact:
    clarity: critical
    version_control: high
    priority: high
  status: active
  examples:
    good: "> **创建时间**: 2026-01-22 14:30:00"
    bad: "> **日期**: 2026-01-22"

- id: DR-016
  created: 2026-01-22
  frequency: 1
  category: safety
  title: "方案执行前必须等待用户确认"
  content: "在Plan Mode之外，如果涉及到复杂的文件修改（>1个文件）或不可逆操作，必须先简述方案，并明确等待用户输入'同意'或'执行'后，再调用工具。严禁在同一个回复中'先斩后奏'（即提出方案后紧接着就调用工具执行）。"
  rationale: "用户多次抱怨'不要直接开始'、'等等'。AI过于主动会导致用户来不及纠正错误的方向。必须给予用户'踩刹车'的机会。"
  impact:
    safety: critical
    user_control: critical
    priority: highest
  status: active
  examples:
    good: "AI: 我准备修改X和Y文件，添加Z功能。是否执行？\n(等待用户回复)\n用户: 执行。\nAI: Tool(Write...)"
    bad: "AI: 我准备修改X和Y文件。Tool(Write...)"

- id: DR-017
  created: 2026-01-22
  frequency: 3
  category: efficiency
  title: "多文件读取必须并行"
  content: "当需要读取多个文件时，必须使用Glob+并行Read，而非串行读取。7个文件串行读取=7t，并行读取=2.3t，节省66%时间。"
  rationale: "本次对话读取7个agent文件时串行执行，浪费了66%时间。Glob工具可快速定位文件，Read工具支持并行调用。"
  impact:
    token_saving: "0%"
    time_saving: "66%"
    performance: critical
    priority: high
  status: active
  examples:
    good: "Glob('agents/*.prompt.md') → Read(product, architect, frontend) 同时读取3个文件"
    bad: "Read('product.prompt.md') → Read('architect.prompt.md') → Read('frontend.prompt.md') 串行3次"

- id: DR-019
  created: 2026-01-30
  frequency: 0
  category: thinking_methodology
  title: "思维工具箱综合应用"
  content: "使用思维工具选择矩阵，根据场景自动匹配工具：第一性原理（分析/优化/设计）、苏格拉底诘法（用户不确定）、奥卡姆剃刀（方案选择）、布鲁姆金字塔（学习指导）、水平思考（创新）、帕累托法则（效率优化）、系统思维（复杂系统）、墨菲定律（风险评估）。详细协议见thinking-toolkit_完整版.md"
  rationale: "用户要求综合运用多种思维方法提高对话水平，但需平衡token效率。采用矩阵索引+外部文档方案，主文档只增加2.8KB，详细信息按需加载，节省82% token（对比完整添加15KB）。包含8个核心工具+组合协议+触发优先级。"
  impact:
    token_saving: "82%"
    flexibility: critical
    user_satisfaction: high
    analysis_quality: critical
    priority: highest
  status: active
  examples:
    good: "用户：'应该用RayCaster还是深度相机？' → AI：第一性原理+奥卡姆剃刀 → '基于RayCaster有Bug+深度相机更简单，选深度相机拼接'"
    good: "用户：'我想提高执行力' → AI：苏格拉底诘法+第一性原理 → 提问引导+基于INTJ的Se劣势推导方案"
    good: "用户：'需要新功能' → AI：水平思考+布鲁姆金字塔 → 先发散创新再收敛评估"
    bad: "用户：'应该用A还是B？' → AI：'其他人都在用A' → 没有使用奥卡姆剃刀（简单解释优先）"

- id: DR-020
  created: 2026-02-06
  frequency: 1
  category: accuracy
  title: "逻辑计算代码化 (Logic Delegation to Code)"
  content: "对于精确逻辑（日期计算、数学运算、复杂约束），必须委托给 Python/Bash 脚本执行，严禁依赖 LLM 在 Prompt 中进行推断。"
  rationale: "daily-news v4.1 证明 LLM 无法稳定处理 'Today - 1 day' 的日期逻辑。v5.0 通过 Python 脚本计算并注入变量，彻底解决了该问题。"
  impact:
    accuracy: critical
    error_prevention: high
  status: active
  examples:
    good: "Python算好 'yesterday=2026-01-31' → 注入 Prompt: 'Search for {yesterday}'"
    bad: "Prompt: 'Search for news from the day before {today}' (LLM可能算错)"

- id: DR-021
  created: 2026-02-06
  frequency: 1
  category: content_quality
  title: "旅行/生活攻略类文档标准"
  content: "必须使用权威、客观、专业的语气（禁止'日记体'或过于主观的表达）。必须包含'避雷/坑点'检查（需通过小红书/搜索验证）。必须包含图片占位符或链接（Markdown格式）。"
  rationale: "用户明确拒绝'根据日记生成'的随意风格，要求'权威'和'专业'。强调必须验证'避雷'点，不能瞎编。"
  impact:
    user_satisfaction: critical
    accuracy: high
  status: active
  examples:
    good: "语气：'建议早上8点出发'（笃定）| 避雷：'西街拍照收费坑点多，建议先问价'（经验证）"
    bad: "语气：'今天我去了西街，感觉还不错'（日记体）| 避雷：'西街很完美，没缺点'（未验证）"

- id: DR-023
  created: 2026-02-09
  frequency: 1
  category: documentation
  title: "智能文档策略：情境化决策 (Contextual Decision)"
  content: "在生成文档前，必须分析新内容与现有知识库的关系。决策逻辑：(1) 内容是现有文档的补充、解释或延伸 -> 修改/追加到现有文件。(2) 内容是全新的独立领域或篇幅极长(>2000字) -> 创建新文件。(3) 严禁为每个零散问题创建碎片化文档。"
  rationale: "用户强调不是单纯的'优先追加'，而是'分清后自动抉择'。目标是构建连贯的知识体系，而非碎片化的文件堆。"
  impact:
    file_hygiene: critical
    knowledge_cohesion: critical
    priority: highest
  status: active
  examples:
    good: "用户问'C++数组越界' -> 检测到'C系列语言辨析.md' -> 追加章节。用户问'量子计算入门' -> 无相关文档 -> 创建新文件。"
    bad: "用户问'C++数组越界' -> 盲目创建新文件。用户问'量子计算' -> 强行追加到'C++文档'。"

- id: DR-024
  created: 2026-02-09
  frequency: 1
  category: documentation
  title: "文档自动互链机制"
  content: "在生成或修改文档时，必须在文末添加'## 📚 延伸阅读'或'## 🔗 相关文档'章节。使用Glob搜索项目中的相关文档，并添加Markdown相对链接。如果没有直接相关文档，则链接到父级索引或同类文档。"
  rationale: "用户要求'自动插入链接'，以便在复习时能关联相关知识。孤立的文档价值低，互链的文档构成知识库。"
  impact:
    knowledge_graph: high
    user_experience: high
  status: active
  examples:
    good: "在'React科普.md'文末添加：\n## 🔗 相关文档\n- [前端vs后端](前端vs后端与软件开发全貌_科普_2026-02-09.md)\n- [JS语言辨析](JS_CSS_HTML科普.md)"
    bad: "文档以'## 总结'结束，没有链接到其他相关文件。"

- id: DR-025
  created: 2026-02-09
  frequency: 1
  category: system_maintenance
  title: "配置自同步原则"
  content: "当dynamic_rules.md更新时，必须检查CLAUDE.md是否需要同步（特别是Trigger定义和核心规则索引）。保持两个配置文件的认知一致性。"
  rationale: "用户指出'CLAUDE.md'经常滞后于'dynamic_rules.md'，导致新规则没有在System Prompt层面上生效。"
  impact:
    system_consistency: critical
    instruction_adherence: high
  status: active
  examples:
    good: "添加了DR-023（智能文档策略）到dynamic_rules → 立即检查CLAUDE.md的Content Strategy是否需要同步"
    bad: "dynamic_rules中有新规则，但CLAUDE.md中还是旧的定义"

- id: DR-028
  created: 2026-02-10
  frequency: 1
  category: accuracy
  title: "精确时间戳获取协议 (Time Precision Protocol)"
  content: "在生成包含时间戳（created/date字段）的文档前，必须显式调用 `date` 工具获取当前系统精确时间。严禁依赖模型内部感知的模糊时间或预设偏移量。"
  rationale: "用户指出文档时间戳严重偏离实际时间（模型估算16:00，实际21:15）。只有系统工具能提供准确的客观时间。"
  impact:
    accuracy: critical
    data_integrity: high
  status: active
  examples:
    good: "调用 `date` → 获知 '21:15:00' → 写入文档 metadata"
    bad: "直接估算 '应该是下午4点左右' → 写入 '16:00:00' (错误)"

- id: DR-029
  created: 2026-02-12
  frequency: 1
  category: task_management
  title: "任务闭环协议 (Task Lifecycle Protocol)"
  content: "当使用 TaskCreate 开启显式任务后，必须在逻辑工作流结束时主动调用 TaskUpdate 将其标记为 completed 或 deleted。严禁将状态为 open 的任务遗留到对话结束，导致任务列表积压。"
  rationale: "用户提醒'任务又忘记关了'。开启任务是为了追踪进度，如果只开不关，会失去任务管理的意义并造成混乱。"
  impact:
    process_integrity: high
    user_experience: medium
  status: active
  examples:
    good: "TaskCreate('Search') -> WebSearch -> ... -> TaskUpdate(status='completed')"
    bad: "TaskCreate('Search') -> WebSearch -> (对话结束，任务仍为 open)"

```

## Rule Statistics
- Total rules: 19
- Active: 19
- Deprecated: 4 (Moved to Core)
- Last updated: 2026-02-09
- Next merge check: At 25 rules
