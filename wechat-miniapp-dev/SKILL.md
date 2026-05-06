---
name: wechat-miniapp-dev
description: >-
  Use when developing WeChat Mini Program (微信小程序) with CloudBase cloud functions,
  OCR, wx.cloud API, WXML/WXSS/JS. Triggers: 小程序开发, 云函数, fn-ocr, fn-user,
  wx.cloud.uploadFile, chooseMedia, tcb deploy, cloudbaserc, miniprogram-ci,
  小程序上传, 云函数部署, 数据库 push, OCR识别, 验光, 眼轴.
---

# wechat-miniapp-dev

微信小程序 + CloudBase 开发实战指南。基于南吴眼镜小程序项目积累的坑点与模式。

---

## 项目结构

```
miniprogram/          # 小程序前端代码
cloudfunctions/       # 云函数（每个子目录一个函数）
cloudbaserc.json      # CloudBase 配置（envId + functions 列表）
package.json          # 含部署脚本
private.wx***.key     # 上传密钥（miniprogram-ci 使用）
upload.js             # 小程序代码上传脚本
```

---

## 云函数部署

### 命令行部署（tcb CLI）

```bash
# 部署单个云函数
tcb fn deploy fn-ocr --force --dir cloudfunctions/fn-ocr

# 部署多个
npm run deploy:ocr
npm run deploy:user
npm run deploy:all-fn
```

**坑：** `tcb fn deploy` 默认找 `functions/` 目录，项目实际用 `cloudfunctions/`，**必须加 `--dir`**。

### cloudbaserc.json 配置

```json
{
  "envId": "cloud1-xxx",
  "functions": [
    { "name": "fn-user", "timeout": 10, "memorySize": 128, "runtime": "Nodejs16.13" },
    { "name": "fn-ocr",  "timeout": 30, "memorySize": 256, "runtime": "Nodejs16.13" }
  ]
}
```

OCR 函数超时设 30s，内存设 256MB；其他函数 10s/128MB 即可。

### 小程序代码上传（miniprogram-ci）

```bash
node upload.js   # 或 npm run upload
```

上传后在微信公众平台体验版/审核。

---

## 页面生命周期：onLoad vs onShow

```
onLoad  — 页面首次创建时触发（传参 options），整个生命周期只触发一次
onShow  — 每次页面显示时触发，包括：首次打开 + 从其他页面 navigateBack 返回
```

**坑：非 TabBar 页面从子页面返回，只触发 onShow，不触发 onLoad。**

```javascript
// 错误：数据只在首次进入时加载，返回后不刷新
onLoad() { this.loadProducts() }

// 正确：放在 onShow，每次显示都刷新
onShow() { this.loadProducts() }
```

典型场景：
- 商品管理列表页 → 上传新商品 → 返回 → 列表需要刷新 → 必须在 `onShow` 里调用 `loadProducts()`
- 客户列表 → 新建客户 → 返回 → 同上

---

## 云图片 URL：cloud:// vs HTTP

`<image src="...">` **不能直接渲染 `cloud://` 格式的 fileID**，必须转为临时 HTTP URL。

```javascript
// 错误：直接用 fileID
this.setData({ photoUrl: product.images[0] })  // cloud://xxx — 不显示

// 正确：批量转换
const fileIDs = products
  .filter(p => p.images?.[0]?.startsWith('cloud://'))
  .map(p => p.images[0])

if (fileIDs.length > 0) {
  const urlRes = await wx.cloud.getTempFileURL({ fileList: fileIDs })
  const urlMap = {}
  urlRes.fileList.forEach(f => { urlMap[f.fileID] = f.tempFileURL })
  products.forEach(p => {
    if (p.images?.[0] && urlMap[p.images[0]]) {
      p.images = [urlMap[p.images[0]]]
    }
  })
}
```

临时 URL 有效期约 2 小时，每次进页面重新获取。

---

## wx.showLoading 配对规则

