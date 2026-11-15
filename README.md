<div align="center">
  <img src="assets/logo-horizontal.svg" alt="金融宣教 · financial-literacy-education" width="720"/>
</div>

# 金融宣教（Financial Literacy Education）

> 金融机构消费者权益保护 · 教育宣传岗专业 Skill · 版本 v1.0.0

面向金融机构消保部门教育宣传岗的智能副驾。岗位定位是**公益性、普惠性的知识传播者，不是营销推广**：通过系统化、常态化的金融知识普及和风险提示，提升公众金融素养与风险防范意识，从源头减少因信息不对称或认知偏差导致的消费纠纷。

## 四种角色

| 角色 | 场景 | 主要交付物 |
|------|------|-----------|
| **R1 体制机制管理者** | 年度计划、管理办法、经费预算、专业答疑 | 年度计划（文字版 + 表格版）、管理办法、预算表 |
| **R2 活动组织策划者** | 3·15 / 9月金融教育宣传月、五进入、线上线下阵地、监管报送 | 实施方案、阵地标准、活动总结、数据报表 |
| **R3 内容创作者** | 知识"翻译"、以案说险、风险提示、短视频、海报提示词 | 视频脚本、文案、图像生成提示词、互动策划 |
| **R4 效果评估者** | 覆盖统计、效果评估、投诉关联、案例沉淀 | 评估报告、数据台账、优秀案例集 |

复合意图按串行链处理：策划→创作、策划→创作→评估、评估→机制、机制→策划。

## 核心设计

- **依据先行**：任何角色第一个动作都是检索机构知识库，再按需联网核验官方原文；不编造文号、条款号、活动数据，未核实内容标 `[待验证]`；输出前做二次合规复核。
- **四条刚性要求**：年度计划必须"文字版 + 表格版"双格式；管理办法必须覆盖"计划制定→活动策划→组织实施→材料报送→总结评估"五环节；宣教要嵌入业务全流程并留痕；专项经费单列可核查。
- **活动五要素**：主题、时间、地点/渠道、负责人、预计覆盖人次，缺一不可；主题与报送对象逐字核对监管通知。
- **内容接地气**：专业术语翻成大白话，多用生活比喻，不照搬法条；短视频脚本**先故事情节、后分镜**；风险提示必须"现象 + 后果 + 建议"三段。
- **评估有数据有对比**：过程指标与结果指标并重，必须含趋势对比与归因；数据不足时输出需求清单，不生成空心报告。
- **公益边界**：宣教内容不得夹带产品营销、不做法律定性、营销类推送须可拒收退订。

## 目录结构

```
├── SKILL.md                      # 技能主文件：岗位定位、四角色路由、工作流主干、交付规范
├── _icon.png                     # 技能图标（512×512）；SkillHub 卡片图标需在平台端单独上传
├── references/
│   ├── knowledge-base.md         # 六类知识库文档地图、元数据过滤标签、检索与引用规则
│   ├── role-mechanism.md         # R1 作业规范
│   ├── role-event-planning.md    # R2 作业规范
│   ├── role-content-creation.md  # R3 作业规范
│   ├── content-playbook.md       # 生活比喻库、受众分层、渠道与形式矩阵、禁用表达
│   ├── role-effect-evaluation.md # R4 作业规范
│   ├── integration-spec.md       # 集成规格：调度、编排、输入输出协议、工具权限、异常处理
│   └── output-standards.md       # 四角色标准输出结构、命名规范、质量要求
├── templates/                    # 11 类交付物模板
│   ├── annual-plan.md            # 年度计划（文字版）
│   ├── annual-plan-table.md      # 年度计划（表格版 / Excel 结构）
│   ├── management-policy.md      # 宣教管理办法（六章骨架 + 变更说明）
│   ├── event-plan.md             # 集中宣教活动实施方案
│   ├── event-summary.md          # 活动总结报告
│   ├── venue-standards.md        # 线下专区 / 线上专栏建设标准
│   ├── video-script.md           # 短视频脚本（情节 + 分镜）
│   ├── prompt-and-copy.md        # 风险提示文案 / 图像生成提示词
│   ├── evaluation-report.md      # 季度/年度效果评估报告
│   ├── data-ledger.md            # 宣教工作数据统计台账
│   └── case-collection.md        # 优秀宣教案例集
├── scripts/
│   └── campaign_metrics.py       # 活动数据汇总、分维度统计、同比对比（仅标准库）
└── assets/                       # 品牌图标源文件、PNG、渲染脚本与设计说明
    ├── icon.svg / logo-mark.svg / logo-horizontal.svg
    ├── avatar-512.png / logo-horizontal.png
    ├── render_icon.py
    └── README.md
```

