# -*- coding: utf-8 -*-
"""LingXu Character OS · V3 生成引擎

用法：
  python generate_character.py --brief "设计一个25岁土属性镇墟司女性外勤，性格野性但可靠"
  python generate_character.py --brief "..." --seed 7 --export ../export

流程（对应 10_RANDOM_ENGINE 的 V3 版）：
  解析 brief → 选原型 → 抽 Face DNA → 个性/身体/发型/服装/材质/能力/武器/领域
  → 撞脸检查（全库硬撞则重抽）→ 自动评分 → 输出角色卡（可直接进 01_CHARACTERS/）
"""
import os, re, sys, json, random, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lingxu_lib as L

ATTR = ["金", "木", "水", "火", "土", "电", "雷"]
SURNAME = ["陆", "沈", "顾", "裴", "谢", "商", "宋", "黎", "韶", "裴", "钟离", "上官", "闻", "越", "萧", "凌", "桑", "容"]
GIVEN = ["烬", "岚", "珩", "砚", "岐", "岑", "衍", "烛", "砚", "霜", "樾", "巡", "砺", "铎", "澈", "笺", "烬", "黎", "野", "岑"]

def parse_brief(brief, lib):
    b = brief or ""
    out = {}
    m = re.search(r"(\d{1,3})\s*岁", b)
    out["age"] = int(m.group(1)) if m else random.choice([18, 20, 22, 24, 25, 26, 28, 30, 32, 35, 38, 42, 45])
    if re.search(r"女|少女|女性|姑娘|女子", b): out["gender"] = "女"
    elif re.search(r"男|少年|男性|男子", b): out["gender"] = "男"
    else: out["gender"] = random.choice(["男", "女"])
    out["attribute"] = next((a for a in ["电", "雷", "金", "木", "水", "火", "土"] if a in b), random.choice(ATTR[:5]))
    out["faction"] = next((f for f in L.FACTION_LIST if f in b), "—")
    ps = [p for p in L.PERSONALITY_LIST if p in b]
    out["personality_list"] = ps
    out["raw"] = b
    return out

def infer_archetype(info, lib):
    name = next((a["名称"] for a in lib["archetype"] if a["名称"] in info["raw"]), None)
    if name:
        return name
    tone = {L.TONE.get(p) for p in info["personality_list"] if p}
    cand = []
    for a in lib["archetype"]:
        nm = a["名称"]
        if nm == "少年兵" and info["age"] >= 22:   # 年龄不符则排除
            continue
        sc = len(tone & set(L.ARCH_TONE.get(nm, []))) * 2 + (1 if info["faction"] in L.ARCH_FACTION.get(nm, []) else 0)
        cand.append((sc, nm))
    cand.sort(reverse=True)
    return cand[0][1] if cand else "游侠"

VIS_TRAIT = ["收紧动作幅度与表情", "稳定眼神", "放松眼尾与嘴角", "锐利眼型", "强烈轮廓", "结构不对称",
             "材质温润", "非人平静", "反差配色", "破损细节", "简洁剪影", "层叠结构", "高洁材质", "低重心体态"]

def compose_visual(a, b, c):
    return f"{a}→{random.choice(VIS_TRAIT)}；{b}→{random.choice(VIS_TRAIT)}；{c}→{random.choice(VIS_TRAIT)}"

def gen_name(info):
    return random.choice(SURNAME) + random.choice(GIVEN)

def draw_face(lib, info):
    return random.choice(lib["face"])

def resample_face(lib, info, existing, max_try=400):
    """抽到不硬撞、且与全库最高相似度 < 55% 的 Face DNA。"""
    best = None
    for _ in range(max_try):
        f = draw_face(lib, info)
        clash = L.face_vs_existing(f, existing)
        top = clash[0] if clash else {"score": 0, "hard": False}
        if not top["hard"] and top["score"] < 55:
            return f, clash
        if best is None or (clash[0]["score"] < best[1][0]["score"]):
            best = (f, clash)
    return best

def build(brief, seed=None):
    if seed is not None:
        random.seed(seed)
    lib = L.load_all()
    info = parse_brief(brief, lib)
    info["archetype"] = infer_archetype(info, lib)

    face, clash = resample_face(lib, info, lib["existing"])
    body_pool = [b for b in lib["body"] if b["性别"] == info["gender"]] or lib["body"]
    body = random.choice(body_pool)
    hair = random.choice(lib["hair"])
    cost_pool = [c for c in lib["costume"] if info["faction"] != "—" and c["阵营"] == info["faction"]] or lib["costume"]
    costume = random.choice(cost_pool)
    material = random.choice(lib["material"])
    ability = random.choice(lib["ability"])
    weapon = random.choice(lib["weapon"])
    domain = random.choice(lib["domain"])
    if info["personality_list"]:
        p = dict(random.choice(lib["personality"]))
        pl = info["personality_list"]
        p["第一眼"] = pl[0]
        if len(pl) > 1: p["第二眼"] = pl[1]
        if len(pl) > 2: p["第三眼"] = pl[2]
        p["关键词串"] = "、".join([p["第一眼"], p["第二眼"], p["第三眼"]])
        p["视觉化要点"] = compose_visual(p["第一眼"], p["第二眼"], p["第三眼"])
    else:
        p = random.choice(lib["personality"])
    arch = next((a for a in lib["archetype"] if a["名称"] == info["archetype"]), lib["archetype"][0])

    c = {
        "name": gen_name(info), "age": info["age"], "gender": info["gender"],
        "faction": info["faction"], "attribute": info["attribute"], "archetype": info["archetype"],
        "personality": p, "personality_list": info["personality_list"],
        "face": face, "body": body, "hair": hair, "costume": costume,
        "material": material, "ability": ability, "weapon": weapon, "domain": domain,
        "arch_row": arch, "brief": brief,
    }
    c["score"] = L.score_character(c, clash)
    c["clash"] = clash[:5]
    c["date"] = datetime.date.today().isoformat()
    return c

