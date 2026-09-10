# -*- coding: utf-8 -*-
"""
LingXu SYSTEM_LIBRARY V3 生成器
产出：Face DNA 5200 / 气质 1100 / 身体 560 / 服装 1080 / 武器 560 / 能力 560 / 领域 320
+ 组合规则 + 评分系统 + 生成引擎 的「大数据表」部分。
固定随机种子，可复现。
输出目录：<repo>/06_SYSTEM_LIBRARY
"""
import os, csv, random, json

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 06_SYSTEM_LIBRARY
random.seed(20260910)

def W(path, text):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text.replace("\r\n", "\n"))

def WCSV(path, headers, rows):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(headers)
        w.writerows(rows)

def pick(lst, n):
    return [random.choice(lst) for _ in range(n)]

# ============================================================ 词表
FACE_MAIN = [
 "长鹅蛋脸","短鹅蛋脸","宽鹅蛋脸","窄鹅蛋脸","方鹅蛋脸","鹅蛋偏方","鹅蛋偏菱","鹅蛋偏心形",
 "长方脸","短方脸","宽方脸","窄方脸","柔和方脸","骨感方脸","成熟方脸","幼态方脸",
 "圆脸","短圆脸","长圆脸","圆方脸","幼态圆脸","清瘦圆脸",
 "标准菱形","长菱形","宽菱形","骨感菱形","柔和菱形",
 "倒三角脸","倒梯形脸","正梯形脸","梨形脸","上宽下窄脸","上窄下宽脸",
 "颧部展开脸","下颌突出脸","骨感窄脸","肉感短脸","双颌匀称脸",
 "心形脸","长心形脸","宽心形脸","方菱过渡脸"]
EGG = {"长鹅蛋脸","短鹅蛋脸","宽鹅蛋脸","窄鹅蛋脸","方鹅蛋脸","鹅蛋偏方","鹅蛋偏菱","鹅蛋偏心形"}
FACE_AUX = [
 "偏锐收窄","偏柔圆润","中轴微长","中轴收紧","上庭展开","上庭收窄","中庭展宽","中庭拉长",
 "下庭收窄","下庭加重","颧部微收","颧部外扩","下颌线清晰化","下颌线柔化","颌角弱化","颌角强调",
 "面中平缓","面中立体化","骨点外显","骨点内敛","颊部略凹","颊部饱满","颈部线条延长","颈部线条收短"]
FOREHEAD = ["高额","低额","宽额","窄额","饱满额","平直额","微凸额","骨感额"]
BROW_BONE = ["高眉骨","低眉骨","厚眉骨","薄眉骨","外侧突出眉骨","内侧突出眉骨","压迫感眉骨","柔和眉骨"]
SOCKET = ["深眼窝","浅眼窝","宽浅眼窝","窄深眼窝","眼下骨感","眼下饱满","中度眼窝"]
CHEEKBONE = ["高颧骨","低颧骨","宽颧骨","窄颧骨","外扩颧骨","柔和颧骨"]
CHEEK = ["饱满面颊","薄面颊","轻凹面颊","成熟收紧面颊","幼态柔软面颊"]
JAW = ["宽下颌","窄下颌","方下颌","圆方下颌","骨感下颌","柔和下颌","明显下颌角","收敛下颌"]
EYE_TYPE = ["长杏眼","短杏眼","窄杏眼","宽杏眼","丹凤眼","平凤眼","瑞凤眼","桃花眼","柳叶眼",
 "狐狸系眼","猫系眼","狭长眼","圆长眼","下垂眼","冷感眼","疲惫眼","少年圆眼","成熟长眼",
 "鹰隼眼","狼系眼","蛇系眼","鹿系眼","鹤系眼","短圆杏眼","狭长瑞凤眼","上扬凤眼","平直杏眼","半睁懒眼"]
