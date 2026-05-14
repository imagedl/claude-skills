---
name: portrait-style-gen
description: >-
  Use when user wants to generate styled children portrait photos using 火山引擎即梦AI API.
  Triggers: "生成写真风格", "图生图写真", "批量生成风格图",
  "油画风", "法式复古", "伦勃朗", "印象派", "莫奈",
  "精灵风", "苔藓精灵", "月光精灵", "蘑菇精灵", "樱花精灵", "花仙子",
  "公主风", "公主城堡", "轻奢宫廷", "国风汉服",
  "唯美风", "马卡龙", "芭蕾核", "奶油白", "森系田园",
  "亲子风", "母女", "簪花汉服", "蕾丝皇冠", "母女白纱", "母女纱裙",
  "母女森系", "母女户外", "母女国潮", "母女新中式", "母女樱花", "母女和风".
---

# portrait-style-gen

使用火山引擎即梦AI（jimeng_seedream46_cvtob）对儿童写真进行风格化图生图。

## API 基础配置

```python
access_key = 'AKLTMjk1NTZiMTg0M2NmNDNkYzgzYzI3N2ExM2Y3Yjg1MjQ'
secret_key = 'TmpZek9HWmtNVEk0TURNeU5HTXhaamhqTVdJME1UbGpZVEE1TmpaaFl6VQ=='
req_key   = 'jimeng_seedream46_cvtob'
region    = 'cn-north-1'
service   = 'cv'
endpoint  = 'https://visual.volcengineapi.com'
```

图片预处理（**必须**，否则超时或报50500）：
```python
def prepare_img(path, max_long=2048):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    ratio = min(max_long/w, max_long/h)
    nw, nh = int(w*ratio), int(h*ratio)
    img = img.resize((nw, nh), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=90)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode(), nw, nh
```

提交 + 轮询（串行，免费账号只能1并发）：
```python
# 提交时遇50430(并发限制) → 等30秒重试
# GetResult每10s轮询，最多30次
# 结果取 binary_data_base64[0] 或 image_urls[0]
```

完整代码模板见 `api_template.py`。

## 输出目录

`/home/dulian/图片/修图/写真风格/`

---

## Scale 选择策略

| 情况 | scale | 说明 |
|------|-------|------|
| 人脸占比大 / 竖图 | 70–85 | 保留面部特征 |
| 环境占比大 / 横图 | 50 | 更强风格化 |
| 油画风（强烈推荐） | **85** | 面部保留度最高 |
| 其他风格默认 | 50 | 均衡效果 |

---

## 风格参数

---

## 一、公主风

### 经典粉嫩公主风
- **scale**: 50
- **prompt**:
```
a cute little girl, princess style portrait, wearing a pink lace tulle dress with bow details,
flower crown with roses and baby's breath, pastel pink floral wall background,
soft butterfly lighting, dreamy bokeh, moody pink and cream tones,
professional children photography, high quality, 8k resolution
```

---

### 轻奢宫廷公主风
- **scale**: 65
- **prompt**:
```
preserve original child face shape and facial features exactly, keep face identity unchanged,
elegant little princess portrait, luxurious gold and deep rose velvet gown,
golden tiara crown with pearls, ornate baroque palace garden background,
dramatic rembrandt lighting with golden highlights,
rich jewel tones, cinematic children portrait, museum-quality photography
```

---

### 国风古典公主风（汉服）
- **scale**: 55
- **prompt**:
```
beautiful little girl in chinese hanfu princess dress, soft pink and gold silk fabric,
traditional hair ornaments with jade and flowers, ancient chinese garden with lanterns,
warm golden hour lighting, delicate porcelain skin, watercolor painting atmosphere,
elegant oriental children portrait photography
```

---

### 公主城堡风（原版保留）
- **scale**: 50
- **prompt**:
```
princess in magical castle garden, fairytale royal garden with roses and vines,
elegant princess dress with sparkles, golden tiara crown, soft pink and gold tones,
enchanted castle background, dreamy bokeh, children portrait, high quality
```

