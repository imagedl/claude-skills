---
name: image-prompt-engineer
description: Transform natural language into model-optimized image generation prompts for Nano Banana, FLUX 1.1, Recraft V3, SeeDream V3/V4, and SD 3.5. Includes quality scoring (0-10), safety/technical warnings, auto-determined specs (resolution, aspect ratio, format), and JSON output for API integration.
---

## Purpose

Transform natural language descriptions into production-ready, model-optimized image generation prompts. This skill bridges the gap between how humans describe images ("a cozy coffee shop on a rainy day") and how AI models generate best results ("cozy artisan coffee shop, rain-streaked windows, warm amber lighting, photorealistic, 8k uhd, shallow depth of field").

The skill supports five leading image generation model families—Nano Banana (photorealism specialist), FLUX 1.1 (artistic versatility), Recraft V3 (text-in-image precision), SeeDream V3/V4 (high-resolution powerhouse), and Stable Diffusion 3.5 (complex scene handling). Each model has unique strengths, keyword patterns, and technical requirements that dramatically impact output quality.

Beyond prompt transformation, this skill provides:
- Quality scoring system (0-10 scale across 6 dimensions) to validate prompt effectiveness before generation
- Automated warning detection for safety issues, quality problems, technical mismatches, and optimization opportunities
- Technical specification auto-detection (resolution, aspect ratio, format, model variant) based on use case analysis
- Structured JSON output ready for direct API integration with image generation services

Use this skill when you need consistent, high-quality prompt engineering at scale, when integrating image generation into applications, or when optimizing prompts for specific model capabilities.

## When to Use This Skill

Claude should invoke this skill when:

- User provides a natural language image description and needs it transformed for a specific model (Nano Banana, FLUX 1.1, Recraft V3, SeeDream, SD 3.5)
- User requests quality validation or scoring of an existing image generation prompt
- User needs to determine optimal technical specifications (resolution, aspect ratio, format) for an image generation task
- User wants to compare which model is best suited for their image generation requirements
- User is building an application that integrates with image generation APIs and needs structured prompt output
- User describes an image concept and needs safety/quality warnings before generating
- User has a prompt that underperforms and needs optimization with model-specific keywords
- User needs batch processing of multiple image descriptions with consistent quality standards

## Supported Models Overview

**Nano Banana** - Photorealism specialist optimized for lifelike images of people, products, and environments. Excels at natural lighting, skin texture, and real-world materials. Best for commercial photography, product shots, and realistic portraits.

**FLUX 1.1** - Artistic versatility champion with exceptional style range from anime to oil paintings. Superior prompt adherence and creative interpretation. Best for artistic content, concept art, and stylized illustrations.

**Recraft V3** - Text-in-image precision leader with industry-best text rendering capabilities. Handles typography, logos, and branded content flawlessly. Best for marketing materials, social graphics, and designs requiring accurate text.

**SeeDream V3/V4** - High-resolution powerhouse supporting up to 2048x2048 output with exceptional detail preservation. V4 offers enhanced quality and faster generation. Best for large-format prints, detailed landscapes, and professional photography.

**Stable Diffusion 3.5** - Complex scene handling expert with superior multi-object composition and spatial reasoning. Excels at detailed prompts with multiple subjects and intricate relationships. Best for elaborate scenes, storytelling images, and complex compositions.

## Prompt Transformation Process

The transformation follows a five-stage workflow:

**Stage 1: Intent Analysis**
Parse the natural language input to identify core elements: primary subject, scene context, desired style, mood/atmosphere, technical requirements (if specified), and any special features (text, specific composition). Extract implicit requirements (e.g., "product photography" implies commercial lighting, shallow depth of field, clean background).

**Stage 2: Model Selection**
Determine optimal model based on requirements. Match photorealism needs to Nano Banana, artistic styles to FLUX 1.1, text requirements to Recraft V3, high-resolution demands to SeeDream, and complex multi-object scenes to SD 3.5. If user specifies a model, validate compatibility with their requirements and flag mismatches.

