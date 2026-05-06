---
name: wechat-miniapp-pencil-design
description: >-
  Use when designing WeChat Mini Program UI with Pencil MCP tool.
  Triggers: 微信小程序设计, miniapp UI, .pen 文件设计小程序页面,
  TabBar 设计, 状态栏/导航栏, 登录态/未登录态页面, 小程序多页面布局,
  icon_font 图标, 渐变背景, 品牌卡片, 个人中心页, 管理后台页.
---

# wechat-miniapp-pencil-design

用 Pencil MCP 设计微信小程序 UI 的实战指南。基于南吴眼镜项目积累的坑点与模式。

---

## 微信小程序标准尺寸

```
画布宽度:  375px（设计稿）
屏幕高度:  812px（iPhone X 基准）
StatusBar: h:62px
NavBar:    h:56px
TabBar:    h:95px（含 safe area）
内容区:    812 - 62 - 56 - 95 = 599px（有 TabBar 时）
```

---

## 页面结构模板

每个页面：`layout:vertical` Frame，宽 375，高 812。

```
页面Frame (fill:#F7F8FA, layout:vertical, h:812, w:375)
  ├─ StatusBar     h:62  fill:#深色
  ├─ NavBar        h:56  fill:#深色
  ├─ [主体内容]    height:fill_container
  └─ TabBar        h:95  fill:#深色
```

主体内容用 `height:fill_container` 自动撑满剩余空间。

---

## TabBar 结构模板

```
TabBar (fill:#1A1A2E, h:95, layout:horizontal, padding:[12,21,21,21])
  pill (fill:#ffffff1f, cornerRadius:36, h:62, layout:horizontal,
        padding:4, stroke:{align:"inside",fill:"#ffffff33",thickness:1})
    tab_active (fill:#4A90D9, cornerRadius:26, layout:vertical,
                gap:4, h:fill, w:fill, alignItems:center, justifyContent:center)
      icon_font  fill:#FFFFFF  h:18 w:18
      text       fill:#FFFFFF  fontSize:10 fontWeight:"600"
    tab_inactive (fill:#00000000, cornerRadius:26, layout:vertical,
                  gap:4, h:fill, w:fill, alignItems:center, justifyContent:center)
      icon_font  fill:#ffffff60  h:18 w:18
      text       fill:#ffffff60  fontSize:10
```

常用 iconFontName：`house`（首页）、`person`（我的）、`store`（门店）、`eyeglasses`（眼镜）

---

## 已知 BUG 与规避方法

### BUG 1：新建节点不渲染（跨 session）

**症状**：I() 新建的节点截图中不显示，但 batch_get 能查到。  
**原因**：Pencil 跨 session 渲染缓存问题。  
**解决**：优先 M()（移动现有节点）+ U()（更新属性）改造，避免纯 I() 新建关键可见节点。如必须新建，在同一 batch 里紧跟 U() 触发渲染。

### BUG 2：C()（复制）全局失效

**症状**：C() 报错或无效果。  
**解决**：完全放弃 C()，用 M() 移动现有节点 + I() 新建替代。

### BUG 3：fill:"none" 报错

**解决**：透明色统一用 `"#00000000"`，不用 `"none"`。

### BUG 4：icon_font 节点不接受 cornerRadius / padding

**解决**：icon_font 类型只设 `iconFontName`、`fill`、`height`、`width`，其余属性报错。需要带背景色的图标，外套一个 frame。

### BUG 5：R() 后原节点 ID 消失

**症状**：R("oldId",...) 后，新节点用 binding 名引用；下一次 batch 中不能再用 oldId。  
**解决**：R() 操作后的节点 ID 从 batch result 的 binding 里取，分两次 batch 操作。

### BUG 6：layout 容器内 rectangle 无法撑满做背景

**症状**：在 layout:vertical 的 frame 里放 fill_container 的 rectangle，截图中不显示。  
**解决**：改用 `layout:none` + 绝对坐标，或用 image() 直接设容器的图片 fill（frame 不支持 image fill）。背景图只能放在 `type:"rectangle"` 节点上。

### BUG 7：本地图片路径在截图中不渲染

**症状**：image() 设置本地路径后，get_screenshot 显示灰色空白。  
**原因**：截图引擎无法访问本地文件系统图片。  
**解决**：截图验证时改用渐变色 + icon 装饰代替；实际 .pen 文件中图片路径已写入，导出/实现时会正常显示。或将图片转为 base64 内联（大图不推荐）。