EYE_TAIL = ["眼尾微挑","眼尾明显挑","眼尾平直","眼尾下压","眼尾下沉","眼尾延展"]
EYE_DIST = ["宽眼距","标准眼距","窄眼距"]
IRIS = ["深色瞳","浅褐瞳","灰蓝瞳","琥珀瞳","墨玉瞳","异色瞳","环状虹膜","碎裂虹膜","星点虹膜","淡金瞳"]
NOSE_ROOT = ["高鼻根","中高鼻根","中鼻根","低鼻根","宽鼻根","窄鼻根"]
NOSE_BRIDGE = ["高直鼻梁","中直鼻梁","宽骨鼻梁","柔和鼻梁","微弧鼻梁","轻鹰钩鼻梁","轻微偏左鼻梁","轻微偏右鼻梁"]
NOSE_TIP = ["小圆鼻头","方圆鼻头","微钝鼻头","骨感鼻头","肉感鼻头","轻翘鼻头","下压鼻头","窄翼鼻头"]
LIP = ["薄唇","厚唇","上薄下厚","上厚下薄","宽嘴","小嘴","弓形唇","平直唇","成熟长唇"]
MOUTH_CORNER = ["嘴角上扬","嘴角平直","嘴角下垂","单侧上扬","嘴角紧收"]
MARK = ["无标志","左眼下浅泪痣","右眼下浅泪痣","眉尾旧疤","眉心竖纹浅痕","右眉轻断","鼻梁旧伤",
 "左颊浅疤","颈侧细疤","耳后小痣","唇下小痣","眼角小痣","异色瞳","环状虹膜","碎裂虹膜",
 "单侧虎牙","单侧酒窝","双侧酒窝","指节薄茧","眉上小疤","下颌浅疤","额角旧痕","眼睑褶皱不对称","瞳孔残缺"]

PERSONALITY = ["清冷","聪慧","柔软","野性","可靠","危险","温柔","疯狂","神性","妖异","沉稳","孤傲",
 "温润","凌厉","散漫","坚毅","天真","沧桑","阴郁","明亮","克己","放纵","疏离","亲和","神秘","直率",
 "隐忍","张扬","克制","暴烈","悲悯","冷酷","慵懒","警觉","虔诚","叛逆","温雅","狠戾","通透","执拗",
 "从容","局促","高贵","市井","病弱","强健","沉静","躁动","坦然"]

BODY_BUILD_M = ["剑士型","战士型","刺客型","智者型","力士型","瘦长型","均衡型","重装型","游侠型","隐修型"]
BODY_BUILD_F = ["灵巧型","战斗型","成熟型","少女型","修长型","丰盈型","精悍型","异族型","温和型","猎手型"]
PROP = ["6.5头身","7头身","7.5头身","8头身","8.5头身"]
MUSCLE = ["低脂清晰","中等紧实","饱满力量","非战斗肌","少年未成型","病弱纤薄","精瘦紧致","厚实沉稳"]
STANCE = ["自然站姿","重心前倾","重心后坐","侧身戒备","放松垂手","抱臂而立","手扶武器","微微下沉"]

FACTION = ["镇墟司","宗门","流亡者","贵族","战士团","商贾","医者","隐世","恶灵","复苏体","灰区","王庭","游侠","学宫"]
COSTUME_SILHOUETTE = ["长袍","短衣","半甲","轻甲","重甲","披风","护臂","腰封","多层衣摆","非对称剪裁","束身","宽袖"]
COSTUME_STRUCT = ["肩甲结构","胸甲结构","分片下摆","交领叠襟","绑带束腰","背部长摆","腿部绑甲","外披短褂","高领护颈","暗袋夹层"]
COSTUME_ACC = ["腰牌","臂环","护腕","颈饰","面具残片","符囊","药囊","令牌","断扣","旧皮带","耳饰","额饰"]
COSTUME_COND = ["完整如新","日常使用痕","战损修补","边境磨损","陈年旧物","当下战损","身份剥除感"]

HAIR_STRUCT = ["高束","低束","半束","散发","编发","盘发","双层结构","不对称发型","短削","中长直落"]
HAIR_TEX = ["柔顺","厚重","凌乱","湿润","风吹感","战损感","干枯","油亮","毛躁"]
HAIR_ERA = ["少年","成年","黑化","战后"]

