# -*- coding: utf-8 -*-
"""Face DNA 相似度检查：新角色 vs 全库。

用法：
  python tools/check_face_similarity.py --name 新角色 --dna "脸型=窄鹅蛋脸;眼型=长杏眼;鼻型=高直鼻;下颌=窄下颌"
  python tools/check_face_similarity.py --name 新角色 --file path/to/new_face_dna.md

判定：
  >=70% 撞脸，必须改；55-70% 再拉开两个维度；<55% 通过。
  脸型+眼型+鼻型+下颌 四项全同 -> 直接判定撞脸。
"""
import argparse, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "04_DATABASE", "face_index.csv")

WEIGHTS = {"脸型": 3, "眼型": 3, "鼻型": 2, "下颌": 2, "三庭": 1,
           "眉形": 1, "唇型": 1, "个性标志": 1}
HARD_KEYS = ["脸型", "眼型", "鼻型", "下颌"]


def parse_dna(text):
    d = {}
    for part in re.split(r"[;；\n]", text):
        if "=" in part:
            k, v = part.split("=", 1)
        elif "：" in part:
            k, v = part.split("：", 1)
        else:
            continue
        d[k.strip()] = v.strip()
    return d


def sim(a, b):
    """维度内相似度：相同=1，有一方缺失=0.5，有交集词=0.7，否则=0。"""
    if not a or not b:
        return 0.5
    if a == b:
        return 1.0
    sa = set(re.findall(r"[\u4e00-\u9fff]+", a))
    sb = set(re.findall(r"[\u4e00-\u9fff]+", b))
    if sa & sb:
        return 0.7
    return 0.0


def score(new, row):
    total = wsum = 0.0
    for k, w in WEIGHTS.items():
        v_new = new.get(k)
        v_row = row.get(k) or (row.get(k + "（合并）") if k + "（合并）" in row else "")
        if v_new is None and not v_row:
            continue
        total += w * sim(v_new or "", v_row or "")
        wsum += w
    return (total / wsum * 100) if wsum else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--dna", help='"脸型=...;眼型=...;鼻型=...;下颌=..."')
    ap.add_argument("--file", help="新角色 face_dna.md 路径")
    args = ap.parse_args()

    if args.dna:
        new = parse_dna(args.dna)
    elif args.file:
        new = parse_dna(open(args.file, encoding="utf-8").read())
    else:
        sys.exit("需要 --dna 或 --file")

    path = os.path.normpath(CSV_PATH)
    if not os.path.exists(path):
        sys.exit("找不到 face_index.csv：%s" % path)
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))

    results = []
    for r in rows:
        if r.get("角色") == args.name:
            continue
        s = score(new, r)
        hard = all(str(new.get(k, "")).strip() and str(new.get(k, "")).strip() == str(r.get(k, "") or "").strip()
                   for k in HARD_KEYS)
        results.append((s, hard, r.get("角色", "?"), r.get("备注", "")))
    results.sort(reverse=True, key=lambda x: (x[1], x[0]))

    print("新角色：%s" % args.name)
    print("比对角色数：%d\n" % len(results))
    for s, hard, name, note in results[:10]:
        flag = "撞脸(四项全同)" if hard else ("撞脸" if s >= 70 else ("需拉开" if s >= 55 else "通过"))
        print("  %5.1f%%  %-12s %s %s" % (s, name, flag, ("示例数据" if "示例" in (note or "") else "")))
    if not results:
        print("  库里还没有可比对的角色。")


if __name__ == "__main__":
    main()