### BUG 8：M() 第三参数必须是数字

**症状**：`M("id","parent","siblingId")` 报错。  
**解决**：第三参数只接受数字索引（0-based），如 `M("id","parent",0)`。

### BUG 9：`height:"auto"` 无效

**症状**：`U("id", {height:"auto"})` 报错 `Invalid properties: /height expected one of: number, "$variable", sizing behavior (fit_content or fill_container...)`。  
**解决**：只允许 `"fit_content"`、`"fill_container"` 或数字，不接受 `"auto"`。

### BUG 10：大量 U() 结构改造后页面整体变空白

**症状**：对同一个页面 Frame 执行了大量 M() 重排 + U() 属性变更（如 10+ 个子节点移位、重命名、换父级）后，截图显示整个页面空白，但 batch_get 仍能查到所有节点。  
**原因**：Pencil 的渲染缓存不只对 I() 失效——大规模结构改造会让父 Frame 的渲染缓存失效。即使节点在上一 session 正常渲染过，经过大规模重排后也会消失。  
**解决**：
- **最小改动原则**：只对需要改内容（文本/颜色）的节点做 U()，不要同时做大量 M() 移位
- **已渲染稳定的节点**：只更新 content/fill/fontSize 等属性，不改变父子结构
- **结构改动过多时**：接受无法截图验证，依赖代码实现；或新开一个新 Frame 从头设计

---

## 多状态页面设计模式

同一功能页面的不同状态（登录/未登录、空状态/有数据）放在**同一画布不同 x 坐标**：

```
未登录首页:  x:-415   （左侧备用位）
已登录首页:  x:0      （主画布起点）
门店页:      x:415
我的页:      x:1245   （间距 830，留出一页宽 + 空间）
管理页1:     x:2075
```

命名规范：`name:"首页-未登录"`、`name:"首页-已登录"`

---

## 渐变背景写法

```javascript
fill:{
  type:"gradient",
  gradientType:"linear",
  rotation:135,
  colors:[
    {color:"#1A1A2E", position:0},
    {color:"#16213E", position:0.5},
    {color:"#0F3460", position:1}
  ]
}
```

---

## Hero 区（Banner）绝对定位模式

当需要图片/渐变背景 + 叠加文字时，改用 `layout:none`：

```javascript
// 1. 容器改为绝对定位
U("heroFrame", {layout:"none", fill:"#00000000"})

// 2. 背景层（渐变或图片矩形）
U("bgRect", {x:0, y:0, width:375, height:200, fill:{...gradient...}})

// 3. 蒙层（可选）
U("overlay", {x:0, y:0, width:375, height:200, fill:"#00000066"})

// 4. 文字层（绝对定位到底部）
U("titleFrame", {x:20, y:142, width:335, height:28})
U("subtitleFrame", {x:20, y:170, width:335, height:20})
```

---

## 品牌卡片模式（四格）

```
brandCard (fill:#FFFFFF, cornerRadius:12, layout:vertical, gap:12, padding:[14,14])
  brandTitle (layout:horizontal, justifyContent:space_between)
    label "青少年防控专区"  fill:#1A1A2E  fontSize:15  fontWeight:"700"
    more  "查看全部 >"     fill:#4A90D9  fontSize:12
  brandList (layout:horizontal, gap:8, width:fill_container)
    brand1~4 (fill:#EEF4FB, cornerRadius:10, layout:vertical, gap:6,
              padding:[10,8], width:74, alignItems:center)
      name  fontSize:13  fontWeight:"700"
      sub   fontSize:11  fill:#4A90D9
```

注意：brandList 的子项必须用**固定宽度**（如 74），不能用 fill_container，否则 Circular layout 报错。

---

## 登录 CTA 组件模式

```
ctaBar (fill:#1A1A2E, cornerRadius:12, layout:horizontal,
        padding:[16,20], alignItems:center, justifyContent:space_between)
  textArea (layout:vertical, gap:2, width:fill_container)
    title  "登录后查看您的配镜档案和订单"
           fill:#FFFFFF  fontSize:14  fontWeight:"600"
    sub    "记录视力变化，掌握孩子眼健康动态"
           fill:#ffffff99  fontSize:12
  chevron (type:icon_font, iconFontName:"chevron-right", fill:#FFFFFF, h:18, w:18)
```