MATERIAL = [
 ("布料","丝绸","素白","轻","细腻","轻微","柔和","华贵"),
 ("布料","麻布","土褐","中","粗糙","明显","哑光","劳作"),
 ("布料","粗布","灰青","中","粗结","明显","哑光","底层"),
 ("布料","纱","半透明","极轻","轻薄","无","朦胧","飘逸"),
 ("布料","皮革","深棕","重","纹路清晰","明显","半哑","征途"),
 ("金属","青铜","暗青金","重","铸造纹","氧化痕","冷光","古旧"),
 ("金属","黑铁","哑黑","重","锻造痕","锈斑","暗哑","实用"),
 ("金属","玄钢","冷银","重","致密","细微","锐利反光","锋利"),
 ("金属","银","银白","中","拉丝","轻微","高反光","仪典"),
 ("金属","金","暖金","重","浮雕","轻微","亮泽","权贵"),
 ("金属","寒铁合金","青灰","重","暗纹","寒霜感","冷光","禁制"),
 ("自然","玉石","青白","中","温润","包浆感","半透光泽","灵性"),
 ("自然","木","原木色","轻","年轮","磨损","哑光","朴素"),
 ("自然","骨","灰白","中","多孔","裂纹","哑光","野性"),
 ("自然","晶体","透明蓝","中","多面","崩口","折射","能量"),
]

ABILITY_MECH = ["方向改变","位置改变","空间连接","状态交换","冻结","复制","吞噬","强化","削弱",
 "延迟","加速","折叠","锚定","转移","伪装","记录","回溯","共生","寄生","分解","重构","共振",
 "标记","剥离","回响","嵌套","错位"]
ABILITY_SOURCE = ["血脉","契约","器物","功法","天授","残缺体质","异化","共鸣"]
ABILITY_MEDIUM = ["气","血","影","声","光","尘","纹","丝","雾","雷"]
ABILITY_CONTACT = ["接触命中","范围笼罩","视线锁定","地面蔓延","媒介传导"]
ABILITY_RESULT = ["造成位移","改变因果顺序","剥夺行动","交换位置","复制信息","限制变化",
 "吸收结构","改变身体规则","标记目标","制造错误感知"]

DOMAIN_TYPE = ["空间领域","感知领域","时间领域","因果领域","规则领域","生命领域","材料领域",
 "声音领域","影之领域","温度领域","重力领域","概念领域"]
DOMAIN_TRIGGER = ["画地为界","睁眼即启","以血为引","击掌触发","咏唱三息","吞下媒介","受创反启","静立不动"]
DOMAIN_SCOPE = ["半径三步","一整个房间","视线之内","一条战线","自身为心","百步方圆"]
DOMAIN_RULE = ["距离被改写","方向不再可信","速度分层","结果可被替换","某种力消失",
 "进入者被记录","位置可被抵押","语言即成真","影与本体互换","重量可被赋予"]

WEAPON_TYPE = ["单手剑","双手巨剑","短刀","长刀","枪","戟","鞭","软剑","弓","弩","拳套","爪","扇","伞",
 "钟","印","幡","笛","链","盾","符","锤","镰","环","笔","琴","针","钩","棍","杖"]
WEAPON_MECH = ["折叠变形","断节重组","以气御使","吸血反哺","铭文启动","分体飞击","锁链牵引","刀刃自愈",
 "收纳空间","共鸣震动","结印增幅","消耗寿命","吸取记忆","重量变化","镜像复制"]
WEAPON_MATERIAL = ["黑铁","玄钢","寒铁合金","青铜","骨","玉","木","晶体","银","金"]
WEAPON_FORM = ["短柄","长柄","无柄悬浮","可伸缩","双持","背负式","缠于手臂","藏于袖"]