---

## 二、唯美风

### 糖果马卡龙风
- **scale**: 50
- **prompt**:
```
sweet little girl in pastel macaron dreamland, wearing a pastel pink puff sleeve dress
with bow and lace ruffles, pink flower crown with roses,
soft cotton candy clouds and rainbow pastel background,
warm soft diffused lighting, candy color tones, whimsical fairy tale atmosphere,
children portrait photography, high quality
```

---

### 芭蕾核 Balletcore 风
- **scale**: 50
- **prompt**:
```
little ballerina girl, pastel pink ballet tutu dress, white pointe shoes,
ethereal white studio or soft pink backdrop, delicate lace details,
soft top lighting with gentle fill, airy and graceful movement,
japanese film photography aesthetic, high key lighting,
dreamy children portrait, fine art photography
```

---

### 奶油白极简风
- **scale**: 50
- **prompt**:
```
minimalist cream aesthetic children portrait, little girl in simple white linen dress,
pure white or warm off-white seamless background, single window soft natural light,
clean and airy composition, skin luminous and glowing,
modern fine art photography, editorial style, high fashion children portrait
```

---

### 森系田园风
- **scale**: 70
- **prompt**:
```
real photo, photorealistic children portrait, preserve original face identity completely,
little girl wearing a floral cotton dress and straw hat,
sitting in a sunny meadow with wildflowers and tall grass,
golden hour backlit photography, warm green and yellow tones,
dreamy soft bokeh background, natural film photography aesthetic,
kodak portra color tones, children portrait, high quality
```

---

## 三、油画风

### 法式复古写实油画风 ✅（已验证最佳）
- **scale**: 85
- **适用**: 所有构图（竖/横），面部保留度最高
- **prompt**:
```
French vintage realist oil painting, classic academic portrait style,
keep original face shape and facial features completely unchanged,
preserve child face identity and likeness exactly,
only add painterly oil texture to background flowers and clothing,
smooth porcelain skin, soft warm golden light,
painterly sunflower and daisy background, rich warm earthy tones,
Bouguereau style, museum-quality fine art portrait
```

---

### 荷兰黄金时代风（伦勃朗）
- **scale**: 85
- **prompt**:
```
rembrandt style oil painting portrait, little girl with soft candlelight illumination,
classic triangle highlight on cheek, dark rich background in deep brown and forest green,
warm amber and ochre color palette, antique european interior,
visible impasto brushstrokes, old master painting texture,
dramatic chiaroscuro lighting, dutch golden age fine art
```

---

### 印象派莫奈风
- **scale**: 70
- **prompt**:
```
impressionist oil painting of a child in a garden, monet-inspired style,
visible loose expressive brushstrokes, dappled sunlight through flowers,
vibrant but harmonious colors — yellow, green, soft pink and lavender,
atmospheric garden background with water lilies or roses,
post-impressionist texture, plein air painting, fine art children portrait
```

---

### 油画风（通用版）
- **scale 选择策略**:
  - 竖图 / 人脸占比大 → scale=70
  - 横图 / 环境占比大 → scale=50
- **prompt**:
```
oil painting portrait of a child, impressionist style, visible brushstrokes,
warm golden sunflower field background, painterly texture on clothing and flowers,
soft realistic face with delicate features, natural skin tone,
Monet-inspired floral garden, rich warm yellows and greens,
artistic masterpiece, children portrait oil painting
```

---

## 四、精灵风

### 苔藓森林精灵风
- **scale**: 65
- **prompt**:
```
preserve original child face shape and facial features exactly, keep face identity unchanged,
woodland elf fairy girl portrait, lush ancient forest setting,
wearing a flowing sage green and earth-tone fairy dress,
intricate leaf and moss crown, delicate pointed elf ears,
magical golden dappled sunlight through forest canopy (tyndall light effect),
soft green and earthy tones, glowing fireflies in background,
enchanted nature spirit atmosphere, children fantasy portrait photography
```

