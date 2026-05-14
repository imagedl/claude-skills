#!/usr/bin/env python3
"""
38张底片批量风格化生成脚本
- 每张图使用最推荐的第一风格
- 串行执行（免费账号单并发）
- 已生成的自动跳过
用法: python3 /home/dulian/.claude/skills/portrait-style-gen/batch_portrait.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from api_template import prepare_img, submit_and_wait
import time
from PIL import Image

SRC_DIR = '/home/dulian/图片/杜莲 底片'
OUT_DIR = '/home/dulian/图片/修图/写真风格'
os.makedirs(OUT_DIR, exist_ok=True)

# ── Prompt 库 ─────────────────────────────────────────────────
PROMPTS = {

    '法式复古写实油画风': {
        'scale': 85,
        'prompt': (
            'French vintage realist oil painting, classic academic portrait style, '
            'keep original face shape and facial features completely unchanged, '
            'preserve child face identity and likeness exactly, '
            'only add painterly oil texture to background flowers and clothing, '
            'smooth porcelain skin, soft warm golden light, '
            'painterly sunflower and daisy background, rich warm earthy tones, '
            'Bouguereau style, museum-quality fine art portrait'
        ),
    },

    '印象派莫奈油画风': {
        'scale': 70,
        'prompt': (
            'impressionist oil painting of a child in a garden, monet-inspired style, '
            'visible loose expressive brushstrokes, dappled sunlight through flowers, '
            'vibrant but harmonious colors — yellow, green, soft pink and lavender, '
            'atmospheric garden background with water lilies or roses, '
            'post-impressionist texture, plein air painting, fine art children portrait'
        ),
    },

    '荷兰黄金时代伦勃朗风': {
        'scale': 85,
        'prompt': (
            'rembrandt style oil painting portrait, little girl with soft candlelight illumination, '
            'classic triangle highlight on cheek, dark rich background in deep brown and forest green, '
            'warm amber and ochre color palette, antique european interior, '
            'visible impasto brushstrokes, old master painting texture, '
            'dramatic chiaroscuro lighting, dutch golden age fine art'
        ),
    },

    '苔藓森林精灵风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'woodland elf fairy girl portrait, lush ancient forest setting, '
            'wearing a flowing sage green and earth-tone fairy dress, '
            'intricate leaf and moss crown, delicate pointed elf ears, '
            'magical golden dappled sunlight through forest canopy (tyndall light effect), '
            'soft green and earthy tones, glowing fireflies in background, '
            'enchanted nature spirit atmosphere, children fantasy portrait photography'
        ),
    },

    '蘑菇精灵风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'adorable mushroom fairy girl in enchanted forest, tiny cottage-core fairy outfit '
            'in warm rust and cream tones, sitting on giant toadstool mushroom, '
            'warm amber and terracotta colors, magical soft bokeh, '
            'real children portrait photography, photorealistic, high quality'
        ),
    },

    '花海仙子精灵风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'flower fairy girl in full bloom garden, wearing sheer white chiffon fairy dress, '
            'elaborate fresh flower crown with roses, peonies and wildflowers, '
            'surrounded by soft pink and white flower field, '
            'golden hour backlight creating magical aura, '
            'gossamer butterfly wings with translucent shimmer, '
            'fairy dust sparkles, dreamy shallow depth of field, '
            'enchanted garden children portrait'
        ),
    },

    '糖果马卡龙唯美风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'sweet little girl in pastel macaron dreamland, wearing a pastel pink puff sleeve dress '
            'with bow and lace ruffles, pink flower crown with roses, '
            'soft cotton candy clouds and rainbow pastel background, '
            'warm soft diffused lighting, candy color tones, whimsical fairy tale atmosphere, '
            'children portrait photography, high quality'
        ),
    },

    '奶油白极简风': {
        'scale': 80,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity completely unchanged, '
            'do not alter face structure, eyes, nose or mouth, '
            'minimalist cream aesthetic children portrait, little girl in simple white linen dress, '
            'pure white or warm off-white seamless background, single window soft natural light, '
            'clean and airy composition, skin luminous and glowing, '
            'modern fine art photography, editorial style, high fashion children portrait'
        ),
    },

    '经典粉嫩公主风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'a cute little girl, princess style portrait, wearing a pink lace tulle dress with bow details, '
            'flower crown with roses and baby\'s breath, pastel pink floral wall background, '
            'soft butterfly lighting, dreamy bokeh, moody pink and cream tones, '
            'professional children photography, high quality, 8k resolution'
        ),
    },

    '国风古典公主风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'beautiful little girl in chinese hanfu princess dress, soft pink and gold silk fabric, '
            'traditional hair ornaments with jade and flowers, ancient chinese garden with lanterns, '
            'warm golden hour lighting, delicate porcelain skin, soft bokeh background, '
            'elegant oriental children portrait photography, photorealistic'
        ),
    },

    '樱花精灵风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'cherry blossom fairy girl portrait, wearing a delicate pink kimono-inspired fairy dress, '
            'sakura flower crown, surrounded by soft falling pink petals, '
            'white fluffy rabbit companion, '
            'japanese garden with cherry blossom trees in full bloom, '
            'soft pink and white color palette, hazy dreamy atmosphere, '
            'film photography aesthetic with gentle lens flare, '
            'spring fairy tale children portrait photography'
        ),
    },

    '汉服樱花风': {
        'scale': 70,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'little girl in elegant pink hanfu dress catching falling cherry blossom petals with her raised hand, '
            'pink sakura petals drifting down and landing on her open palm, '
            'ancient chinese garden with cherry blossom trees in full bloom, '
            'traditional pavilion and stone path background, '
            'warm soft spring light, gentle pink and gold tones, '
            'delicate hair ornaments with sakura flowers, '
            'dreamy shallow depth of field, film photography aesthetic, '
            'children portrait photography, photorealistic, high quality'
        ),
    },

    '母女轻奢宫廷亲子风': {
        'scale': 75,
        'prompt': (
            'preserve original face shapes and facial features of both mother and child completely unchanged, '
            'do not alter face structure, eyes, nose or mouth of either person, '
            'keep both faces identical to the original photo, '
            'mother and daughter portrait in luxurious baroque palace garden, '
            'elegant gold and deep rose velvet gowns with pearl details, '
            'golden tiara crowns, ornate palace columns and roses background, '
            'dramatic warm golden rembrandt lighting, '
            'rich jewel tones — deep rose, champagne gold, ivory white, '
            'cinematic fine art family portrait, museum-quality photography'
        ),
    },

    '母女粉金纱裙宫廷风': {
        'scale': 75,
        'prompt': (
            'preserve original face shapes and facial features of both mother and child completely unchanged, '
            'do not alter face structure, eyes, nose or mouth of either person, '
            'keep both faces identical to the original photo, '
            'mother and daughter in luxurious blush pink and champagne gold layered ball gowns, '
            'heavily embroidered bodice with 3D floral applique and crystal embellishments, '
            'voluminous multi-layer organza skirt with lace trim, '
            'ornate royal crown with pearl and crystal details, brilliant sparkle, '
            'baroque rose garden palace background, soft warm golden light, '
            'haute couture fashion portrait, cinematic fine art photography, museum-quality'
        ),
    },

    '母女白纱宫廷风': {
        'scale': 75,
        'prompt': (
            'preserve original face shapes and facial features of both mother and child completely unchanged, '
            'do not alter face structure, eyes, nose or mouth of either person, '
            'keep both faces identical to the original photo, '
            'luxurious mother and daughter portrait in royal garden, '
            'wearing white and ivory layered tulle princess gowns, '
            'ornate golden tiara crowns with pearls, '
            'grand palace garden with marble columns and white roses, '
            'soft diffused window light, cream white and gold tones, '
            'fine art portrait photography, editorial style, museum-quality'
        ),
    },

    '轻奢宫廷公主风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'elegant little princess portrait, luxurious gold and deep rose velvet gown, '
            'golden tiara crown with pearls, ornate baroque palace garden background, '
            'dramatic rembrandt lighting with golden highlights, '
            'rich jewel tones, cinematic children portrait, museum-quality photography'
        ),
    },

    '月光精灵风': {
        'scale': 65,
        'prompt': (
            'preserve original child face shape and facial features exactly, keep face identity unchanged, '
            'moonlight fairy girl portrait, mystical blue and violet night atmosphere, '
            'iridescent silver and deep blue fairy costume, crescent moon hair accessory, '
            'bioluminescent flowers and floating magical orbs in background, '
            'cool moonlit color palette — silver, deep blue, soft lavender, '
            'ethereal and otherworldly, fantasy children portrait photography, '
            'cinematic lighting with colored gels'
        ),
    },

    '母女白色蕾丝皇冠风': {
        'scale': 75,
        'prompt': (
            'preserve original face shapes and facial features of both mother and child completely unchanged, '
            'do not alter face structure, eyes, nose or mouth of either person, '
            'keep both faces identical to the original photo, '
            'mother and daughter wearing matching white sheer lace gowns with intricate silver crystal embroidery, '
            'full long sleeves, delicate floral lace overlay, luxurious haute couture quality, '
            'mother wearing a tall elaborate silver crystal crown with layered spikes, '
            'silver drop earrings and silver crystal choker necklace, '
            'daughter wearing a flat silver crystal headband crown, no earrings on daughter, '
            'daughter also wearing a delicate silver crystal necklace, '
            'soft white feather background, pure white and silver tones, '
            'high-end studio portrait lighting, fine art photography, museum-quality'
        ),
    },

    '母女奶油梦幻纱裙风': {
        'scale': 72,
        'prompt': (
            'preserve original face shapes and facial features of both mother and child completely unchanged, '
            'do not alter face structure, eyes, nose or mouth of either person, '
            'keep both faces identical to the original photo, '
            'mother and daughter in dreamy ivory white multi-layer organza gowns with voluminous puff sleeves, '
            '3D floral applique scattered across bodice, soft feathered sleeve trim, '
            'daughter wearing a large soft flower crown covering her hair completely, '
            'mother with flowing hair and braided details with small flowers, '
            'warm moody golden-brown art studio background, white harp prop beside them, '
            'soft glowing bokeh particles floating in air, warm cream and ivory tones, '
            'cinematic dreamy fine art family portrait, high quality'
        ),
    },

    '母女簪花汉服风': {
        'scale': 68,
        'prompt': (
            'preserve original face shapes and facial features of both mother and child completely unchanged, '
            'do not alter face structure, eyes, nose or mouth of either person, '
            'mother wearing ivory hanfu with wide flowing sleeves, '
            'daughter wearing soft pink hanfu, '
            'mother wearing a full round floral headdress covering the top of her head, '
            'densely layered with white and pink flowers, chinese zanhua style, '
            'daughter wearing a smaller round flower crown with pink blooms, '
            'soft pink studio background, warm diffused lighting, '
            'chinese portrait photography, photorealistic, high quality'
        ),
    },

    '森系田园唯美风': {
        'scale': 70,
        'prompt': (
            'real photo, photorealistic children portrait, preserve original face identity completely, '
            'little girl wearing a floral cotton dress and straw hat, '
            'sitting in a sunny meadow with wildflowers and tall grass, '
            'golden hour backlit photography, warm green and yellow tones, '
            'dreamy soft bokeh background, natural film photography aesthetic, '
            'kodak portra color tones, children portrait, high quality'
        ),
    },
}

# ── 主动生成列表：只有在此列表中的任务才会执行生成 ──────────────
# 默认为空 = 不主动生成任何新图；已存在的文件仍会显示"已存在，跳过"
# 需要生成新图时，在此添加 (fname, style_name) 并运行脚本
TO_RUN = {
    ('DS1_5650.jpg', '母女白色蕾丝皇冠风'),
}

# ── 跳过列表：即使文件不存在也不重跑 ──────────────────────────
SKIP = {
    # ('文件名', '风格名'),  # 原因
    ('DS1_5671.jpg', '母女轻奢宫廷亲子风'),  # 妈妈脸型变了，待重新规划
    ('DS1_5343.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5349.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5603.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5629.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5630.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5650.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5653.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5662.jpg', '奶油白极简风'),   # 暂不跑
    ('DS1_5672.jpg', '奶油白极简风'),   # 暂不跑
}

# ── 38张底片 → 最推荐风格映射 ─────────────────────────────────
TASKS = [
    # 黄色花系组
    ('花系主题册 (12).jpg',  '印象派莫奈油画风'),
    ('花系主题册 (13).jpg',  '法式复古写实油画风'),
    ('花系主题册 (14).jpg',  '印象派莫奈油画风'),
    ('花系主题册 (15).jpg',  '法式复古写实油画风'),
    ('花系主题册 (17).jpg',  '法式复古写实油画风'),
    ('花系主题册 (20).jpg',  '印象派莫奈油画风'),
    ('花系主题册 (26).jpg',  '荷兰黄金时代伦勃朗风'),
    ('花系主题册 (7).jpg',   '森系田园唯美风'),
    # 森林精灵组
    ('花系主题册 (32).jpg',  '苔藓森林精灵风'),
    ('花系主题册 (34).jpg',  '苔藓森林精灵风'),
    ('花系主题册 (42).jpg',  '蘑菇精灵风'),
    ('花系主题册 (47).jpg',  '苔藓森林精灵风'),
    ('花系主题册 (47).jpg',  '樱花精灵风'),
    ('花系主题册 (50).jpg',  '苔藓森林精灵风'),
    ('花系主题册 (50).jpg',  '樱花精灵风'),
    # 糖果裙/室内花拱门组
    ('DS1_5333.jpg',         '糖果马卡龙唯美风'),
    ('DS1_5335.jpg',         '法式复古写实油画风'),
    ('DS1_5338.jpg',         '糖果马卡龙唯美风'),
    ('DS1_5343.jpg',         '奶油白极简风'),
    ('DS1_5349.jpg',         '奶油白极简风'),
    ('DS1_5356.jpg',         '法式复古写实油画风'),
    ('DS1_5387.jpg',         '糖果马卡龙唯美风'),
    ('DS1_5388.jpg',         '糖果马卡龙唯美风'),
    ('DS1_5393.jpg',         '花海仙子精灵风'),
    ('DS1_5397.jpg',         '花海仙子精灵风'),
    ('DS1_5404.jpg',         '法式复古写实油画风'),
    ('DS1_5404.jpg',         '轻奢宫廷公主风'),
    ('DS1_5405.jpg',         '经典粉嫩公主风'),
    ('DS1_5405.jpg',         '轻奢宫廷公主风'),
    # 汉服国风组
    ('DS1_5502.jpg',         '国风古典公主风'),
    ('DS1_5514.jpg',         '国风古典公主风'),
    ('DS1_5523.jpg',         '国风古典公主风'),
    ('DS1_5531.jpg',         '国风古典公主风'),
    ('DS1_5550_HD.jpg',      '国风古典公主风'),
    ('DS1_5550_HD.jpg',      '汉服樱花风'),
    # 亲子白底组
    ('DS1_5603.jpg',         '奶油白极简风'),
    ('DS1_5603.jpg',         '母女轻奢宫廷亲子风'),
    ('DS1_5629.jpg',         '奶油白极简风'),
    ('DS1_5629.jpg',         '母女轻奢宫廷亲子风'),
    ('DS1_5630.jpg',         '奶油白极简风'),
    ('DS1_5630.jpg',         '母女轻奢宫廷亲子风'),
    ('DS1_5650.jpg',         '奶油白极简风'),
    ('DS1_5650.jpg',         '母女轻奢宫廷亲子风'),
    ('DS1_5650.jpg',         '母女白色蕾丝皇冠风'),
    ('DS1_5653.jpg',         '奶油白极简风'),
    ('DS1_5653.jpg',         '母女轻奢宫廷亲子风'),
    ('DS1_5662.jpg',         '奶油白极简风'),
    ('DS1_5662.jpg',         '母女轻奢宫廷亲子风'),
    ('DS1_5671.jpg',         '法式复古写实油画风'),
    ('DS1_5671.jpg',         '母女粉金纱裙宫廷风'),
    ('DS1_5671.jpg',         '母女白纱宫廷风'),
    ('DS1_5671.jpg',         '母女白色蕾丝皇冠风'),
    ('DS1_5671.jpg',         '母女奶油梦幻纱裙风'),
    ('DS1_5662.jpg',         '母女簪花汉服风'),
    ('DS1_5672.jpg',         '奶油白极简风'),
    ('DS1_5672.jpg',         '母女轻奢宫廷亲子风'),
]

def main():
    total = len(TASKS)
    done = 0
    skipped = 0
    failed = 0

    for idx, (fname, style_name) in enumerate(TASKS, 1):
        src = os.path.join(SRC_DIR, fname)
        stem = fname.replace('.jpg', '')
        out_path = os.path.join(OUT_DIR, f'{stem}_{style_name}.jpg')

        print(f"\n[{idx}/{total}] {fname} → {style_name}")

        if (fname, style_name) in SKIP:
            print(f"  ⏭ 在跳过列表中，忽略")
            skipped += 1
            continue

        if os.path.exists(out_path):
            print(f"  ⏭ 已存在，跳过")
            skipped += 1
            continue

        if (fname, style_name) not in TO_RUN:
            print(f"  ⏭ 不在生成列表，跳过")
            skipped += 1
            continue

        if not os.path.exists(src):
            print(f"  ✗ 源文件不存在: {src}")
            failed += 1
            continue

        style = PROMPTS[style_name]
        w0, h0 = Image.open(src).size
        print(f"  原图: {w0}x{h0}, scale={style['scale']}")

        img_b64, nw, nh = prepare_img(src)
        ok = submit_and_wait(img_b64, nw, nh, style['scale'], style['prompt'], out_path)

        if ok:
            done += 1
        else:
            failed += 1

        time.sleep(3)

    print(f"\n{'='*50}")
    print(f"完成: {done}  跳过: {skipped}  失败: {failed}  共: {total}")
    print(f"输出目录: {OUT_DIR}")

if __name__ == '__main__':
    main()