ARCHETYPE = [
 ("英雄","成长 / 责任 / 突破","先冲再想，护住身后的人","挺拔剪影 + 明亮色块 + 标志性武器","镇墟司/宗门"),
 ("守护者","稳定 / 防御 / 牺牲","站在最前面，替人挡下","宽厚肩线 + 重甲 + 面盾","镇墟司/王庭"),
 ("猎杀者","精准 / 冷酷","一击之后不回头","修长低重心 + 深色 + 短刃","灰区/游侠"),
 ("谋略者","计算 / 控制","先布棋，再落子","规整剪影 + 书卷气 + 暗纹","学宫/王庭"),
 ("狂战士","力量 / 压迫","不闪不避，只向前","魁梧骨架 + 重器 + 战损","战士团/恶灵"),
 ("妖异者","魅惑 / 危险","美丽与杀意同时出现","异色瞳 + 反差配色 + 非人称武器","恶灵/复苏体"),
 ("游侠","自由 / 生存","不被任何一面墙困住","轻装 + 旧物堆叠 + 常用工具","灰区/游侠"),
 ("医者","救赎 / 旁观","先止血，再问对错","素净 + 药囊 + 稳定手","宗门/学宫"),
 ("隐修","克制 / 顿悟","不出手则已，出手即定局","简朴 + 极简剪影 + 一物","隐世/宗门"),
 ("反叛者","质疑 / 打破","规矩是给别人定的","不对称剪裁 + 记号 + 破损","灰区/流亡者"),
 ("匠人","专注 / 造物","东西比人可靠","工具挂满身 + 低调色 + 厚手掌","商贾/宗门"),
 ("囚徒","枷锁 / 复仇","先记住锁链的形状","束缚结构 + 旧伤 + 眼神不散","流亡者/灰区"),
 ("祭司","信仰 / 代价","替某样东西说话","仪典层叠 + 苍白 + 符号","宗门/王庭"),
 ("少年兵","早熟 / 未被磨平","假装不疼","未成型骨架 + 大一号装备","镇墟司/战士团"),
 ("归乡者","放下 / 执念","回来了，但地方变了","旧衣新补 + 停顿的站姿","灰区/隐世"),
]

# ============================================================ 1) Face DNA 5200
face_rows = []
seen = set()
egg_budget = 1200  # 限鹅蛋占比 <25%
tries = 0
while len(face_rows) < 5200 and tries < 400000:
    tries += 1
    pool = FACE_MAIN if len(face_rows) >= egg_budget else [f for f in FACE_MAIN if f not in EGG]
    main = random.choice(pool)
    aux = random.choice(FACE_AUX)
    fh, bb, so = random.choice(FOREHEAD), random.choice(BROW_BONE), random.choice(SOCKET)
    cb, ch, jw = random.choice(CHEEKBONE), random.choice(CHEEK), random.choice(JAW)
    et, ea, ed, ir = random.choice(EYE_TYPE), random.choice(EYE_TAIL), random.choice(EYE_DIST), random.choice(IRIS)
    nr, nb, nt = random.choice(NOSE_ROOT), random.choice(NOSE_BRIDGE), random.choice(NOSE_TIP)
    lp, mc = random.choice(LIP), random.choice(MOUTH_CORNER)
    mk = "无标志" if random.random() < 0.12 else random.choice(MARK[1:])
    key = (main, aux, bb, et, nb, jw, mk)
    if key in seen:
        continue
    seen.add(key)
    fid = f"FD{len(face_rows)+1:05d}"
    one = f"{main}（{aux}），{bb}/{so}，{et}·{ea}·{ed}，{nr}/{nb}/{nt}，{lp}·{mc}，{jw}"
    face_rows.append([fid, main, aux, fh, bb, so, cb, ch, jw, et, ea, ed, ir, nr, nb, nt, lp, mc, mk, one])

WCSV("01_FACE_DNA/face_dna_5000.csv",
     ["face_id","主脸型","辅变化","额头","眉骨","眼窝","颧骨","面颊","下颌","眼型","眼尾","眼距",
      "虹膜","鼻根","鼻梁","鼻头","唇型","嘴角","特殊标志","一句话脸"], face_rows)