`wx.showLoading` 必须在所有退出路径上都调用 `wx.hideLoading`，否则 loading 蒙层会永久卡住。

```javascript
// 错误：异常路径没有 hideLoading
async loadProduct(id) {
  wx.showLoading({ title: '加载中...' })
  const res = await callFn(...)   // 如果抛出，hideLoading 永远不执行
  wx.hideLoading()
}

// 正确：用 try/finally 保证一定执行
async loadProduct(id) {
  wx.showLoading({ title: '加载中...' })
  try {
    const res = await callFn(...)
    // ...
  } catch (e) {
    wx.showToast({ title: '网络错误，请重试', icon: 'error' })
  } finally {
    wx.hideLoading()   // 无论成功/失败/异常都执行
  }
}
```

---

## 页面间通信（上一页回调）

子页面操作完成后需要通知父页面更新数据，用 `getCurrentPages()` 直接调用上一页的方法：

```javascript
// 子页面（image-crop/index.js）确认后回调
const pages = getCurrentPages()
const prevPage = pages[pages.length - 2]
if (prevPage && prevPage.onCropDone) {
  prevPage.onCropDone(res.tempFilePath)
}
wx.navigateBack()

// 父页面（product-upload.js）定义回调方法
onCropDone(croppedPath) {
  this.processImage(croppedPath)
}
```

注意：`pages[pages.length - 1]` 是当前页，`pages[pages.length - 2]` 是上一页。

---

## 图片上传：两次上传分离 OCR 与存储

拍照上传商品时，同一张图片需要做两件事：**永久存储**和 **OCR 识别后删除**。不要复用同一个 fileID。

```javascript
async processImage(path) {
  // 上传一份到商品永久路径
  const productFileID = await uploadFile(`product-images/${Date.now()}.jpg`, path)
  // 上传一份到 OCR 临时路径（云函数里用完后删除）
  const ocrFileID = await uploadFile(`ocr-temp/${Date.now()}.jpg`, path)
  
  const ocrRes = await callFn('fn-ocr', { action: 'recognizeProduct', data: { fileID: ocrFileID } })
  this.setData({ cloudPath: productFileID })  // 保存永久路径
}
```

**坑：只上传一次再传给 OCR，OCR 云函数删除后商品图片也没了。**

---

## Canvas 图片裁剪（仿微信头像）

基于 Canvas 2D API 实现拖动 + 双指缩放裁剪，适合微信小程序。

### 关键实现思路

```javascript
// 1. 初始化：图片最短边 = 裁剪框大小，居中
const scale = Math.max(cropSize / img.width, cropSize / img.height) * 1.05
const imgW = img.width * scale, imgH = img.height * scale
const imgX = cropX - (imgW - cropSize) / 2
const imgY = cropY - (imgH - cropSize) / 2

// 2. 拖动限制：裁剪框不能露出图片边缘
imgX = Math.min(imgX, cropX)
imgY = Math.min(imgY, cropY)
imgX = Math.max(imgX, cropX + cropSize - imgW)
imgY = Math.max(imgY, cropY + cropSize - imgH)

// 3. 输出裁剪结果：用 offscreenCanvas 截取裁剪区域
const offCanvas = wx.createOffscreenCanvas({ type: '2d', width: cropSize * dpr, height: cropSize * dpr })
const offCtx = offCanvas.getContext('2d')
offCtx.scale(dpr, dpr)
offCtx.drawImage(
  img,
  (cropX - imgX) / imgW * img.width,   // 源图 x 偏移
  (cropY - imgY) / imgH * img.height,   // 源图 y 偏移
  (cropSize / imgW) * img.width,        // 源图截取宽
  (cropSize / imgH) * img.height,       // 源图截取高
  0, 0, cropSize, cropSize
)
wx.canvasToTempFilePath({ canvas: offCanvas, fileType: 'jpg', quality: 0.92, success: ... })
```

### Canvas 页面必须用 `type: "2d"` 节点