**Stage 3: Keyword Application**
Apply model-specific keyword patterns from the extensive library (see references/model_keyword_patterns.md). Add quality boosters (e.g., "8k uhd", "highly detailed", "professional photography"), style keywords (e.g., "cinematic lighting", "volumetric fog", "golden hour"), technical terms (e.g., "shallow depth of field", "bokeh", "ray tracing"), and negative prompt elements to suppress common artifacts.

Structure keywords in optimal order for the target model: typically subject description first, then style/quality modifiers, then technical specifications, then atmosphere/mood elements. Use comma separation for most models, with appropriate emphasis syntax where supported.

**Stage 4: Quality Validation**
Score the transformed prompt across six dimensions (0-10 scale):

- Clarity (2.0x weight): Keyword precision and specificity, avoiding vague terms
- Completeness (1.5x weight): Coverage of subject, style, lighting, composition, technical details
- Optimization (1.5x weight): Model-specific keyword usage, quality boosters, negative prompts
- Coherence (1.0x weight): Logical consistency between elements, no contradictions
- Technical Validity (1.0x weight): Specification alignment with model capabilities
- Safety (1.0x weight): Content policy compliance, appropriate content filters

Calculate weighted average for overall quality score. Scores below 7.0 trigger optimization recommendations.

**Stage 5: Output Generation**
Compile structured JSON output containing:
- Optimized prompt text (positive and negative where applicable)
- Selected model and variant (standard/pro/turbo)
- Quality score breakdown and overall rating
- Warning array (safety, quality, technical, optimization categories)
- Technical specifications (resolution, aspect ratio, format, seed, steps, guidance scale)
- Metadata (original input, transformation rationale, model selection reasoning)

## Quality Validation System

The 0-10 scoring system evaluates prompt effectiveness before generation:

**Clarity (0-10, weight 2.0x)**: Measures keyword precision and specificity. High scores use concrete descriptors ("golden hour sunlight through rain-streaked windows" vs "nice lighting"). Penalizes vague terms (beautiful, nice, good) and ambiguous phrasing. References quality_scoring_criteria.md for full rubric.

**Completeness (0-10, weight 1.5x)**: Assesses coverage of critical elements. Strong prompts describe subject, setting, style, lighting, composition, technical parameters, and mood. Identifies missing elements that would improve output (e.g., lacks lighting direction, no style specification, undefined background).

**Optimization (0-10, weight 1.5x)**: Evaluates model-specific enhancement usage. Checks for quality boosters appropriate to the model (Nano Banana: "photorealistic, 8k uhd"; FLUX: "masterpiece, best quality"; Recraft: "clean vector graphics"). Verifies negative prompts address model-specific weaknesses.

**Coherence (0-10, weight 1.0x)**: Validates logical consistency. Detects contradictions ("bright sunny day" + "nighttime"), style conflicts ("photorealistic" + "anime style"), and implausible combinations ("underwater desert landscape"). Flags compositional issues.