---

### 花海仙子风
- **scale**: 50
- **prompt**:
```
flower fairy girl in full bloom garden, wearing sheer white chiffon fairy dress,
elaborate fresh flower crown with roses, peonies and wildflowers,
surrounded by soft pink and white flower field,
golden hour backlight creating magical aura,
gossamer butterfly wings with translucent shimmer,
fairy dust sparkles, dreamy shallow depth of field,
enchanted garden children portrait
```

---

### 月光精灵风
- **scale**: 50
- **prompt**:
```
moonlight fairy girl portrait, mystical blue and violet night atmosphere,
iridescent silver and deep blue fairy costume, crescent moon hair accessory,
bioluminescent flowers and floating magical orbs in background,
cool moonlit color palette — silver, deep blue, soft lavender,
ethereal and otherworldly, fantasy children portrait photography,
cinematic lighting with colored gels
```

---

### 蘑菇精灵风
- **scale**: 50
- **prompt**:
```
adorable mushroom fairy girl in enchanted forest, tiny cottage-core fairy outfit
in warm rust and cream tones, sitting on giant toadstool mushroom,
surrounded by miniature forest world with tiny doors and windows,
warm amber and terracotta colors, magical soft bokeh,
photorealistic cozy whimsical children portrait photography
```

---

### 樱花精灵风（春季限定）
- **scale**: 50
- **prompt**:
```
cherry blossom fairy girl portrait, wearing a delicate pink kimono-inspired fairy dress,
sakura flower crown, surrounded by soft falling pink petals,
japanese garden with cherry blossom trees in full bloom,
soft pink and white color palette, hazy dreamy atmosphere,
film photography aesthetic with gentle lens flare,
spring fairy tale children portrait photography
```

---

## 五、亲子风（母女）

> **双人场景通用规则**
> 
> **面部保留三重指令**（每个亲子 prompt 必须包含前 3 行）：
> ```
> preserve original face shapes and facial features of both mother and child completely unchanged,
> do not alter face structure, eyes, nose or mouth of either person,
> keep both faces identical to the original photo,
> ```
> 
> **双人负向 prompt**（可选，对抗面部融合/变形）：
> ```
> face merging, face swap, distorted features, altered facial structure, blurred faces, identity change
> ```
> 
> **Scale 策略（双人）**：
> | 构图类型 | scale | 说明 |
> |---------|-------|------|
> | 半身/特写（面部占比大） | 72–78 | 最高面部保留 |
> | 全身站姿 | 65–70 | 平衡服装与面部 |
> | 环境占主导 | 60–65 | 更强场景风格化 |
> | 汉服/国风 | 65–68 | 防 50500，prompt 需精简 |

---

### 母女白纱宫廷风
- **scale**: 75
- **prompt**:
```
preserve original face shapes and facial features of both mother and child completely unchanged,
do not alter face structure, eyes, nose or mouth of either person,
keep both faces identical to the original photo,
luxurious mother and daughter portrait in royal garden,
wearing matching white and ivory layered tulle princess gowns,
ornate golden tiara crowns with pearls and crystals,
grand baroque palace garden with marble columns and white roses,
soft diffused window light, cream white and gold tones,
fine art portrait photography, editorial style, museum-quality
```

---

### 母女白色蕾丝皇冠风
- **scale**: 75
- **prompt**:
```
preserve original face shapes and facial features of both mother and child completely unchanged,
do not alter face structure, eyes, nose or mouth of either person,
keep both faces identical to the original photo,
mother and daughter wearing matching white sheer lace gowns with silver crystal embroidery,
mother wearing tall elaborate silver crystal crown with layered spikes and silver drop earrings,
daughter wearing flat silver crystal headband crown and delicate silver necklace,
soft white feather background, pure white and silver tones,
high-end studio portrait lighting, fine art photography, museum-quality
```

---

