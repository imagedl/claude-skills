# Model Keyword Patterns

Comprehensive keyword libraries and transformation rules for all 5 supported image generation model families.

## Table of Contents

1. [Nano Banana (Gemini 2.5 Flash Image)](#nano-banana)
2. [FLUX 1.1 Suite](#flux-11-suite)
3. [Recraft V3](#recraft-v3)
4. [SeeDream V3/V4](#seedream-v3v4)
5. [SD 3.5 Large/Medium](#sd-35-largemedium)

---

## Nano Banana (Gemini 2.5 Flash Image)

**Best For:** Photorealistic portraits, professional headshots, product photography with human models, face-centric compositions

### Optimal Prompt Structure

```
Subject → Facial Details → Lighting → Environment → Camera → Style
```

### Required Keywords by Category

**Photorealism Foundation:**
- photorealistic
- lifelike
- natural skin texture
- realistic lighting
- authentic details

**Facial Feature Descriptors:**
- subtle facial features
- natural expression
- micro-expressions
- authentic skin tone
- gentle smile
- confident expression
- warm gaze
- expressive eyes
- natural wrinkles (if appropriate)
- skin pores visible (for extreme realism)

**Lighting Specifications:**
- soft natural light
- golden hour
- studio lighting
- diffused light
- gentle shadows
- warm light
- cool daylight
- backlit
- rim lighting
- Rembrandt lighting
- butterfly lighting
- split lighting

**Camera Technical Details:**
- portrait lens
- 85mm lens
- 50mm lens
- 135mm lens
- shallow depth of field
- bokeh background
- f/1.4 aperture
- f/2.8 aperture
- professional photography
- medium format
- full-frame sensor

**Face Preservation Terms:**
- maintain facial structure
- preserve identity
- realistic proportions
- accurate facial geometry
- natural bone structure

### Transformation Rules

1. **Always add specific facial feature descriptors** - Never leave face description vague
2. **Include detailed lighting setup** - Direction, quality, and mood
3. **Specify camera equipment** - Lens focal length and aperture effect
4. **Add texture details** - Skin, fabric, environment materials
5. **Use "photorealistic" or "lifelike" explicitly** - Anchor the style

### Good vs Bad Examples

**Bad:**
```
"A woman smiling"
```

**Good:**
```
"Professional portrait of a woman in business attire, subtle facial features with
natural skin texture, soft smile showing authentic expression, warm studio lighting
with gentle shadows, photographed with 85mm portrait lens, photorealistic style,
shallow depth of field, neutral gray background"
```

### Keyword Frequency Guidelines

- Photorealism keywords: 2-3 per prompt
- Facial descriptors: 3-5 per prompt
- Lighting terms: 2-3 per prompt
- Camera specs: 2-3 per prompt

---

## FLUX 1.1 Suite

**Best For:** Artistic compositions, concept art, digital illustration, creative marketing visuals

### Variant Selection Guide

**FLUX 1.1 Pro Ultra** (Use for):
- Complex multi-element scenes
- Highest detail requirements
- Artistic masterworks
- Maximum quality needed

**FLUX 1.1 Pro** (Use for):
- High-quality artistic renders
- Balanced detail and cost
- Professional creative work
- General artistic projects

**FLUX 1.1 Pro Redux** (Use for):
- Style-consistent variations
- Reference image style transfer
- Maintaining brand consistency
- Iterating on existing concept

**FLUX Dev** (Use for):
- Creative balance
- Faster generation needed
- Good quality acceptable
- Budget-conscious projects

**FLUX Schnell** (Use for):
- Speed-critical prototyping
- Simple compositions
- Rough concept visualization
- Rapid iteration

**FLUX Realism** (Use for):
- Photographic realism (non-face-focused)
- Natural scenes without human subjects
- Documentary-style imagery
- Realistic textures and materials

### Optimal Prompt Structure

```
Subject → Composition → Style → Mood → Technical Specs → Variant
```

### Required Keywords by Variant

**Pro/Pro Ultra Keywords:**
- intricate details
- masterful composition
- fine art quality
- complex lighting
- elaborate scene
- exceptional detail
- artistic masterwork
- premium quality
- sophisticated rendering

**Dev Keywords:**
- creative rendering
- artistic style
- balanced composition
- expressive details
- stylized approach
- imaginative interpretation

**Schnell Keywords:**
- clean composition
- simple style
- efficient design
- streamlined aesthetic
- focused concept

**Realism Keywords:**
- photographic
- realistic textures
- natural lighting
- documentary style
- authentic materials
- lifelike rendering

### Composition Terms

- rule of thirds
- golden ratio
- leading lines
- symmetrical
- asymmetrical balance
- dynamic composition
- foreground interest
- depth layers
- visual flow
- focal point
- negative space

### Mood & Atmosphere Keywords

- ethereal atmosphere
- magical ambiance
- dramatic mood
- serene environment
- intense energy
- mystical quality
- cinematic feel
- dreamy atmosphere
- epic scale
- intimate setting

### Artistic Style Descriptors

- digital painting
- concept art
- impressionist style
- surrealist approach
- fantasy art
- sci-fi aesthetic
- painterly textures
- brush strokes visible
- mixed media
- contemporary art

### Transformation Rules

1. **Choose variant based on complexity** - Pro Ultra for complex, Schnell for simple
2. **Add composition descriptors** - Rule of thirds, leading lines, symmetry
3. **Include mood/atmosphere keywords** - Set emotional tone
4. **Specify art style** - If not photorealistic
5. **Use technical photography terms** - Depth of field, focal length, lighting ratios

### Keyword Frequency Guidelines

- Complexity keywords (intricate, masterful): 2-3 per prompt
- Composition terms: 2-3 per prompt
- Mood keywords: 1-2 per prompt
- Style descriptors: 2-3 per prompt

---

## Recraft V3

**Best For:** Logo design, marketing materials with text, brand identity, infographics, vector illustrations

### Optimal Prompt Structure

```
Subject → Text Elements → Brand Style → Composition → Vector Format
```

### Required Keywords by Category

**Text Rendering Keywords:**
- sharp text
- crisp typography
- legible text overlay
- integrated text elements
- text composition
- typographic design
- clear lettering
- readable font
- text-focused design

**Vector Quality Keywords:**
- clean lines
- vector-ready
- scalable design
- sharp edges
- precise geometry
- vector format
- scalable vector graphics
- SVG output
- resolution-independent

**Brand Design Terms:**
- professional branding
- corporate identity
- logo design
- brand consistency
- visual identity
- brand guidelines
- trademark quality
- commercial design

**Composition & Layout:**
- balanced layout
- hierarchical design
- visual flow
- white space
- organized composition
- structured layout
- grid-based design
- centered composition
- asymmetric balance

**Typography Styles:**
- sans-serif
- serif font
- script typography
- decorative font
- bold lettering
- condensed type
- geometric typeface
- modern typography
- classic font

### Text Specification Rules

1. **Always specify text content explicitly** - Use quotes: "COMPANY NAME"
2. **Include typography style** - Sans-serif, serif, decorative, etc.
3. **Add color palette specifications** - Hex codes or color names
4. **Mention vector format if output will be resized** - Scalable, SVG, vector-ready
5. **Describe text placement and integration** - Primary, secondary, accent
6. **Use design hierarchy terms** - Primary element, supporting text, accent

### Color Specification Patterns

```
"gradient blue (#0066FF to #00CCFF)"
"navy blue (#001F3F) and gold (#FFD700)"
"monochromatic gray scale"
"vibrant rainbow palette"
"corporate blue and white"
"red (#FF0000) accent on white background"
```

### Transformation Rules

1. **Text content must be quoted** - "TEXT GOES HERE"
2. **Specify font characteristics** - Bold, sans-serif, modern, etc.
3. **Include explicit color palette** - Hex codes or specific color names
4. **Mention vector output** - "vector-ready", "scalable design"
5. **Describe layout structure** - Balanced, hierarchical, grid-based

### Good vs Bad Examples

**Bad:**
```
"Logo with text INNOVATE"
```

**Good:**
```
"Professional business logo with integrated text 'INNOVATE', clean geometric shapes
forming abstract lightbulb symbol, sharp sans-serif typography in navy blue (#001F3F)
and gold (#FFD700), balanced composition with ample white space, vector-ready design
with crisp edges, scalable format, modern corporate identity style"
```

### Keyword Frequency Guidelines

- Text rendering keywords: 2-3 per prompt
- Vector quality terms: 2-3 per prompt
- Brand descriptors: 2-3 per prompt
- Typography specifications: 2-3 per prompt

---

## SeeDream V3/V4 (MiniMax)

**Best For:** Print production (posters, billboards), architectural visualization, product photography requiring extreme detail, fine art reproduction

### Model Version Selection

**SeeDream V3:**
- Maximum resolution: 2048x2048
- Speed: Faster generation (15-30 seconds)
- Use for: Web-quality high-resolution images
- Cost: Lower than V4

**SeeDream V4:**
- Maximum resolution: 4096x4096
- Speed: Slower generation (30-60 seconds)
- Use for: Print production, billboards, large-format
- Cost: Higher than V3

### Optimal Prompt Structure

```
Subject → Resolution Specs → Detail Density → Technical Requirements → Language
```

### Required Keywords by Category

**Resolution Specifications:**
- 4K ultra-high-resolution (for V4)
- 2K high-resolution (for V3)
- 2048x2048 (V3 target)
- 4096x4096 (V4 target)
- extreme detail density
- ultra-detailed
- high-fidelity

**Detail Density Descriptors:**
- intricate details
- fine textures
- crisp clarity
- pixel-perfect
- microscopic detail
- minute details
- elaborate texturing
- hyper-detailed
- meticulous craftsmanship

**Technical Quality Terms:**
- high dynamic range
- HDR lighting
- color accuracy
- color-correct
- sharp focus throughout
- professional quality
- studio-grade
- print-ready
- publication-quality
- archival quality

**Material & Texture Terms:**
- visible grain structure
- fabric weave visible
- wood grain detail
- metal finishing (brushed, polished, matte)
- glass reflections
- surface imperfections
- material authenticity
- tactile quality

**Production Context:**
- large-format printing
- billboard production
- gallery exhibition
- museum quality
- commercial print
- poster reproduction
- architectural rendering
- product catalog

### Language Support Keywords

- English text (specify if text present)
- Chinese text (specify if text present)
- bilingual text elements (if applicable)
- multilingual design

### Transformation Rules

1. **Always specify target resolution explicitly** - 2048 or 4096
2. **Add detail density descriptors for every element** - Fine, intricate, microscopic
3. **Include material texture descriptions** - Visible weave, grain, surface quality
4. **Specify lighting precision** - HDR, color temperature, direction
5. **Mention print production if applicable** - Billboard, large-format, gallery
6. **Add language specification if text included** - English, Chinese, bilingual

### Good vs Bad Examples

**Bad:**
```
"High-res room interior"
```

**Good:**
```
"Architectural interior rendering at 4096x4096 ultra-high-resolution, modern
minimalist living room with floor-to-ceiling windows, intricate wood grain
textures on furniture, crisp reflections on polished marble floor, fine fabric
weave visible on cushions, professional architectural photography quality, high
dynamic range lighting from golden hour sun, pixel-perfect clarity, extreme
detail density for print production"
```

### Keyword Frequency Guidelines

- Resolution specs: 1-2 per prompt (explicit numbers)
- Detail density terms: 3-5 per prompt
- Texture descriptors: 3-5 per prompt (per major element)
- Technical quality keywords: 2-3 per prompt

---

## SD 3.5 Large/Medium (Stability AI)

**Best For:** Book covers with integrated titles, marketing materials with complex compositions, concept art with multiple subjects, illustrations with typographic elements

### Variant Selection Guide

**SD 3.5 Large** (Use for):
- Complex multi-element scenes
- Intricate compositions with 3+ subjects
- Detailed background + foreground coordination
- Typography + imagery integration
- 8B parameter model (maximum capability)

**SD 3.5 Large Turbo** (Use for):
- Same as Large but faster (4x speed)
- Reduced inference steps
- Good for iteration and prototyping
- Acceptable quality trade-off for speed

**SD 3.5 Medium** (Use for):
- Simpler prompts (1-2 subjects)
- Single-focus compositions
- Cost-effective option
- 2.5B parameter model
- Faster generation than Large

### Optimal Prompt Structure

```
Subject → Typography → Complex Elements → Scene Composition → Variant
```

### Required Keywords by Category

**Typography Integration:**
- integrated text
- typographic elements
- legible text overlay
- text composition
- title treatment
- headline integration
- font design
- text as design element

**Complexity & Multi-Element:**
- multiple subjects
- layered composition
- complex scene
- detailed elements
- intricate arrangement
- multi-focal composition
- elaborate setting
- coordinated elements

**Spatial Relationships:**
- foreground elements
- midground detail
- background depth
- atmospheric perspective
- spatial hierarchy
- depth layering
- overlapping elements
- z-axis composition

**Style Unity:**
- digital art style
- concept art approach
- illustration style
- artistic rendering
- painterly quality
- unified aesthetic
- consistent style
- coherent visual language

**Technical Composition:**
- balanced lighting across elements
- coherent perspective
- unified color grading
- harmonious composition
- visual cohesion
- integrated design

### Text Content Specification

When text is required in output:
```
"integrated title text 'BOOK TITLE' in bold serif font"
"overlay text 'HEADLINE' in sans-serif uppercase"
"decorative text 'Subtitle' in script style"
```

### Transformation Rules

1. **Choose variant based on prompt complexity** - Large for multi-element, Medium for simple
2. **Include text content explicitly if present** - Quoted text with style description
3. **Describe spatial relationships between elements** - Foreground, midground, background
4. **Add atmospheric effects** - Fog, lighting, depth cues
5. **Specify art style** - Concept art, digital painting, illustration
6. **Use compositional terms** - Layered, atmospheric perspective, spatial hierarchy

### Element Count Guidelines

**SD 3.5 Large:**
- 3-8 distinct elements/subjects
- Complex spatial relationships
- Multiple lighting sources
- Detailed foreground + background

**SD 3.5 Medium:**
- 1-2 primary subjects
- Simple background
- Single lighting source
- Focused composition

### Good vs Bad Examples

**Bad:**
```
"Fantasy scene with dragon and knight"
```

**Good:**
```
"Epic fantasy book cover composition with integrated title text 'THE DRAGON'S OATH'
in ornate golden serif font at top, multiple subjects including armored knight in
dramatic pose in foreground, majestic dragon circling ancient stone castle in
background, layered atmospheric perspective with misty mountains, complex lighting
with dramatic sunset rays breaking through clouds, digital art style with painterly
textures, coherent fantasy aesthetic across all elements, rich color grading blending
warm oranges with cool blues, spatial depth from foreground to distant peaks"
```

### Keyword Frequency Guidelines

- Typography keywords (if text present): 2-3 per prompt
- Complexity terms: 2-3 per prompt
- Spatial relationship descriptors: 3-4 per prompt
- Style unity keywords: 2-3 per prompt

---

## Cross-Model Keyword Guidelines

### Universal Quality Modifiers (Use sparingly, model-specific terms preferred)

- high quality
- detailed
- professional
- premium
- exceptional
- masterful
- expert

### Universal Composition Terms (Applicable to all models)

- centered
- off-center
- rule of thirds
- symmetrical
- asymmetrical
- balanced
- dynamic
- static
- minimal
- complex

### Universal Lighting Terms (Applicable to all models)

- natural light
- artificial light
- golden hour
- blue hour
- overcast
- direct sunlight
- diffused light
- hard light
- soft light

### Avoid These Generic/Weak Terms

- "good quality" → Use model-specific quality terms instead
- "nice lighting" → Specify lighting type, direction, quality
- "beautiful" → Too vague, describe specific aesthetic qualities
- "amazing" → Meaningless, use concrete descriptors
- "perfect" → Not actionable, specify what makes it perfect

---

## Keyword Combination Strategies

### Layering Keywords for Maximum Impact

**Pattern: Base + Specification + Technical**
```
Base: "portrait"
Specification: "professional business portrait"
Technical: "professional business portrait with natural skin texture,
           photographed with 85mm lens, photorealistic"
```

### Avoiding Keyword Redundancy

**Redundant (wasteful):**
```
"high quality, premium quality, exceptional quality, professional quality"
```

**Optimized (effective):**
```
"premium professional quality with meticulous attention to detail"
```

### Model-Specific Keyword Density

**Nano Banana:** 15-20 keywords total
**FLUX 1.1:** 12-18 keywords total
**Recraft V3:** 10-15 keywords total (+ explicit text content)
**SeeDream V4:** 18-25 keywords total (detail-dense)
**SD 3.5 Large:** 20-30 keywords total (complex scenes)

---

## Update History

**Version 1.0.0** (2025-01-11)
- Initial comprehensive keyword library
- All 5 model families documented
- Transformation rules established
- Good/bad examples included