```xml
<!-- WXML -->
<canvas type="2d" id="cropCanvas" bindtouchstart="onTouchStart"
        bindtouchmove="onTouchMove" bindtouchend="onTouchEnd"
        style="width:{{canvasW}}px; height:{{canvasH}}px"/>
```

```javascript
// 必须用 SelectorQuery，不能用 wx.createCanvasContext
wx.createSelectorQuery().select('#cropCanvas').fields({ node: true, size: true }).exec(res => {
  const canvas = res[0].node
  const ctx = canvas.getContext('2d')
  canvas.width = canvasW * dpr
  canvas.height = canvasH * dpr
  ctx.scale(dpr, dpr)
})
```

**坑：** 旧版 `wx.createCanvasContext` API 无法使用 `canvas.createImage()`，必须用 Canvas 2D 节点模式。

---

## WXML 条件渲染坑

```xml
<!-- 错误：form 初始为 {}，form.name 是 undefined，!== undefined 仍为 false -->
<view wx:if="{{form.name !== undefined && (isEdit || identified)}}">

<!-- 正确：直接用 flag 变量控制显示 -->
<view wx:if="{{isEdit || identified}}">
```

初始化 data 里的 `form: {}` 没有 `name` 属性，`form.name !== undefined` 在 WXML 里判断为 false，导致表单永远不显示。**用明确的 boolean flag 控制显示，不要用 form 字段的存在性判断。**

---

## 云函数调用模式

### 前端统一调用入口

```javascript
// miniprogram/utils/cloud.js
const { callFn } = require('../../utils/cloud')

// 调用示例
const res = await callFn('fn-user', { action: 'adminCreateCustomer', data: { ... } })
```

### 云函数路由模式

```javascript
// cloudfunctions/fn-xxx/index.js
exports.main = async (event) => {
  const { action, data } = event
  switch (action) {
    case 'actionName': return actionFn(data)
    default: return { code: 404 }
  }
}
```

返回值统一用 `{ code: 0, data: ... }` / `{ code: -1, msg: e.message }`。

---

## 数据库操作

### 向数组字段追加记录（db.command.push）

```javascript
const db = cloud.database()
await db.collection('users').doc(userId).update({
  data: { axialRecords: db.command.push({ date, rightEye, leftEye, createTime: new Date().toISOString() }) }
})
```

**坑：** `push` 是 `db.command.push`，不是数组原生 push。追加到嵌套数组必须用 command，直接赋值会覆盖整个数组。

---

## OCR 识别

### 上传图片 → OCR 流程

```javascript
// 1. 上传到云存储
const up = await wx.cloud.uploadFile({ cloudPath: `ocr/file_${Date.now()}.jpg`, filePath: tempPath })

// 2. 调用 OCR 云函数
const res = await callFn('fn-ocr', { action: 'recognizePrescription', data: { fileID: up.fileID } })

// 3. 用完删除临时文件（云函数内）
await cloud.deleteFile({ fileList: [data.fileID] }).catch(() => {})
```

### generalBasic OCR 返回格式

```javascript
const res = await cloud.openapi.ocr.generalBasic({ fileID: data.fileID })
const lines = (res.items || []).map(i => i.words)  // 每行文字
const fullText = lines.join('\n')
```

### 眼科报告解析（AVG 眼轴）

```javascript
// 眼科生物测量仪报告：AVG 行第一个两位小数 = 眼轴 AL（mm）
// 第一个 AVG = OD 右眼，第二个 AVG = OS 左眼
const avgLines = lines.filter(l => /^AVG\b/i.test(l.trim()))
const extractAL = (line) => { const m = line.match(/\b(\d{2}\.\d{2})\b/); return m ? m[1] : '' }
odAL = extractAL(avgLines[0])  // 右眼
osAL = extractAL(avgLines[1])  // 左眼

// 兜底：全文正则
const allAvg = [...text.matchAll(/AVG\s+(\d{2}\.\d{2})/gi)]
```

