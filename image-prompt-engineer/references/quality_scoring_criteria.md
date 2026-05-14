# Quality Scoring Criteria

Detailed 0-10 point scoring system across 6 dimensions.

## Scoring Dimensions

### 1. Specificity (0-2 points)

**2 points:** Concrete nouns, specific actions, detailed descriptors
- "85mm portrait lens" not "camera"
- "warm studio lighting with soft shadows" not "good lighting"
- "navy blue blazer" not "business attire"

**1 point:** Mostly specific with some vague terms
- Mix of concrete and abstract descriptors

**0 points:** Highly abstract or vague
- "beautiful scene", "nice image", "good quality"

### 2. Structure (0-2 points)

**2 points:** Follows model's optimal structure exactly
- Nano Banana: Subject → Face → Lighting → Camera → Style
- FLUX: Subject → Composition → Style → Mood
- Recraft V3: Subject → Text → Brand → Vector
- SeeDream: Subject → Resolution → Detail → Technical
- SD 3.5: Subject → Typography → Elements → Composition

**1 point:** Partially structured
**0 points:** Unstructured, random keyword order

### 3. Keywords (0-2 points)

**2 points:** Contains 3+ model-specific proven keywords
- Nano Banana: "photorealistic", "natural skin texture", "85mm lens"
- FLUX: "intricate details", "masterful composition", "cinematic"
- Recraft V3: "vector-ready", "sharp text", "scalable design"

**1 point:** 1-2 model-specific keywords
**0 points:** No model-specific keywords

### 4. Completeness (0-2 points)

**2 points:** All elements present
- Subject clearly defined
- Style specified
- Technical specs included
- Context provided

**1 point:** Missing 1-2 elements
**0 points:** Missing 3+ elements

### 5. Use Case Alignment (0-1 points)

**1 point:** Model matches use case optimally
- Nano Banana for portraits: YES
- FLUX for portraits: NO (use Nano Banana instead)
- Recraft V3 for text-heavy: YES
- SeeDream V4 for 4K print: YES

**0 points:** Model mismatch

### 6. Safety (0-1 points)

**1 point:** No restricted content
**0 points:** Contains:
- Celebrity names
- Violence/explicit content
- Copyrighted characters
- Trademarked elements

## Score Interpretation

- **9.0-10.0**: Excellent - Ready for generation
- **7.0-8.9**: Good - Minor improvements possible
- **5.0-6.9**: Fair - Needs refinement
- **0.0-4.9**: Poor - Major issues, suggest rewrite

## Examples

### Example 1: Score 10/10

**Prompt:**
"Professional portrait of confident businesswoman in navy blue blazer, subtle facial features with natural skin texture, warm smile showing authentic expression, soft studio lighting with gentle shadows defining facial structure, photographed with 85mm portrait lens creating shallow depth of field, photorealistic style with lifelike details, neutral gray background"

**Scoring:**
- Specificity: 2/2 (concrete descriptors throughout)
- Structure: 2/2 (follows Nano Banana structure perfectly)
- Keywords: 2/2 ("natural skin texture", "85mm portrait lens", "photorealistic style")
- Completeness: 2/2 (subject, lighting, camera, style all present)
- Use Case Alignment: 1/1 (Nano Banana optimal for portrait)
- Safety: 1/1 (no restricted content)
- **Total: 10/10**

### Example 2: Score 5/10

**Prompt:**
"A nice portrait of a woman"

**Scoring:**
- Specificity: 0/2 (vague: "nice", "woman" with no details)
- Structure: 0/2 (no structure, single sentence)
- Keywords: 0/2 (no model-specific keywords)
- Completeness: 0/2 (missing lighting, camera, style, details)
- Use Case Alignment: 1/1 (if using Nano Banana)
- Safety: 1/1 (no restricted content)
- **Total: 2/10**

**Improvement needed:** Add facial details, lighting setup, camera specs, style keywords
