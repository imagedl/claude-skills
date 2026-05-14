#!/usr/bin/env python3
"""
火山引擎即梦AI 图生图模板
用法: 修改 src/out_path/prompt/scale 后直接运行
"""
import json, datetime, hashlib, hmac, requests, base64, time, os
from PIL import Image
import io

# ── API 配置 ──────────────────────────────────────────────────
method     = 'POST'
host       = 'visual.volcengineapi.com'
region     = 'cn-north-1'
endpoint   = 'https://visual.volcengineapi.com'
service    = 'cv'
access_key = 'AKLTMjk1NTZiMTg0M2NmNDNkYzgzYzI3N2ExM2Y3Yjg1MjQ'
secret_key = 'TmpZek9HWmtNVEk0TURNeU5HTXhaamhqTVdJME1UbGpZVEE1TmpaaFl6VQ=='

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def call_api(action, version, body_params):
    req_body = json.dumps(body_params)
    query_params = {'Action': action, 'Version': version}
    canonical_querystring = '&'.join(f'{k}={v}' for k, v in sorted(query_params.items()))
    t = datetime.datetime.utcnow()
    current_date = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')
    payload_hash = hashlib.sha256(req_body.encode('utf-8')).hexdigest()
    content_type = 'application/json'
    canonical_headers = (f'content-type:{content_type}\nhost:{host}\n'
                         f'x-content-sha256:{payload_hash}\nx-date:{current_date}\n')
    signed_headers = 'content-type;host;x-content-sha256;x-date'
    canonical_request = (f'{method}\n/\n{canonical_querystring}\n{canonical_headers}\n'
                         f'{signed_headers}\n{payload_hash}')
    credential_scope = f'{datestamp}/{region}/{service}/request'
    string_to_sign = ('HMAC-SHA256\n' + current_date + '\n' + credential_scope + '\n' +
                      hashlib.sha256(canonical_request.encode()).hexdigest())
    kDate    = sign(secret_key.encode('utf-8'), datestamp)
    kRegion  = sign(kDate, region)
    kService = sign(kRegion, service)
    kSigning = sign(kService, 'request')
    signature = hmac.new(kSigning, string_to_sign.encode(), hashlib.sha256).hexdigest()
    headers = {
        'X-Date': current_date,
        'Authorization': (f'HMAC-SHA256 Credential={access_key}/{credential_scope}, '
                          f'SignedHeaders={signed_headers}, Signature={signature}'),
        'X-Content-Sha256': payload_hash,
        'Content-Type': content_type
    }
    r = requests.post(f'{endpoint}?{canonical_querystring}', headers=headers, data=req_body, timeout=60)
    return r.json()

def prepare_img(path, max_long=2048):
    """resize到max_long再base64，避免超时和尺寸不足错误"""
    img = Image.open(path).convert('RGB')
    w, h = img.size
    ratio = min(max_long / w, max_long / h)
    nw, nh = int(w * ratio), int(h * ratio)
    img = img.resize((nw, nh), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=90)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode(), nw, nh

def submit_and_wait(img_b64, nw, nh, scale, prompt, out_path):
    # 提交（50430并发限制时等30秒重试）
    for attempt in range(5):
        resp = call_api('CVSync2AsyncSubmitTask', '2022-08-31', {
            'req_key': 'jimeng_seedream46_cvtob',
            'binary_data_base64': [img_b64],
            'prompt': prompt,
            'width': nw, 'height': nh,
            'force_single': True,
            'scale': scale,
        })
        if resp.get('code') == 10000:
            break
        elif resp.get('code') == 50430:
            print(f"  并发限制，等30秒... (attempt {attempt+1})")
            time.sleep(30)
        else:
            print(f"  ✗ 提交失败: {resp.get('message')} (code={resp.get('code')})")
            return False
    else:
        print("  ✗ 多次重试后仍失败")
        return False

    tid = resp['data']['task_id']
    print(f"  ✓ task_id={tid}")

    # 轮询结果
    for i in range(30):
        time.sleep(10)
        qresp = call_api('CVSync2AsyncGetResult', '2022-08-31', {
            'req_key': 'jimeng_seedream46_cvtob',
            'task_id': tid,
        })
        if qresp.get('code') == 10000:
            status = qresp['data'].get('status', '?')
            print(f"  [{i+1}] {status}")
            if status not in ('in_queue', 'in_progress', None):
                data = qresp['data']
                imgs = data.get('binary_data_base64') or []
                urls = data.get('image_urls') or []
                img_data = base64.b64decode(imgs[0]) if imgs else requests.get(urls[0]).content
                with open(out_path, 'wb') as f:
                    f.write(img_data)
                print(f"  ✓ 保存 {os.path.basename(out_path)} ({len(img_data)/1024/1024:.1f} MB)")
                return True
        else:
            print(f"  [{i+1}] err={qresp.get('code')}")
    print("  ✗ 超时未完成")
    return False


# ── 使用示例 ──────────────────────────────────────────────────
if __name__ == '__main__':
    SRC_FILES = [
        '/home/dulian/图片/杜莲 底片/花系主题册 (7).jpg',
    ]
    OUT_DIR = '/home/dulian/图片/修图/写真风格'
    STYLE_NAME = '法式复古油画风'
    SCALE = 85
    PROMPT = (
        'French vintage realist oil painting, classic academic portrait style, '
        'keep original face shape and facial features completely unchanged, '
        'preserve child face identity and likeness exactly, '
        'only add painterly oil texture to background flowers and clothing, '
        'smooth porcelain skin, soft warm golden light, '
        'painterly sunflower and daisy background, rich warm earthy tones, '
        'Bouguereau style, museum-quality fine art portrait'
    )

    for src in SRC_FILES:
        name = os.path.basename(src).replace('.jpg', '')
        w0, h0 = Image.open(src).size
        print(f"\n>>> [{name}] {w0}x{h0}")
        img_b64, nw, nh = prepare_img(src)
        out_path = os.path.join(OUT_DIR, f'{name}_{STYLE_NAME}.jpg')
        submit_and_wait(img_b64, nw, nh, SCALE, PROMPT, out_path)
        time.sleep(3)  # 避免紧连提交

    print("\n=== 全部完成 ===")