---

## 拍照/选图

### wx.chooseMedia（推荐）vs wx.chooseImage

```javascript
// 推荐：chooseMedia（支持指定来源）
wx.chooseMedia({
  count: 1, mediaType: ['image'], sourceType: ['camera', 'album'],
  success: async (res) => {
    const tempFile = res.tempFiles[0].tempFilePath
  }
})

// 旧API：chooseImage（tempFilePaths 不同）
wx.chooseImage({
  success: (res) => {
    const src = res.tempFilePaths[0]  // 注意是 tempFilePaths，不是 tempFiles
  }
})
```

**坑：** 两个 API 返回结构不同，混用会导致 undefined。

---

## WXML 模板常见模式

### 条件渲染 + 数据绑定

```xml
<block wx:if="{{identified}}">
  <input value="{{form.odAL}}" bindinput="onInput" data-key="odAL" type="digit"/>
</block>
```

### onInput 通用处理器

```javascript
onInput(e) { this.setData({ [`form.${e.currentTarget.dataset.key}`]: e.detail.value }) }
```

`data-key` + 通用 onInput，避免为每个字段写单独的处理函数。

---

## 页面导航

```javascript
// 跳转（可返回）
wx.navigateTo({ url: '/pages/my/axial' })

// 返回
wx.navigateBack()

// 带参数
wx.navigateTo({ url: `/pages/admin/customer-form?id=${id}` })
// 接收
onLoad(options) { const id = options.id }
```

---

## app.json 注册新页面

```json
{
  "pages": [
    "pages/my/index",
    "pages/my/prescription",
    "pages/my/axial",       // 新增页面必须在此注册
    "pages/my/invoice"
  ]
}
```

**坑：** 忘记注册会报 `page not found`，与 404 区分不明显。

---

## UI 设计工作流（强制规则）

**凡涉及新页面或重要交互界面，必须先用 Pencil 设计，确认后再写代码。**

### 工作流顺序

1. **Pencil 设计** — 用 `wechat-miniapp-pencil-design` skill 完成页面设计
   - 主态页面（正常浏览态）
   - 弹窗/底部 sheet 态（如有）
   - 截图验证通过
2. **代码实现** — 对照 Pencil 设计稿还原 WXML/WXSS
3. **云函数** — 视情况部署对应 fn-xxx

### 设计文件位置

```
designs/nanwu-glasses-local.pen   # 南吴眼镜设计文件
```

多状态页面放在同一画布不同 x 坐标（参考 `wechat-miniapp-pencil-design` skill 的坐标规范）。

---

## 充值套餐管理模式

### recharge_packages 集合结构

```javascript
{
  _id: "...",
  name: "充500送50",          // 显示名，可自动生成
  amount: 500,               // 充值金额（Number）
  gift: 50,                  // 赠送金额（Number，默认 0）
  enabled: true,             // 是否启用
  createTime: "2025-...",
  updateTime: "2025-..."
}
```

### 云函数 4 个 action（fn-user）

```javascript
case 'adminListPackages':    return adminListPackages()
case 'adminSavePackage':     return adminSavePackage(data)    // id存在→update，否则→add
case 'adminTogglePackage':   return adminTogglePackage(data)  // {id, enabled}
case 'adminDeletePackage':   return adminDeletePackage(data)  // {id}
```

```javascript
async function adminSavePackage(data) {
  const { id, name, amount, gift } = data
  const doc = {
    name: name || `充${amount}送${gift || 0}`,
    amount: Number(amount), gift: Number(gift) || 0,
    enabled: true, updateTime: new Date().toISOString()
  }
  if (id) {
    await db.collection('recharge_packages').doc(id).update({ data: doc })
  } else {
    doc.createTime = new Date().toISOString()
    await db.collection('recharge_packages').add({ data: doc })
  }
  return { code: 0 }
}
```

### 多 Tab 页面 JS 结构

