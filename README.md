# LingXu_Character_OS ·《灵墟纪》角色操作系统

> 给 AI、生图、视频生成共用的**角色记忆库 / 虚拟美术资产库**。
> 目标只有一句：**同一世界，不同的人。**

## 它解决三件事

1. **身份一致** — 任何模型动手前，先读本库的 `face_dna.md` / `identity_anchor.md`，而不是重新猜一张脸。
2. **防撞脸** — 新角色设计前，先查 `04_DATABASE/face_index`，与全库做 Face DNA 相似度比对。
3. **资产可追溯** — 图片按 `<拼音>_<类型>_v00n` 命名；每次生成进 `05_GENERATION_LOG`，失败版本进 `rejected_designs/`。

## 目录地图

```
LingXu_Character_OS/
├── README.md
├── 00_PROJECT_RULES/          规则层（生图前必读）
│   ├── visual_style.md        72/28 统一 CG 风格
│   ├── character_rules.md     防撞脸规则 / Face DNA 制度
│   ├── image_standard.md      六类图片规范 + 命名与版本规范
│   └── prompt_template.md     生图提示词模板
├── 01_CHARACTERS/             角色层（一角色一目录）
│   └── _TEMPLATE/             复制改名即新建角色
├── 02_FACTION/                阵营层
├── 03_WORLD/                  世界层：地图 / 场景 / 建筑
├── 04_DATABASE/               索引层 ★ 防撞脸核心
│   ├── face_index.xlsx        Face DNA 总表（人看）
│   ├── face_index.csv         同数据纯文本（git diff / 脚本看）
│   ├── character_compare.md   两两对比结论
│   └── similarity_check.md    AI 防撞脸 SOP
├── 05_GENERATION_LOG/         生成记录
│   └── rejected_designs/      废案存档（含失败原因）
└── tools/                      防撞脸相似度检查脚本
```

## 三条强制流程

### 新建角色
1. 复制 `01_CHARACTERS/_TEMPLATE` → `01_CHARACTERS/<角色名>`。
2. 填 `character.md`（基础信息 / 气质 / 定位）→ `face_dna.md`（12 维度）→ `identity_anchor.md`。
3. 跑 `tools/check_face_similarity.py` 与 `face_index.csv` 比对；**相似度 ≥70% 必须改维度**。
4. 更新 `04_DATABASE/face_index`（xlsx 与 csv 同步）。
5. 生成「图1 身份标准照」，定稿后锁 **Face DNA v001**，此后换装换场景都不许改脸。

### 生成图片
读 `00_PROJECT_RULES/image_standard.md` → 用该角色 `prompts/` 里的模板 → 产物按命名规范落盘 → 写 `05_GENERATION_LOG/<日期>_<角色>.md`。

### 换装 / 换场景 / 换时期
Face Identity 不动，只改 Costume / Scene / State。改脸 = 换人，见 `character_rules.md`。

## 与旧资产的关系

- 旧资产：Obsidian 库内 `灵墟纪/1金 … 10复苏体/*.md`，124 张角色卡（图片本体在 Mac 的「图片集中」，Windows 端暂无原图）。
- 本库：长期维护的规范库 + 索引。旧卡按 `01_CHARACTERS/_TEMPLATE` 逐步迁移，迁移一个就在 `face_index` 记一行。
- 迁移待办见 `01_CHARACTERS/README.md` 末尾。

## 注意事项

- 本目录位于坚果云同步文件夹内，**`.git` 会被同步**。建议：提交前确认同步已完成；或在坚果云客户端中把 `.git` 设为不同步。
- 大文件走 Git LFS：首次克隆后执行 `git lfs install && git lfs pull`。
- 存储策略：Git 里只放 ≤512px 预览图、md、prompt 与 metadata；4K 图与视频帧放 LFS。
