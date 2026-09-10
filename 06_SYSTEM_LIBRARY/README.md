# LingXu SYSTEM_LIBRARY V3 · 角色生成数据库（生产版）

> 《灵墟纪》公共角色生成数据库。目标：**输入一句身份描述，自动产出一个不撞脸、有独立脸/身体/能力机制的角色，可直接进入 Character OS。**
>
> 核心原则（延续 V2）：**随机生成真实身份，而不是随机生成漂亮模板。**

## 一句话用法

```bash
cd 06_SYSTEM_LIBRARY/engine
python generate_character.py --brief "设计一个25岁土属性镇墟司女性外勤，性格野性但可靠"
```

输出：控制台摘要 + `export/<姓名>_v3auto_<日期>.md`（角色卡，可直接改名进 `01_CHARACTERS/`）+ 同名 `.json`。

## 库容量

| 库 | 文件 | 条数 |
| --- | --- | --- |
| Face DNA（完整脸） | `01_FACE_DNA/face_dna_5000.csv` | **5200** |
| 气质组合 | `02_PERSONALITY/personality_1000.csv` | **1100** |
| 身体模板 | `03_BODY/body_500.csv` | **560** |
| 发型 | `04_HAIR/hair.csv` | **360** |
| 服装结构 | `05_COSTUME/costume_1000.csv` | **1080** |
| 材质 | `06_MATERIAL/material.csv` | 15（含 6 维属性） |
| 能力机制 | `07_ABILITY/ability_500.csv` | **560** |
| 领域规则 | `08_DOMAIN/domain_300.csv` | **320** |
| 武器机制 | `09_WEAPON/weapon_500.csv` | **560** |
| 角色原型 | `10_ARCHETYPE/archetype.csv` | 15 |
| 原子词表 | `01_FACE_DNA/ATOMS_*.csv`、`02_PERSONALITY/ATOMS.csv` | — |

## 目录

```
06_SYSTEM_LIBRARY/
├── 00_INDEX/STATS.md            库容量统计
├── 01_FACE_DNA/                 Face DNA 库 + 原子词表 + 组合规则
├── 02_PERSONALITY/              气质组合 + 气质原子
├── 03_BODY/                     身体模板
├── 04_HAIR/                     发型
├── 05_COSTUME/                  服装结构
├── 06_MATERIAL/                 材质（颜色/重量/纹理/磨损/反射/历史感）
├── 07_ABILITY/                  能力机制 + 机制合成规则
├── 08_DOMAIN/                   领域规则（触发/范围/规则/限制/优势/代价/破坏）
├── 09_WEAPON/                   武器机制
├── 10_ARCHETYPE/                角色原型
├── 11_RULES/                    生成流程 / 评分系统 / 防撞脸规则
├── engine/                      生成引擎（Python，仅标准库）
│   ├── lingxu_lib.py            加载 / 撞脸检查 / 评分核心
│   ├── generate_character.py    一句话 → 角色卡
│   └── score_character.py       评分 / 撞脸检查 CLI
└── export/                      生成产物
```

## 生成流程（V3）

`解析 brief → 选原型 → 抽 Face DNA → 撞脸检查(硬撞重抽) → 气质/身体/发型/服装/材质/能力/武器/领域 → 自动评分 → 导出角色卡`

详见 `11_RULES/generation_pipeline.md`。

## 评分与防撞脸

- 总分 = 新颖度 35% + 一致性 25% + 辨识度 20% + 完整度 20%，等级 S/A/B/C/D。
- 防撞脸：与全库比，**脸型+眼型+鼻型+下颌 四项全同 = 硬撞（重抽）**；≥70% 撞脸需改；55–70% 再拉开两维；<55% 通过。
- 详见 `11_RULES/scoring_system.md`、`11_RULES/anti_clash_rules.md`。

## 与 Character OS 的关系

本库是**生成侧**；`01_CHARACTERS/` 是**定稿侧**。流程：

> 本库生成 → 人工复核（脸/身体/能力锚点）→ 锁定 Face DNA v001 → 写入 `01_CHARACTERS/<角色>/` + `04_DATABASE/face_index`

> 注意：库内数据为**候选生成素材**，不是已定稿角色。定稿才算进入世界观。
