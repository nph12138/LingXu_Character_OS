# 01 · 角色层

## 目录约定

```
01_CHARACTERS/<角色名>/
├── character.md           角色档案（基础信息 / 气质 / 定位 / 锚点摘要）
├── face_dna.md            Face DNA 十二维度（最重要，锁后不可改）
├── identity_anchor.md     永久身份锚点：Face / Hair / Body / Costume
├── 01_identity/           图1 身份标准照
├── 02_design/             图2 人物设计图（front / side / back）
├── 03_video_asset/        视频角色资产图
├── 04_hero_art/           Hero Key Art
├── 05_hero_frame/         视频 Hero Frame
├── 06_effect/             战斗特效图（按需）
└── prompts/               identity_prompt.txt / hero_prompt.txt / video_prompt.txt
```

- 目录名用**中文角色名**（人读），文件名用**拼音 ID**（机读），两者在 `character.md` 顶部同时写清。
- 每个图片目录里放一份 `README.md`（命名与版本规范），由 `_TEMPLATE` 复制而来。
- 变体角色（恶灵形态 / 少年时期）**单开目录**：`疏岚_恶灵时期/`，Face Identity 继承主卡并标注差异。

## 新建角色步骤

1. `cp -r _TEMPLATE <角色名>`
2. 改 `character.md` 顶部：中文名、拼音 ID、目录名。
3. 填 `face_dna.md` 十二维度（从 `要求.md` 第五、六章词典取值）。
4. 跑 `tools/check_face_similarity.py` → 相似度 <55% 才继续。
5. 在 `04_DATABASE/face_index.xlsx` 与 `.csv` 各加一行。
6. 生成 `01_identity/`，定稿后锁 Face DNA v001，写 `05_GENERATION_LOG/<日期>_<角色>.md`。

## 迁移待办（旧 124 张卡）

旧卡在 `灵墟纪/1金 … 10复苏体/*.md`，共 124 张，已统一为六槽位结构。迁移按批次推进，每批做完更新 `face_index`：

- [ ] 批次 1：镇墟司 + 少年团（天衡、昭璃、昭衡、游峥、砺钧、钟离澈、疏岚、烬离、星澜 …）
- [ ] 批次 2：十二墟魄（不坏傀、冥骑、幽刹、冷弧月、绯轮、铄影、烬王、烬蛾 …）
- [ ] 批次 3：灰区与人类
- [ ] 批次 4：复苏体与血兽
- [ ] 批次 5：低阶恶灵

迁移规则：只搬文字与锚点，图片沿用原文件名放进对应目录并补 `_v001` 版本标记。