# atoms 导出
WCSV("01_FACE_DNA/ATOMS_face_shape.csv", ["主脸型"], [[x] for x in FACE_MAIN])
WCSV("01_FACE_DNA/ATOMS_facial_structure.csv",
     ["额头","眉骨","眼窝","颧骨","面颊","下颌"],
     [[a,b,c,d,e,f] for a,b,c,d,e,f in zip(pick(FOREHEAD,8),pick(BROW_BONE,8),pick(SOCKET,8),
                                            pick(CHEEKBONE,8),pick(CHEEK,8),pick(JAW,8))])
WCSV("01_FACE_DNA/ATOMS_eye.csv", ["眼型","眼尾","眼距","虹膜"],
     [[a,b,c,d] for a,b,c,d in zip(EYE_TYPE, pick(EYE_TAIL,28), pick(EYE_DIST,28), pick(IRIS,28))])
WCSV("01_FACE_DNA/ATOMS_nose_mouth.csv", ["鼻根","鼻梁","鼻头","唇型","嘴角"],
     [[a,b,c,d,e] for a,b,c,d,e in zip(pick(NOSE_ROOT,20),pick(NOSE_BRIDGE,20),pick(NOSE_TIP,20),
                                        pick(LIP,20),pick(MOUTH_CORNER,20))])
WCSV("01_FACE_DNA/ATOMS_mark.csv", ["特殊标志"], [[x] for x in MARK])

# ============================================================ 2) 气质 1100
pers_rows, pseen = [], set()
while len(pers_rows) < 1100:
    a, b, c = random.sample(PERSONALITY, 3)
    if (a, b, c) in pseen:
        continue
    pseen.add((a, b, c))
    vis = f"{a}→收紧动作幅度与表情；{b}→{random.choice(['稳定眼神','放松眼尾/嘴角','锐利眼型','强烈轮廓','结构不对称','材质温润','非人平静'])}；{c}→{random.choice(['简洁剪影','层叠结构','破损细节','高洁材质','反差配色'])}"
    pers_rows.append([f"PS{len(pers_rows)+1:05d}", a, b, c, f"{a}、{b}、{c}", vis,
                      f"第一眼{a}，第二眼{b}，第三眼{c}"])
WCSV("02_PERSONALITY/personality_1000.csv",
     ["p_id","第一眼","第二眼","第三眼","关键词串","视觉化要点","一句话"], pers_rows)
WCSV("02_PERSONALITY/ATOMS.csv", ["气质词"], [[x] for x in PERSONALITY])

# ============================================================ 3) 身体 560
body_rows, bseen = [], set()
while len(body_rows) < 560:
    g = random.choice(["男","女"])
    build = random.choice(BODY_BUILD_M if g == "男" else BODY_BUILD_F)
    pr, mu, st = random.choice(PROP), random.choice(MUSCLE), random.choice(STANCE)
    if (g, build, pr, mu, st) in bseen:
        continue
    bseen.add((g, build, pr, mu, st))
    body_rows.append([f"BD{len(body_rows)+1:04d}", g, build, pr, mu, st,
                      f"{g}性·{build} / {pr} / {mu} / {st}"])
WCSV("03_BODY/body_500.csv", ["body_id","性别","体型","比例","肌肉型","站姿","描述"], body_rows)

# ============================================================ 4) 发型
hair_rows = []
for i,(s,t,e) in enumerate(((s,t,e) for s in HAIR_STRUCT for t in HAIR_TEX for e in HAIR_ERA)):
    hair_rows.append([f"HR{i+1:04d}", s, t, e, f"{e}期·{s}·{t}"])
WCSV("04_HAIR/hair.csv", ["hair_id","结构","质感","时期","描述"], hair_rows)

# ============================================================ 5) 服装 1080
cost_rows, cseen = [], set()
while len(cost_rows) < 1080:
    fac, sil, st = random.choice(FACTION), random.choice(COSTUME_SILHOUETTE), random.choice(COSTUME_STRUCT)
    acc1, acc2 = random.sample(COSTUME_ACC, 2)
    cond = random.choice(COSTUME_COND)
    if (fac, sil, st, cond) in cseen:
        continue
    cseen.add((fac, sil, st, cond))
    cost_rows.append([f"CS{len(cost_rows)+1:05d}", fac, sil, st, f"{acc1}+{acc2}", cond,
                      f"{fac}·{sil}｜{st}｜{acc1}+{acc2}｜{cond}"])
