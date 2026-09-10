# -*- coding: utf-8 -*-
"""LingXu SYSTEM_LIBRARY V3 · 核心库（加载 / 撞脸检查 / 评分）。

供 generate_character.py 与 score_character.py 复用。
"""
import os, csv, random, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.dirname(HERE)                 # 06_SYSTEM_LIBRARY
OS = os.path.dirname(LIB)                   # LingXu_Character_OS

FACTION_LIST = ["镇墟司", "宗门", "流亡者", "贵族", "战士团", "商贾", "医者", "隐世",
                "恶灵", "复苏体", "灰区", "王庭", "游侠", "学宫"]
PERSONALITY_LIST = ["清冷", "聪慧", "柔软", "野性", "可靠", "危险", "温柔", "疯狂", "神性", "妖异",
 "沉稳", "孤傲", "温润", "凌厉", "散漫", "坚毅", "天真", "沧桑", "阴郁", "明亮", "克己", "放纵",
 "疏离", "亲和", "神秘", "直率", "隐忍", "张扬", "克制", "暴烈", "悲悯", "冷酷", "慵懒", "警觉",
 "虔诚", "叛逆", "温雅", "狠戾", "通透", "执拗", "从容", "局促", "高贵", "市井", "病弱", "强健",
 "沉静", "躁动", "坦然"]

def _load(rel):
    p = os.path.join(LIB, rel)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def load_all():
    return {
        "face": _load("01_FACE_DNA/face_dna_5000.csv"),
        "personality": _load("02_PERSONALITY/personality_1000.csv"),
        "body": _load("03_BODY/body_500.csv"),
        "hair": _load("04_HAIR/hair.csv"),
        "costume": _load("05_COSTUME/costume_1000.csv"),
        "material": _load("06_MATERIAL/material.csv"),
        "ability": _load("07_ABILITY/ability_500.csv"),
        "domain": _load("08_DOMAIN/domain_300.csv"),
        "weapon": _load("09_WEAPON/weapon_500.csv"),
        "archetype": _load("10_ARCHETYPE/archetype.csv"),
        "existing": _load("../04_DATABASE/face_index.csv"),
    }

# ---------------- 相似度 ----------------
def _norm(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s or "")

def dim_sim(a, b):
    a, b = _norm(a), _norm(b)
    if not a or not b:
        return 0.5
    if a == b:
        return 1.0
    # 短语包含（如 长方脸 ⊂ 长方脸独立水系冷感骨相）
    if a in b or b in a:
        return 0.9
    sa, sb = set(re.findall(r"[\u4e00-\u9fff]{2,}", a)), set(re.findall(r"[\u4e00-\u9fff]{2,}", b))
    # 双字滑窗交集
    ga = {a[i:i+2] for i in range(len(a)-1)}
    gb = {b[i:i+2] for i in range(len(b)-1)}
    if ga & gb:
        return 0.7
    return 0.0

W = {"脸型": 3, "眼型": 3, "鼻型": 2, "下颌": 2}
HARD = ["脸型", "眼型", "鼻型", "下颌"]

def face_vs_existing(face_row, existing):
    """返回按相似度降序的 [(score, name, hard)]。"""
    new = {"脸型": face_row.get("主脸型", ""), "眼型": face_row.get("眼型", ""),
           "鼻型": face_row.get("鼻梁", ""), "下颌": face_row.get("下颌", "")}
    out = []
    for r in existing:
        tot = wsum = 0.0
        for k, w in W.items():
            tot += w * dim_sim(new[k], r.get(k, ""))
            wsum += w
        s = tot / wsum * 100 if wsum else 0.0
        hard = all(new[k] and dim_sim(new[k], r.get(k, "")) >= 1.0 for k in HARD)
        out.append({"score": round(s, 1), "name": r.get("角色", "?"), "hard": hard})
    out.sort(key=lambda x: (x["hard"], x["score"]), reverse=True)
    return out