---

## 简约风配色方案（推荐）

| 用途 | 色值 |
|------|------|
| 页面背景 | `#F7F8FA` |
| 主色（深色 bar/按钮） | `#1A1A2E` |
| 品牌蓝（强调/active） | `#4A90D9` |
| 卡片背景 | `#FFFFFF` |
| 品牌卡片背景 | `#EEF4FB` |
| 主文字 | `#1A1A2E` |
| 次文字 | `#666666` |
| 三级文字 | `#999999` |
| 白色透明（TabBar inactive） | `#ffffff60` |
| 深色蒙层 | `#00000066` |

---

## Tab 导航栏深色胶囊样式（已验证）

管理页面常用的双 tab 切换条（黑底白文/白底黑文交换）：

```javascript
// 容器：深色背景
tabBar = I(parent, {type:"frame", fill:"#1A1A2E", layout:"horizontal",
           alignItems:"center", padding:[10,24,10,24], gap:0,
           width:"fill_container", height:"fit_content"})

// 激活 tab：白底深色字
activeTab = I(tabBar, {type:"frame", fill:"#FFFFFF", cornerRadius:20,
              layout:"vertical", alignItems:"center", justifyContent:"center",
              padding:[14,0], height:"fit_content"})
I(activeTab, {type:"text", content:"客户充值", fill:"#1A1A2E", fontSize:13, fontWeight:"700"})

// 非激活 tab：透明底浅色字
inactiveTab = I(tabBar, {type:"frame", fill:"#00000000", cornerRadius:20,
               layout:"vertical", alignItems:"center", justifyContent:"center",
               padding:[14,0], height:"fit_content"})
I(inactiveTab, {type:"text", content:"套餐设置", fill:"rgba(255,255,255,0.5)", fontSize:13})
```

对应 WXSS：
```css
.tab-bar { background: #1A1A2E; display: flex; padding: 10rpx 24rpx; }
.tab-item { flex: 1; text-align: center; padding: 14rpx 0; border-radius: 32rpx; color: rgba(255,255,255,0.5); }
.tab-active { background: #FFFFFF; color: #1A1A2E; font-weight: 700; }
```

---

## 空容器文字迁移模式（M() 偷用已渲染文本）

当目标容器没有文字子节点（空 frame），而需要在其中显示数字/标签时，不要 I() 新建文字（新建节点跨 session 不渲染），改用 M() 从其他已渲染位置"偷"一个文字节点过来：

```javascript
// 1. 先 batch_get 找到文档中某个已渲染的 text 节点 ID（如来自其他 tab 内容区）
// 2. M() 移过去，设置正确的 index
M("已渲染textID", "目标容器ID", 0)
// 3. 立即 U() 更新内容
U("已渲染textID", {content: "¥1234.00", fill:"#FFFFFF", fontSize:40, fontWeight:"700"})
```

典型场景：Stats 数据卡（总余额/客户数/累计充值）的数字区域初始无 text 子节点时使用此方法。

---

## 操作效率技巧

1. **批量更新颜色**：用 `replace_all_matching_properties` 替换全局色值，比逐节点 U() 快得多
2. **先截图再操作**：每完成一个区域先 get_screenshot，验证后再继续，避免积累问题
3. **节点 ID 记录**：重要节点 ID 记录在会话上下文，跨 batch 引用时不要靠 binding（binding 跨 batch 失效）
4. **batch 单次上限**：每次 batch_design 最多 25 个操作，复杂页面分段完成
5. **M() 优先**：需要复用结构时优先 M() 移动现有节点，比新建渲染更可靠
6. **最小结构改动**：对已渲染页面只做 U()（内容/颜色/字号），避免大量 M() 重排，否则触发 BUG 10

---

## 已验证的页面设计顺序

1. 定义页面画布位置（U 根 Frame 的 x/y）
2. StatusBar + NavBar（从已有页面 M() 过来改造）
3. 主体内容区（height:fill_container）
4. TabBar（最后加，确保高度撑满正确）
5. 截图验证整体比例
6. 填充内容卡片
7. 最终截图确认

---

## WIP：持续完善中

本 skill 随南吴眼镜项目设计进度持续更新。每次发现新坑点立即补充到"已知 BUG"章节。