WCSV("05_COSTUME/costume_1000.csv",
     ["costume_id","阵营","剪影","结构要素","配饰","状态","描述"], cost_rows)

# ============================================================ 6) 材质
WCSV("06_MATERIAL/material.csv",
     ["material_id","类别","名称","颜色","重量","纹理","磨损","反射","历史感"],
     [[f"MT{i+1:03d}", *m] for i, m in enumerate(MATERIAL)])

# ============================================================ 7) 能力 560
ab_rows, aseen = [], set()
while len(ab_rows) < 560:
    mech, src, med = random.choice(ABILITY_MECH), random.choice(ABILITY_SOURCE), random.choice(ABILITY_MEDIUM)
    con, res = random.choice(ABILITY_CONTACT), random.choice(ABILITY_RESULT)
    if (mech, src, con) in aseen:
        continue
    aseen.add((mech, src, con))
    ab_rows.append([f"AB{len(ab_rows)+1:04d}", mech, src, med, con, res,
                    f"以{src}为源、{med}为媒介：{mech}；{con} → {res}"])
WCSV("07_ABILITY/ability_500.csv",
     ["ability_id","机制","来源","媒介","接触方式","结果","一句话"], ab_rows)

# ============================================================ 8) 领域 320
do_rows, dseen = [], set()
while len(do_rows) < 320:
    t, tr, sc = random.choice(DOMAIN_TYPE), random.choice(DOMAIN_TRIGGER), random.choice(DOMAIN_SCOPE)
    rl = random.choice(DOMAIN_RULE)
    if (t, tr, rl) in dseen:
        continue
    dseen.add((t, tr, rl))
    limit = random.choice(["每次不超过三息","施术者不能移动","范围内自己同样受限","需持续消耗","对同一目标只生效一次","破界即反噬"])
    adv = random.choice(["抢先手","制造不可预测","地形绝对化","团队增益","封锁退路"])
    cost = random.choice(["寿命","记忆","感官","血液","体温","身份痕迹"])
    brk = random.choice(["击碎中心锚点","同时攻击内外两侧","破坏触发条件","用同源规则对冲","让施术者说出真名"])
    nm = f"{t[:2]}·{tr}"
    do_rows.append([f"DM{len(do_rows)+1:04d}", t, nm, tr, sc, rl, limit, adv, cost, brk])
WCSV("08_DOMAIN/domain_300.csv",
     ["domain_id","类型","名称","触发","范围","规则","限制","优势","代价","破坏方式"], do_rows)

# ============================================================ 9) 武器 560
wp_rows, wseen = [], set()
while len(wp_rows) < 560:
    ty, me, ma, fm = random.choice(WEAPON_TYPE), random.choice(WEAPON_MECH), random.choice(WEAPON_MATERIAL), random.choice(WEAPON_FORM)
    if (ty, me, fm) in wseen:
        continue
    wseen.add((ty, me, fm))
    wp_rows.append([f"WP{len(wp_rows)+1:04d}", ty, me, ma, fm,
                    f"{ma}{ty}·{fm}；机制：{me}"])
WCSV("09_WEAPON/weapon_500.csv",
     ["weapon_id","类型","机制","材质","形态","描述"], wp_rows)

# ============================================================ 10) 原型
WCSV("10_ARCHETYPE/archetype.csv",
     ["archetype_id","名称","核心","行为模式","视觉倾向","常见阵营"],
     [[f"AT{i+1:02d}", *a] for i, a in enumerate(ARCHETYPE)])

print("数据表生成完毕")
print("face_dna:", len(face_rows), "personality:", len(pers_rows), "body:", len(body_rows),
      "hair:", len(hair_rows), "costume:", len(cost_rows), "ability:", len(ab_rows),
      "domain:", len(do_rows), "weapon:", len(wp_rows))