# ---------------- 评分 ----------------
TONE = {
    "野性": "wild", "暴烈": "wild", "张扬": "wild", "强健": "wild", "躁动": "wild", "放纵": "wild",
    "可靠": "steadfast", "坚毅": "steadfast", "沉稳": "steadfast", "从容": "steadfast", "克己": "steadfast",
    "清冷": "cold", "孤傲": "cold", "疏离": "cold", "冷酷": "cold", "沉静": "cold", "隐忍": "cold",
    "温柔": "warm", "柔软": "warm", "温润": "warm", "亲和": "warm", "悲悯": "warm", "温雅": "warm",
    "危险": "danger", "狠戾": "danger", "妖异": "danger", "凌厉": "danger", "疯狂": "danger", "神性": "clever",
    "聪慧": "clever", "神秘": "clever", "通透": "clever", "警觉": "clever",
}
ARCH_TONE = {
    "英雄": ["steadfast"], "守护者": ["steadfast", "warm"], "猎杀者": ["danger", "cold"],
    "谋略者": ["clever", "cold"], "狂战士": ["wild", "danger"], "妖异者": ["danger"],
    "游侠": ["wild"], "医者": ["warm"], "隐修": ["cold", "clever"], "反叛者": ["wild", "danger"],
    "匠人": ["steadfast"], "囚徒": ["danger", "cold"], "祭司": ["cold"], "少年兵": ["wild", "steadfast"],
    "归乡者": ["warm", "cold"],
}
ARCH_FACTION = {
    "英雄": ["镇墟司", "宗门"], "守护者": ["镇墟司", "王庭"], "猎杀者": ["灰区", "游侠"],
    "谋略者": ["学宫", "王庭"], "狂战士": ["战士团", "恶灵"], "妖异者": ["恶灵", "复苏体"],
    "游侠": ["灰区", "游侠"], "医者": ["宗门", "学宫"], "隐修": ["隐世", "宗门"],
    "反叛者": ["灰区", "流亡者"], "匠人": ["商贾", "宗门"], "囚徒": ["流亡者", "灰区"],
    "祭司": ["宗门", "王庭"], "少年兵": ["镇墟司", "战士团"], "归乡者": ["灰区", "隐世"],
}

def score_character(c, clash):
    """c: 生成字典；clash: face_vs_existing 结果。返回 0-100 总分与分项。"""
    top = clash[0] if clash else {"score": 0, "hard": False, "name": "—"}
    # 1) 新颖度：与全库最高相似度越低越好
    novelty = max(0.0, 100.0 - top["score"])
    if top.get("hard"):
        novelty = 0.0
    # 2) 一致性：原型-气质 与 原型-阵营
    at = ARCH_TONE.get(c["archetype"], [])
    tones = {TONE.get(p, "other") for p in c["personality_list"]}
    tone_hit = 1.0 if (tones & set(at)) else 0.4
    fac_hit = 1.0 if c["faction"] in ARCH_FACTION.get(c["archetype"], []) else 0.6
    coherence = (tone_hit * 0.6 + fac_hit * 0.4) * 100
    # 3) 辨识度：有标志 + 非鹅蛋主脸 + 服装/武器机制非空
    dist = 40.0
    if c["face"].get("特殊标志", "无标志") != "无标志":
        dist += 25
    if "鹅蛋" not in c["face"].get("主脸型", ""):
        dist += 20
    if c["weapon"].get("机制") and c["ability"].get("机制"):
        dist += 15
    dist = min(100.0, dist)
    # 4) 完整度
    fields = ["age", "gender", "faction", "attribute", "archetype"]
    filled = sum(1 for k in fields if c.get(k) not in (None, "", "—"))
    complete = filled / len(fields) * 100
    total = novelty * 0.35 + coherence * 0.25 + dist * 0.20 + complete * 0.20
    grade = "S" if total >= 88 else "A" if total >= 78 else "B" if total >= 68 else "C" if total >= 55 else "D"
    return {
        "total": round(total, 1), "grade": grade,
        "novelty": round(novelty, 1), "coherence": round(coherence, 1),
        "distinctiveness": round(dist, 1), "completeness": round(complete, 1),
        "clash_top": top,
    }
