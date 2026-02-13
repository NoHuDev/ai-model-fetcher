---
filename: {{sanitized_model_name}}
base_model: {{base_model}}
model_type: {{model_type}}
version_name: {{version}}
rating:
status:
model_url: {{model_url}}
---


## 🗼 Sample Images

```media-slider
---
autoplay: false
slideshowSpeed: 0
width: 100%
height: 600px
enhancedView: true
transitionEffect: blur
transitionDuration: 70
interactiveNotes: false
carouselShowThumbnails: true
thumbnailPosition: top
---
<!-- BEGIN SAMPLE_IMAGES -->
![[{{image_filename}}]]
<!-- END SAMPLE_IMAGES -->
```

---

## 🧠 Description

{{description}}

---

## 📝 Notes

- 

---

## ⚙️ Recommended Settings

| Parameter | Value |
| --------- | ----- |
| Steps     |       |
| CFG       |       |
| Clip Skip |       |
| VAE       |       |
| Seed      |       |

### Sampler & Scheduler

| Sampler | Scheduler |
| ------- | --------- |
<!-- BEGIN SAMPLERS -->
| {{sampler_name}} | {{scheduler_name}} |
<!-- END SAMPLERS -->

### Resolutions

| Resolution |
| ---------- |
<!-- BEGIN RESOLUTIONS -->
| {{resolution_value}} |
<!-- END RESOLUTIONS -->

---

## ✍️ Model Prompts

#### Positive

<!-- BEGIN POSITIVE_PROMPTS -->
{{prompt_text}}

<!-- END POSITIVE_PROMPTS -->

#### Negative

<!-- BEGIN NEGATIVE_PROMPTS -->
{{prompt_text}}

<!-- END NEGATIVE_PROMPTS -->

###### Prompt Helper
[Prompt Helper]()

---

## 🧪 Test Setups

| Purpose | Sampler | Steps | CFG | Result |
| ------- | ------- | ----- | --- | ------ |
|         |         |       |     |        | 

---

## 🧑‍🔬 Setups

```media-slider
---
autoplay: false
slideshowSpeed: 0
width: 100%
height: 600px
enhancedView: true
transitionEffect: blur
transitionDuration: 70
interactiveNotes: true
carouselShowThumbnails: true
thumbnailPosition: top
---
![[]]*
![[]]*
![[]]*
```

---

## 🔗 Recommended LoRAs

<!-- BEGIN LORAS -->
- [[LoRA - {{lora_name}}]]
<!-- END LORAS -->

---

## 📎 References

- [Model Page]({{model_url}})  
- [Local Snapshot]

---
a
## 💾 Model Download

<!-- BEGIN FILES -->
### File {{file_index}}

| Field  | Value |
|--------|-------|
| Name   | {{file_name}} |
| Type   | {{file_type}} |
| Format | {{file_format}} |
| FP     | {{file_fp}} |
| Download | {{file_url}} |
| Size   | {{file_size}} |

---

<!-- END FILES -->