def to_card(c):
    f = c["face"]; p = c["personality"]
    return f"""# {c['name']}　`v3_auto`　 Face DNA `{f['face_id']}`

> 由 SYSTEM_LIBRARY V3 生成引擎产出（@ {c['date']}）｜评分 **{c['score']['total']}（{c['score']['grade']}）**
> brief：{c['brief'] or '（无）'}
> 状态：**未定稿**——需人工复核锚点后锁 v001 再进 `01_CHARACTERS/`。

## 基础信息
- 姓名：{c['name']}
- 性别：{c['gender']}　年龄：{c['age']}
- 阵营：{c['faction']}　属性：{c['attribute']}
- 原型：{c['archetype']}（{c['arch_row']['核心']}）

## 核心气质
- 第一眼：{p['第一眼']}　第二眼：{p['第二眼']}　第三眼：{p['第三眼']}
- 视觉化：{p['视觉化要点']}

## Face DNA（候选）
- 脸型：{f['主脸型']}（{f['辅变化']}）
- 骨相：{f['额头']} / {f['眉骨']} / {f['眼窝']} / {f['颧骨']} / {f['面颊']} / {f['下颌']}
- 眼：{f['眼型']}·{f['眼尾']}·{f['眼距']}·{f['虹膜']}
- 鼻：{f['鼻根']} / {f['鼻梁']} / {f['鼻头']}
- 唇：{f['唇型']}·{f['嘴角']}
- 特殊标志：{f['特殊标志']}

## 身体 / 发型
- 身体：{c['body']['描述']}
- 发型：{c['hair']['描述']}

## 服装
- {c['costume']['描述']}
- 主要材质：{c['material']['名称']}（{c['material']['类别']}｜{c['material']['历史感']}）

## 能力机制
- {c['ability']['一句话']}

## 武器
- {c['weapon']['描述']}

## 领域（如有）
- {c['domain']['名称']}：{c['domain']['规则']}（触发：{c['domain']['触发']}｜范围：{c['domain']['范围']}）
  - 限制：{c['domain']['限制']}｜代价：{c['domain']['代价']}｜破坏方式：{c['domain']['破坏方式']}

## 自动评分
| 项 | 分 |
| --- | --- |
| 新颖度（对全库） | {c['score']['novelty']} |
| 一致性（原型↔气质↔阵营） | {c['score']['coherence']} |
| 辨识度 | {c['score']['distinctiveness']} |
| 完整度 | {c['score']['completeness']} |
| **总分** | **{c['score']['total']}（{c['score']['grade']}）** |

## 撞脸检查（Top5）
| 角色 | 相似度 | 硬撞 |
| --- | --- | --- |
""" + "\n".join(f"| {x['name']} | {x['score']}% | {'是' if x['hard'] else '否'} |" for x in c["clash"]) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", default="设计一个25岁土属性镇墟司女性外勤，性格野性但可靠")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--export", default=None, help="导出目录（默认 ./export）")
    a = ap.parse_args()
    c = build(a.brief, a.seed)
    card = to_card(c)
    outdir = a.export or os.path.join(L.HERE, "..", "export")
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    base = f"{c['name']}_v3auto_{c['date']}"
    with open(os.path.join(outdir, base + ".md"), "w", encoding="utf-8", newline="") as fp:
        fp.write(card)
    with open(os.path.join(outdir, base + ".json"), "w", encoding="utf-8", newline="") as fp:
        json.dump({k: v for k, v in c.items()}, fp, ensure_ascii=False, indent=2)
    # 控制台摘要
    print(f"★ 生成角色：{c['name']}  {c['gender']}/{c['age']}  {c['faction']}·{c['attribute']}  原型:{c['archetype']}")
    print(f"  气质：{c['personality']['第一眼']} / {c['personality']['第二眼']} / {c['personality']['第三眼']}")
    print(f"  Face：{c['face']['主脸型']}（{c['face']['辅变化']}） · {c['face']['眼型']} · {c['face']['下颌']} · {c['face']['特殊标志']}")
    print(f"  评分：{c['score']['total']}（{c['score']['grade']}）  新颖 {c['score']['novelty']} / 一致 {c['score']['coherence']} / 辨识 {c['score']['distinctiveness']}")
    print(f"  撞脸Top1：{c['score']['clash_top']['name']} {c['score']['clash_top']['score']}%  硬撞={c['score']['clash_top']['hard']}")
    print(f"  导出：{os.path.join(outdir, base)}.md")

if __name__ == "__main__":
    main()