**Technical Validity (0-10, weight 1.0x)**: Confirms specification compatibility. Verifies resolution is supported by model, aspect ratio is valid, requested features exist (some models don't support negative prompts), and parameter ranges are within limits (guidance scale, steps).

**Safety (0-10, weight 1.0x)**: Screens for content policy compliance. Flags potentially sensitive subjects, content that violates platform policies, requests for copyrighted characters/brands without clear fair use, and prompts likely to generate problematic output.

Overall score = (Clarity × 2.0 + Completeness × 1.5 + Optimization × 1.5 + Coherence × 1.0 + Technical × 1.0 + Safety × 1.0) / 8.0

Scores of 7.0-7.9 indicate good quality, 8.0-8.9 excellent, 9.0+ exceptional. Scores below 7.0 receive optimization suggestions.

## Warning Classification

Warnings are categorized into four types with varying severity levels:

**Safety Warnings** (severity: high)
- Content policy violations (violence, explicit content, illegal activities)
- Sensitive topics requiring careful handling (political figures, religious imagery, cultural appropriation)
- Copyright/trademark concerns (branded characters, celebrity likenesses without clear fair use)
- Potentially harmful stereotypes or biased representations

Examples:
- "Prompt requests copyrighted character (Disney princess) without transformative context"
- "Contains sensitive political content that may violate platform policies"
- "Depicts potentially harmful stereotypes; consider more respectful representation"

**Quality Warnings** (severity: medium)
- Vague descriptions lacking specificity ("beautiful landscape", "nice portrait")
- Conflicting elements creating coherence issues ("sunny rainstorm", "realistic cartoon")
- Underspecified technical details (no lighting, composition, or style guidance)
- Overly complex prompts that may confuse the model (100+ keywords)

Examples:
- "Description is vague; specify lighting type, time of day, and style for better results"
- "Conflicting styles detected: 'photorealistic' and 'anime style' are incompatible"
- "Prompt lacks composition guidance; add framing terms like 'close-up' or 'wide shot'"

**Technical Warnings** (severity: medium-high)
- Resolution mismatches (requesting 4K from model limited to 1024x1024)
- Unsupported features (negative prompts on models that don't support them)
- Aspect ratio incompatibilities (requesting 16:9 when model only supports 1:1, 4:3)
- Parameter values outside valid ranges (guidance scale > maximum)

Examples:
- "Requested resolution 2048x2048 exceeds model limit of 1024x1024; use SeeDream V3 instead"
- "Recraft V3 does not support negative prompts; suggestions ignored"
- "Aspect ratio 21:9 unsupported; closest available is 16:9"

**Optimization Warnings** (severity: low)
- Underutilized model capabilities (Recraft V3 prompt without text rendering)
- Better model available for use case (photorealism request on FLUX → suggest Nano Banana)
- Missing quality boosters that would improve output
- Inefficient keyword ordering for target model

Examples:
- "Consider Nano Banana for photorealism; FLUX 1.1 optimized for artistic styles"
- "Recraft V3 selected but no text rendering requested; consider FLUX 1.1 instead"
- "Add quality boosters: '8k uhd', 'highly detailed', 'professional photography'"

Warnings include severity level, category, message, and recommended action. Critical safety warnings may block generation.

## Technical Specification Auto-Detection

The skill automatically determines optimal specifications based on use case analysis:

**Resolution Selection**
Analyze subject complexity and output intent: social media posts (512x512 to 1024x1024), print materials (1536x1536 to 2048x2048), web banners (1024x512 landscape), mobile wallpapers (1024x1792 portrait). Match resolution to model capabilities—don't request 2048x2048 from models capped at 1024x1024. Default to model's sweet spot resolution for best quality/speed balance.

**Aspect Ratio Detection**
Parse composition requirements: portraits default to 3:4 or 2:3, landscapes to 16:9 or 3:2, product shots to 1:1, social graphics to platform specs (Instagram 1:1, Twitter 16:9, Pinterest 2:3). Validate ratio is supported by target model. If unsupported, select closest alternative and warn user.

**Format Determination**
Select output format based on use case: PNG for images requiring transparency or high quality preservation, JPEG for photographs and web optimization, WebP for modern web applications needing compression. Consider downstream usage (print = PNG, web = JPEG/WebP, editing = PNG).

**Model Variant Selection**
Choose between standard/pro/turbo variants based on requirements: standard for balanced quality/speed, pro for maximum quality when time permits, turbo for rapid iteration or high-volume generation. Default to standard unless user specifies quality priority or speed constraints.

**Parameter Auto-Configuration**
Set generation parameters within model limits: guidance scale (typically 7-12 for balanced prompt adherence), steps (20-30 for standard quality, 50+ for pro), seed (random unless user needs reproducibility). Apply model-specific best practices from technical_specs_tables.md.

All auto-detected specifications are included in JSON output with rationale in metadata field.

## JSON Output Format

Output structure for API integration:

```json
{
  "optimized_prompt": {
    "positive": "cozy artisan coffee shop interior, rain-streaked windows, warm amber lighting, wooden tables, steaming espresso cups, photorealistic, 8k uhd, shallow depth of field, bokeh effect, professional photography, cinematic lighting, golden hour atmosphere",
    "negative": "blurry, low quality, distorted, artificial lighting, empty, cold atmosphere"
  },
  "model": {
    "name": "nano-banana",
    "variant": "standard",
    "reason": "Selected for photorealistic interior photography with natural lighting"
  },
  "quality_score": {
    "overall": 8.7,
    "breakdown": {
      "clarity": 9.0,
      "completeness": 8.5,
      "optimization": 9.0,
      "coherence": 9.0,
      "technical_validity": 9.0,
      "safety": 10.0
    },
    "rating": "excellent"
  },
  "warnings": [
    {
      "category": "optimization",
      "severity": "low",
      "message": "Consider specifying camera angle (eye-level, low-angle) for better composition",
      "recommendation": "Add: 'eye-level view' or 'slightly elevated perspective'"
    }
  ],
  "technical_specs": {
    "resolution": {
      "width": 1024,
      "height": 768,
      "reason": "Landscape orientation for interior scene, standard quality"
    },
    "aspect_ratio": "4:3",
    "format": "PNG",
    "seed": null,
    "steps": 25,
    "guidance_scale": 8.5
  },
  "metadata": {
    "original_input": "a cozy coffee shop on a rainy day",
    "timestamp": "2025-01-11T00:15:00Z",
    "transformation_notes": "Added photorealistic quality boosters, specified lighting conditions (warm amber, golden hour), enhanced atmosphere with rain-streaked windows detail, included technical photography terms for depth and focus"
  }
}
```

**Field Descriptions:**
- `optimized_prompt.positive`: Main prompt text with model-specific keywords and quality boosters
- `optimized_prompt.negative`: Elements to suppress (not supported by all models)
- `model.name`: Selected model identifier (nano-banana, flux-1-1, recraft-v3, seedream-v3, seedream-v4, sd-3-5)
- `model.variant`: Generation mode (standard, pro, turbo)
- `model.reason`: Explanation of why this model was selected
- `quality_score.overall`: Weighted average score (0-10 scale)
- `quality_score.breakdown`: Individual dimension scores
- `quality_score.rating`: Text rating (poor, fair, good, excellent, exceptional)
- `warnings`: Array of detected issues with severity and recommendations
- `technical_specs`: Auto-detected generation parameters ready for API submission
- `metadata`: Original input, timestamp, and transformation reasoning for debugging

## Examples

### Example 1: Photorealistic Product Shot (Nano Banana)

**User Input:**
"professional product photo of wireless headphones on a clean surface"

**JSON Output:**
```json
{
  "optimized_prompt": {
    "positive": "premium wireless headphones, matte black finish, positioned on white marble surface, studio lighting with softbox diffusion, clean minimalist composition, product photography, commercial quality, 8k uhd, sharp focus, shallow depth of field, professional color grading, high-end consumer electronics aesthetic",
    "negative": "cluttered background, harsh shadows, lens flare, chromatic aberration, overexposed, color noise"
  },
  "model": {
    "name": "nano-banana",
    "variant": "standard",
    "reason": "Optimal for photorealistic product photography with natural material rendering"
  },
  "quality_score": {
    "overall": 9.1,
    "breakdown": {
      "clarity": 9.5,
      "completeness": 9.0,
      "optimization": 9.5,
      "coherence": 9.0,
      "technical_validity": 9.0,
      "safety": 10.0
    },
    "rating": "exceptional"
  },
  "warnings": [],
  "technical_specs": {
    "resolution": {"width": 1024, "height": 1024, "reason": "Square format standard for product photography"},
    "aspect_ratio": "1:1",
    "format": "PNG",
    "seed": null,
    "steps": 30,
    "guidance_scale": 9.0
  },
  "metadata": {
    "original_input": "professional product photo of wireless headphones on a clean surface",
    "timestamp": "2025-01-11T00:15:00Z",
    "transformation_notes": "Enhanced with commercial photography keywords, specified lighting setup (studio with softbox), added material details (matte black, marble), included technical terms for product shot quality"
  }
}
```

### Example 2: Marketing Graphic with Text (Recraft V3)

**User Input:**
"instagram post for coffee brand with text 'MORNING VIBES' and coffee cup illustration"

**JSON Output:**
```json
{
  "optimized_prompt": {
    "positive": "modern minimalist instagram post design, text 'MORNING VIBES' in bold sans-serif typography, stylized coffee cup illustration with steam, warm brown and cream color palette, clean vector graphics, professional branding, centered composition, social media optimized, high contrast, marketing design aesthetic",
    "negative": null
  },
  "model": {
    "name": "recraft-v3",
    "variant": "standard",
    "reason": "Selected for precise text rendering ('MORNING VIBES') and graphic design capabilities"
  },
  "quality_score": {
    "overall": 8.9,
    "breakdown": {
      "clarity": 9.0,
      "completeness": 8.5,
      "optimization": 9.5,
      "coherence": 9.0,
      "technical_validity": 9.0,
      "safety": 10.0
    },
    "rating": "excellent"
  },
  "warnings": [
    {
      "category": "quality",
      "severity": "low",
      "message": "Consider specifying exact font style for brand consistency",
      "recommendation": "Add: 'geometric sans-serif' or 'modern condensed font'"
    }
  ],
  "technical_specs": {
    "resolution": {"width": 1024, "height": 1024, "reason": "Instagram square post format"},
    "aspect_ratio": "1:1",
    "format": "PNG",
    "seed": null,
    "steps": 25,
    "guidance_scale": 8.0
  },
  "metadata": {
    "original_input": "instagram post for coffee brand with text 'MORNING VIBES' and coffee cup illustration",
    "timestamp": "2025-01-11T00:15:00Z",
    "transformation_notes": "Optimized for Recraft V3's text rendering strength, specified typography style, added vector graphics keywords, defined color palette for brand consistency, included social media composition guidance"
  }
}
```

### Example 3: Artistic Concept Art (FLUX 1.1)

**User Input:**
"fantasy dragon perched on mountain peak at sunset, epic and majestic"

**JSON Output:**
```json
{
  "optimized_prompt": {
    "positive": "majestic fantasy dragon perched on rocky mountain peak, sunset sky with dramatic clouds, scales glistening in golden light, powerful wingspan spread, epic cinematic composition, fantasy art, masterpiece, highly detailed, volumetric lighting, atmospheric perspective, concept art style, trending on artstation, breathtaking vista, magical atmosphere",
    "negative": "low quality, blurry, amateur, poorly drawn anatomy, flat lighting, washed out colors, boring composition"
  },
  "model": {
    "name": "flux-1-1",
    "variant": "standard",
    "reason": "Optimal for fantasy artistic content with strong creative interpretation and style flexibility"
  },
  "quality_score": {
    "overall": 8.5,
    "breakdown": {
      "clarity": 8.5,
      "completeness": 8.0,
      "optimization": 9.0,
      "coherence": 9.0,
      "technical_validity": 9.0,
      "safety": 10.0
    },
    "rating": "excellent"
  },
  "warnings": [
    {
      "category": "optimization",
      "severity": "low",
      "message": "Consider specifying dragon color/type for more controlled output",
      "recommendation": "Add: 'crimson red scales' or 'ancient bronze dragon'"
    }
  ],
  "technical_specs": {
    "resolution": {"width": 1344, "height": 768, "reason": "Cinematic wide aspect for epic landscape composition"},
    "aspect_ratio": "16:9",
    "format": "JPEG",
    "seed": null,
    "steps": 28,
    "guidance_scale": 8.5
  },
  "metadata": {
    "original_input": "fantasy dragon perched on mountain peak at sunset, epic and majestic",
    "timestamp": "2025-01-11T00:15:00Z",
    "transformation_notes": "Applied FLUX artistic quality boosters (masterpiece, trending on artstation), enhanced lighting with volumetric and atmospheric effects, added composition guidance (epic cinematic), specified detail level and mood"
  }
}
```

For more comprehensive transformation examples covering SeeDream and SD 3.5, complex multi-object scenes, edge cases, and quality improvement iterations, see references/transformation_examples.md.

For detailed model-specific keyword patterns and optimization techniques, see references/model_keyword_patterns.md.

For complete quality scoring rubrics with edge case handling, see references/quality_scoring_criteria.md.
