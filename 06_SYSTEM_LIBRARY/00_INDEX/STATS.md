# 库容量统计

| 文件 | 条数 |
| --- | --- |
| `01_FACE_DNA/ATOMS_eye.csv` | 28 |
| `01_FACE_DNA/ATOMS_face_shape.csv` | 42 |
| `01_FACE_DNA/ATOMS_facial_structure.csv` | 8 |
| `01_FACE_DNA/ATOMS_mark.csv` | 24 |
| `01_FACE_DNA/ATOMS_nose_mouth.csv` | 20 |
| `01_FACE_DNA/face_dna_5000.csv` | 5200 |
| `02_PERSONALITY/ATOMS.csv` | 49 |
| `02_PERSONALITY/personality_1000.csv` | 1100 |
| `03_BODY/body_500.csv` | 560 |
| `04_HAIR/hair.csv` | 360 |
| `05_COSTUME/costume_1000.csv` | 1080 |
| `06_MATERIAL/material.csv` | 15 |
| `07_ABILITY/ability_500.csv` | 560 |
| `08_DOMAIN/domain_300.csv` | 320 |
| `09_WEAPON/weapon_500.csv` | 560 |
| `10_ARCHETYPE/archetype.csv` | 15 |

**合计 9962 条数据行。**

## 达成情况（对 V3 目标）

| 目标 | 要求 | 实际 |
| --- | --- | --- |
| Face DNA | 5000+ | **5200** ✅ |
| 气质组合 | 1000+ | **1100** ✅ |
| 身体模板 | 500+ | **560** ✅ |
| 服装结构 | 1000+ | **1080** ✅ |
| 武器机制 | 500+ | **560** ✅ |
| 能力机制 | 500+ | **560** ✅ |
| 领域规则 | 300+ | **320** ✅ |
| 眼鼻嘴组合规则 | — | `01_FACE_DNA/COMBINATION_RULES.md` ✅ |
| 自动评分系统 | — | `11_RULES/scoring_system.md` + `engine/score_character.py` ✅ |

> 重新生成数据表：在工作区运行 `python build_v3.py`（固定随机种子，可复现）。
