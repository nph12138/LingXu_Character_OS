# -*- coding: utf-8 -*-
"""LingXu SYSTEM_LIBRARY V3 · 自动评分 / 撞脸检查 CLI

用法：
  python score_character.py --json ../export/XX_v3auto_2026-09-10.json   # 重算总分
  python score_character.py --dna "脸型=长方脸;眼型=狭长眼;鼻型=骨感鼻梁;下颌=宽下颌"  # 只做撞脸检查
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lingxu_lib as L

def clash_from_dna(dna_str):
    new = {}
    for part in dna_str.replace("；", ";").split(";"):
        if "=" in part:
            k, v = part.split("=", 1); new[k.strip()] = v.strip()
    existing = L._load("../04_DATABASE/face_index.csv")
    row = {"主脸型": new.get("脸型", ""), "眼型": new.get("眼型", ""),
           "鼻梁": new.get("鼻型", ""), "下颌": new.get("下颌", "")}
    return L.face_vs_existing(row, existing)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--dna")
    a = ap.parse_args()

    if a.dna:
        res = clash_from_dna(a.dna)
        print("撞脸检查（对全库 %d 人）：" % len(res))
        for r in res[:10]:
            flag = "撞脸(四项全同)" if r["hard"] else ("撞脸" if r["score"] >= 70 else ("需拉开" if r["score"] >= 55 else "通过"))
            print("  %5.1f%%  %-12s %s" % (r["score"], r["name"], flag))
        return

    if a.json:
        c = json.load(open(a.json, encoding="utf-8"))
        # 统一键：生成器 json 里 face 是 dict
        face = c.get("face", {})
        row = {"主脸型": face.get("主脸型", ""), "眼型": face.get("眼型", ""),
               "鼻梁": face.get("鼻梁", ""), "下颌": face.get("下颌", "")}
        clash = L.face_vs_existing(row, L._load("../04_DATABASE/face_index.csv"))
        s = L.score_character(c, clash)
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return

    ap.print_help()

if __name__ == "__main__":
    main()