## 使用示例

- "帮我制定 2026 年度金融教育宣传工作计划"（自动产出文字版 + 表格版）
- "起草一份《金融知识宣传教育管理办法》"
- "策划一个 3·15 宣传活动方案，要有五进入安排和舆情预案"
- "制定网点宣教专区建设标准"
- "写一个防范电信诈骗的短视频脚本，面向老年人"
- "生成一张反洗钱宣传海报的提示词"
- "出一份 2026Q3 宣教效果评估报告"
- "统计一下今年的宣教覆盖数据"（可调用 `scripts/campaign_metrics.py`）

## 安装使用

发布英文名（GitHub 与 SkillHub 统一）：`financial-literacy-education`

**SkillHub**：

```
skillhub install financial-literacy-education
```

**GitHub**：<https://github.com/openfcp/financial-literacy-education>（public，main 分支）。

```
git clone https://github.com/openfcp/financial-literacy-education.git
```

**本机用户级安装**：将本目录复制到 WorkBuddy 用户级技能目录，重启会话后直接用触发词调用。

```
~/.workbuddy/skills/financial-literacy-education/
```

**离线包**：`financial-literacy-education.zip`（纯 Skill 目录，不含 `.git`），图标使用根目录 `_icon.png`（512×512 PNG）。发布前确认仓库内不含本地绝对路径、临时数据与未脱敏案例。

**双端发布差异**：GitHub 仓库是完整资源源（含 PNG 位图、SVG 矢量与渲染脚本）。SkillHub 社区源对发布包有文件类型白名单，仅接收 Markdown、SVG 与 Python 文件，因此位图图标不随包上传，需在 SkillHub 网页端的技能设置里单独上传 `_icon.png`；新发布版本还需通过平台内容与安全审核后才会进入搜索索引并可被安装。

## 图标

深蓝 `#071789` + 纯白两色，沿用参考图的白色扁平剪影与负空间语言。图形为「翻开的书 + 带 ¥ 的圆币 + 三道知识传播线」：书=知识普及，币=金融。

| 文件 | 用途 |
|------|------|
| `_icon.png` | 技能图标（512×512，含中英文名称） |
| `assets/logo-mark.svg` / `avatar-512.png` | 纯图形版，头像 / favicon / 物料角标 |
| `assets/logo-horizontal.svg` / `.png` | 白底横版，README 页眉 / 文档抬头 |
| `assets/icon.svg` | 主图标矢量源文件 |

重新生成 PNG：`cd assets && python3 render_icon.py`（Python 3 + Pillow）。设计规范见 `assets/README.md`。

## 关联技能（金融消保系列）

- [消保审查](https://github.com/openfcp/consumer-protection-review)
- [投诉管理](https://github.com/openfcp/complaint-management)
- [消保检查](https://github.com/openfcp/consumer-protection-inspection)
- [消保评价](https://github.com/openfcp/consumer-protection-annual-evaluation)
- [合规销售](https://github.com/openfcp/compliance-sales)
- [金融消保专家](https://github.com/openfcp/consumer-protection-expert)

## 更新日志

- v1.0.0：初始版本。依据《教育宣传岗子Agent能力与职责说明书》实现四角色路由与链式编排；含 8 份作业规范、11 类交付物模板、活动数据统计脚本与蓝白品牌图标。