### 母女奶油梦幻纱裙风
- **scale**: 72
- **prompt**:
```
preserve original face shapes and facial features of both mother and child completely unchanged,
do not alter face structure, eyes, nose or mouth of either person,
keep both faces identical to the original photo,
mother and son in ivory white ball gowns, sheer organza top with puff sleeves and 3D rose applique,
thick opaque satin floor-length skirt covering legs entirely, voluminous tulle underskirt,
son wearing large soft flower crown, mother with braided hair and small flowers,
warm golden-brown art studio background, white harp prop, soft bokeh particles,
cinematic dreamy fine art family portrait, high quality
```

---

### 母女簪花汉服风 ✅（已验证）
- **scale**: 68
- **注意**: prompt 必须精简，过于复杂会触发 err=50500；禁止遮脸元素（如扇子/面纱）
- **prompt**:
```
preserve original face shapes and facial features of both mother and child completely unchanged,
do not alter face structure, eyes, nose or mouth of either person,
keep both faces identical to the original photo,
mother wearing ivory hanfu with wide flowing sleeves,
daughter wearing soft pink hanfu,
mother wearing full round floral headdress with white and pink flowers, chinese zanhua style,
daughter wearing smaller round flower crown with pink blooms,
soft pink studio background, warm diffused lighting,
chinese portrait photography, photorealistic, high quality
```

---

### 母女森系户外风 🆕
- **scale**: 68
- **适用**: 自然光户外场景，全身或半身构图
- **prompt**:
```
preserve original face shapes and facial features of both mother and child completely unchanged,
do not alter face structure, eyes, nose or mouth of either person,
keep both faces identical to the original photo,
mother and daughter in matching floral cotton dresses in soft sage green and blush pink,
flower crowns with wildflowers and baby's breath,
standing in sunlit meadow with tall grass and wildflowers,
golden hour backlit photography, warm green and golden tones,
dreamy shallow bokeh background, kodak portra film aesthetic,
natural family portrait photography, high quality
```

---

### 母女新中式国潮风 🆕
- **scale**: 65
- **注意**: prompt 精简，避免复杂头饰描述；背景建议选园林或水墨
- **prompt**:
```
preserve original face shapes and facial features of both mother and child completely unchanged,
do not alter face structure, eyes, nose or mouth of either person,
keep both faces identical to the original photo,
mother in elegant new chinese style qipao in deep dusty rose with gold embroidery,
daughter in matching mini new chinese style dress with floral pattern,
mother with updo hairstyle and jade hair pin, daughter with two small buns,
traditional chinese garden background with peonies and rockery,
warm golden natural light, rich jewel tones, cinematic chinese portrait photography
```

---

### 母女樱花和风风 🆕
- **scale**: 70
- **适用**: 春季主题，全身站姿效果最佳
- **prompt**:
```
preserve original face shapes and facial features of both mother and child completely unchanged,
do not alter face structure, eyes, nose or mouth of either person,
keep both faces identical to the original photo,
mother and daughter wearing matching pink floral kimono-style robes with obi belts,
surrounded by falling cherry blossom petals under blooming sakura trees,
soft pink and white color palette, hazy dreamy spring atmosphere,
gentle lens flare, warm afternoon light, japanese film photography aesthetic,
family portrait photography, high quality
```

---

## 注意事项

- width × height 必须 ≥ 1024×1024，否则报50500
- 原图需 resize 到 max_long=2048 再 base64，否则请求超时
- 免费账号单并发，50430错误等30秒重试，不要并发提交
- 法式复古油画风 scale=85 能最大程度保留原图面部特征，是人像写真的推荐选择
- 油画风系列统一使用 scale=85（竖图）或 scale=70（横图）
- **亲子风关键**：双人面部识别难度更高，scale 不低于 65；prompt 中三重面部保留指令必须保留在前三行
- **亲子风防坑**：汉服/国风类 prompt 字数控制在 120 词以内，过长触发 50500
- **日系奶油白风已移除**：原图若本身是白底日系风，scale≥70 时模型判断"不需要改"，换装效果几乎为零，不适合作为独立风格
