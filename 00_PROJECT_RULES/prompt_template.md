# 00 · 生图提示词模板

## 通用结构

```
主提示词 + 参考图约束 + 负面约束
```

主提示词内部顺序（不要打乱）：

```
身份（姓名/年龄/性别/阵营/属性）
→ Face DNA（逐项抄 face_dna.md）
→ Hair Identity
→ Body Identity
→ Costume Identity
→ 武器/道具
→ 镜头与比例
→ 当前图片任务（本张图是什么类型）
```

## 风格前缀（所有图共用，直接复制）

```
cinematic 3D CG character, high-end game cinematic, animated feature film quality,
realistic PBR fantasy character, Chinese xuanhuan fantasy, 72% realism / 28% stylization,
PBR skin with subtle SSS, visible pores, real eyelid thickness, strand-level hair,
cinematic lighting, depth of field, rim light, environmental reflection
```

## 负面约束（基础包）

```
real photo, live actor, AI portrait, influencer photo, 2D anime, cel shading,
plastic doll skin, wax figure skin, cheap game promo art,
cross-eyed, deformed hands, extra limbs, text, watermark, logo, signature
```

## 分类型模板

### identity（图1 身份标准照）
```
{风格前缀}
{姓名}, {年龄}岁{性别}, {阵营}
Face DNA: {脸型} + {三庭}, {眉骨}, {眉形}, {眼型}, {眼距}, {鼻根}/{鼻梁}/{鼻头}, {唇型}, {下颌}/{下巴}, {个性标志}
Hair: {发型}
Costume: {基础服装}
3:4 vertical, frontal chest-up portrait, facing camera, head straight, both eyes looking at lens,
restrained neutral expression, full top of head / shoulders / upper chest visible,
neutral light grey background, soft even studio CG lighting, no story, no action, no vfx, no weapon
{负面约束}
```

### design（图2 人物设计图）
```
{风格前缀}
character design sheet of {姓名}, 3:4,
one large front full body in the center, one smaller side full body on the left, one smaller back full body on the right,
all three are the SAME character: identical face, identical head-body ratio, identical hairstyle,
identical costume, identical boots, identical accessories, identical weapon, same natural standing pose,
no combat vfx, no story background, only the front view shows the weapon structure
Face DNA: {...}
{负面约束} + no expression sheet, no text, no material swatches, no scene thumbnails
```

### videoasset（视频角色资产图）
```
{风格前缀}
video consistency reference sheet of {姓名}, large scale,
one large identity chest-up portrait + front / side / back three full body views,
simple background, no story, no action, no vfx, no extra design board
Face DNA: {...}
```

### hero（Hero Key Art）
```
{风格前缀}
Hero Key Art of {姓名}, 2:3 vertical, two-thirds to near full body, character occupies 55-70%,
mid shot character sharpest, blurred foreground object for depth, background carries world-building,
ONE core event only: {核心机制画面}
Face DNA: {...}
{负面约束}
```
> 构图前先回答：**什么画面只有这个角色能够出现？**

### frame（视频 Hero Frame）
```
{风格前缀}
16:9 single shot, one clear moment: {起手/冲刺/格挡/召唤/释放/命中/卸力/落地/收招},
action logic: source -> direction -> contact point -> environmental feedback,
face clearly visible, no motion blur on face, anatomically valid motion
Face DNA: {...}
```

### effect（战斗特效图）
```
{风格前缀}
ability VFX study of {姓名}, 9:16,
where it originates: {...} / where it travels: {...} / what it contacts: {...} / what happens after contact: {...},
material logic: {金属/尘土/晶体/液体/骨/火焰...}
{负面约束} + no generic colorful beam, no random particles, no magic circle spam
```

## 使用约定

- 只说「提示词」时不输出长篇档案，只给可复制的三段式。
- Face DNA 字段一律从该角色 `face_dna.md` 抄，不临场改写（改了就是换脸）。
- 每张图的提示词最终落盘到 `01_CHARACTERS/<角色>/prompts/`。