```javascript
data: {
  activeTab: 'customers',   // 当前 tab
  // tab1 数据
  loading: true,
  customers: [],
  // tab2 数据（懒加载）
  pkgLoading: false,
  packages: [],
},

switchTab(e) {
  const tab = e.currentTarget.dataset.tab
  if (tab === this.data.activeTab) return
  this.setData({ activeTab: tab })
  // 懒加载：首次切换才请求
  if (tab === 'packages' && this.data.packages.length === 0) {
    this.loadPackages()
  }
},
```

### Toggle 启用/停用 WXSS

```css
.pkg-toggle { font-size: 22rpx; font-weight: 600; padding: 8rpx 20rpx; border-radius: 20rpx; }
.toggle-on  { background: #EDFCF2; color: #34A853; }
.toggle-off { background: #F3F4F6; color: #999999; }
```

WXML 中用三元表达式：
```xml
<view class="pkg-toggle {{item.enabled?'toggle-on':'toggle-off'}}"
      bindtap="togglePackage" data-id="{{item._id}}" data-enabled="{{!item.enabled}}">
  {{item.enabled?'启用中':'已停用'}}
</view>
```

---

## 已踩坑汇总

| 坑 | 说明 | 解法 |
|----|------|------|
| tcb deploy 找不到目录 | 默认找 `functions/`，不是 `cloudfunctions/` | 加 `--dir cloudfunctions/fn-xxx` |
| db.command.push 未引入 | 直接用 `cloud.database().command` | `const db = cloud.database(); db.command.push(...)` |
| chooseMedia vs chooseImage 返回结构不同 | tempFiles[0].tempFilePath vs tempFilePaths[0] | 统一用 chooseMedia |
| 云函数 OCR timeout | 默认 3s 不够 | cloudbaserc.json 设 timeout:30 |
| 新页面跳转 page not found | app.json 未注册 | 补充到 pages 数组 |
| 透明色 fill:"none" 报错（Pencil） | 见 wechat-miniapp-pencil-design skill | 用 "#00000000" |
| strokeColor / strokeThickness 无效（Pencil） | Pencil 不支持这两个属性 | 改用实心填充色代替边框效果 |
| `<image>` 不渲染 cloud:// | `<image src>` 不支持 cloud:// 格式 | 用 `wx.cloud.getTempFileURL` 批量转 HTTP URL |
| 返回列表不刷新 | `loadProducts` 只在 `onLoad`，navigateBack 不触发 onLoad | 改到 `onShow` |
| loading 蒙层卡住 | `callFn` 抛出后 `wx.hideLoading()` 未执行 | 用 try/finally 包裹 |
| 表单 wx:if 不显示 | `form.name !== undefined` 在 form={} 时为 false | 改用明确 flag：`isEdit \|\| identified` |
| 图片上传后被 OCR 删除 | 商品图 fileID 和 OCR fileID 复用同一份 | 分开上传两次：`product-images/` + `ocr-temp/` |
| Canvas 旧 API 无法 createImage | `wx.createCanvasContext` 返回的 ctx 没有 createImage | 改用 Canvas 2D 节点模式 + SelectorQuery |
| upload.js sed 中文乱码 | sed 替换含中文的字符串会因编码问题失败 | 用 Read 工具读取后用 Write 工具完整重写 |
| CloudBase 集合不存在报 -502005 | `db.collection().add()` 不会自动建集合，未部署云函数时上传静默失败 | 先部署云函数；再用 tcb CLI 手动插入一条文档触发建表：`tcb db nosql execute --command '[{"TableName":"store_certs","CommandType":"INSERT","Command":"{\"insert\":\"store_certs\",\"documents\":[{\"_init\":true}]}"}]'`，之后删除该文档 |
| 云函数未部署时前端无错误提示 | `callFn` 失败时前端 catch 被吞，用户看不到任何报错 | 云函数部署后必须在日志里验证（`tcb fn log fn-xxx --limit 5`）；前端 callFn 应在 catch 中至少 `console.error` |
