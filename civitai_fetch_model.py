# model_fetcher.py
"""
AI Model Fetcher - Downloads models and metadata from AI model APIs.

Note: Current implementation uses AI model platform (civitai.com) as the API provider
"""

import requests
import re
import io
from pathlib import Path
from typing import Optional
from PIL import Image

# =========================================================
# CONFIGURATION & CONSTANTS
# =========================================================

API_MODEL_URL = "https://api.civitai.com/v1/models/{}"
API_TIMEOUT = 30
DEFAULT_IMAGE_PLACEHOLDER_COUNT = 2

# Field names for metadata extraction (different API versions)
SAMPLER_FIELD_NAMES = ["sampler", "samplerName", "Sampler"]
SCHEDULER_FIELD_NAMES = ["scheduler", "schedulerName", "Scheduler"]
SIZE_FIELD_NAMES = ["size", "resolution", "Size"]

# Default directories (can be overridden)
DEFAULT_BASE_DIR = Path(".")
DEFAULT_MD_OUT_DIR = DEFAULT_BASE_DIR / "models"
DEFAULT_IMG_OUT_DIR = DEFAULT_BASE_DIR / "images"

DEFAULT_MD_OUT_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_IMG_OUT_DIR.mkdir(parents=True, exist_ok=True)

# Template file location (relative to this script)
TEMPLATE_FILE = Path(__file__).parent / "model_template.md"

# =========================================================
# TEMPLATE FUNCTIONS
# =========================================================

def load_template() -> str:
    """
    Loads the markdown template from model_template.md.
    Raises FileNotFoundError if template is not found.
    """
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(
            f"Template file not found: {TEMPLATE_FILE}\n"
            f"Please ensure model_template.md exists in the project root."
        )
    return TEMPLATE_FILE.read_text(encoding="utf-8")


def render_template(template: str, variables: dict, lists: dict) -> str:
    """
    Renders the template by replacing variables and filling repeated blocks.
    
    Args:
        template: Template string with {{variable}} and <!-- BEGIN/END --> blocks
        variables: Dict of simple variables to replace
        lists: Dict of lists to fill repeated blocks
               Format: {"SECTION_NAME": [{"key": value, ...}, ...]}
               Example: {"IMAGES": [{"image_filename": "img1.png"}, {"image_filename": "img2.png"}]}
    
    Returns:
        Rendered markdown string
    """
    result = template
    
    # Replace simple variables
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value))
    
    # Replace repeated blocks
    for section_name, items in lists.items():
        begin_marker = f"<!-- BEGIN {section_name} -->"
        end_marker = f"<!-- END {section_name} -->"
        
        # Find the block
        begin_idx = result.find(begin_marker)
        end_idx = result.find(end_marker)
        
        if begin_idx == -1 or end_idx == -1:
            continue
        
        # Extract the block content (between markers)
        block_start = begin_idx + len(begin_marker)
        block_content = result[block_start:end_idx]
        
        # Render this block for each item in the list
        rendered_items = []
        for item in items:
            item_text = block_content
            # Replace variables for this item
            for key, value in item.items():
                placeholder = f"{{{{{key}}}}}"
                item_text = item_text.replace(placeholder, str(value))
            rendered_items.append(item_text)
        
        # Join all rendered items and replace the entire block (keep the markers)
        full_block = begin_marker + block_content + end_marker
        replacement = begin_marker + "".join(rendered_items) + end_marker
        result = result.replace(full_block, replacement)
    
    # Post-processing: Remove all comment markers
    # This prevents Obsidian media-slider plugin from treating them as errors
    result = re.sub(r'<!-- BEGIN .+ -->\n', '', result)
    result = re.sub(r'<!-- END .+ -->\n', '', result)
    # Also handle cases without trailing newline
    result = re.sub(r'<!-- BEGIN .+ -->', '', result)
    result = re.sub(r'<!-- END .+ -->', '', result)
    
    return result

# =========================================================
# GENERAL HELPER FUNCTIONS
# =========================================================

def run(
    model_id: int,
    version_name: str,
    progress_callback=None,
    cancel_event=None,
    md_output_dir: Optional[Path] = None,
    img_output_dir: Optional[Path] = None
):
    """
    Starts the fetch process for a model.
    
    Args:
        model_id: Model ID from the API platform
        version_name: Name of the model version
        progress_callback: Callback for progress display (float: 0-100)
        cancel_event: threading.Event for cancellation
        md_output_dir: Output directory for Markdown (default: ./models)
        img_output_dir: Output directory for images (default: ./images)
    """
    if md_output_dir is None:
        md_output_dir = DEFAULT_MD_OUT_DIR
    if img_output_dir is None:
        img_output_dir = DEFAULT_IMG_OUT_DIR
    
    main(
        model_id,
        version_name,
        progress_callback=progress_callback,
        cancel_event=cancel_event,
        md_output_dir=md_output_dir,
        img_output_dir=img_output_dir
    )


def sanitize_filename(text: str) -> str:
    """
    Removes problematic characters from filenames.
    """
    return re.sub(r"[^\w\d\-_ ]", "_", text).strip()


def download_image(url: str, target_base: Path) -> str | None:
    """
    Downloads an image and saves it in the appropriate format.
    Returns: filename or None on error.
    """
    try:
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()

        img = Image.open(io.BytesIO(response.content))

        if getattr(img, "is_animated", False):
            out_file = target_base.with_suffix(".gif")
            img.save(out_file, save_all=True)
        elif img.mode in ("RGBA", "P"):
            out_file = target_base.with_suffix(".png")
            img.save(out_file)
        else:
            out_file = target_base.with_suffix(".jpeg")
            img.convert("RGB").save(out_file, quality=95)

        return out_file.name

    except Exception as e:
        print(f"[WARN] Image could not be downloaded: {url} ({e})")
        return None

# =========================================================
# AI MODEL METADATA EXTRACTION
# =========================================================

def extract_sampler_scheduler(images: list[dict]) -> list[tuple[str, str]]:
    """
    Extracts unique sampler/scheduler combinations from image metadata.
    """
    results = []
    seen = set()

    for img in images:
        meta = img.get("meta") or {}

        sampler = next((meta.get(f) for f in SAMPLER_FIELD_NAMES if f in meta), None)
        scheduler = next((meta.get(f) for f in SCHEDULER_FIELD_NAMES if f in meta), None)

        key = (str(sampler or "").strip(), str(scheduler or "").strip())

        if key not in seen and any(key):
            seen.add(key)
            results.append(key)

    return results


def extract_resolutions(images: list[dict]) -> list[str]:
    """
    Extracts unique resolutions from image metadata.
    """
    results = []
    seen = set()

    for img in images:
        meta = img.get("meta") or {}
        size = next((meta.get(f) for f in SIZE_FIELD_NAMES if f in meta), None)

        if size:
            value = str(size).strip()
            if value not in seen:
                seen.add(value)
                results.append(value)

    return results


def extract_prompts(images: list[dict]) -> tuple[list[str], list[str]]:
    """
    Extracts positive and negative prompts.
    """
    positive, negative = [], []
    seen_pos, seen_neg = set(), set()

    for img in images:
        meta = img.get("meta") or {}

        pos = meta.get("prompt")
        neg = meta.get("negativePrompt") or meta.get("negativeprompt") or meta.get("negative_prompt")

        if pos:
            pos = str(pos).strip()
            if pos and pos not in seen_pos:
                seen_pos.add(pos)
                positive.append(pos)

        if neg:
            neg = str(neg).strip()
            if neg and neg not in seen_neg:
                seen_neg.add(neg)
                negative.append(neg)

    return positive, negative


def extract_loras(version: dict) -> list[str]:
    """
    Extracts recommended LoRAs from training information.
    """
    loras = set()

    for file in version.get("files", []):
        training = file.get("training") or {}
        resources = training.get("requiredResources", []) + training.get("optionalResources", [])

        for r in resources:
            name = r.get("name")
            if name:
                loras.add(str(name))

    return sorted(loras)

# =========================================================
# MARKDOWN HELPER FUNCTIONS
# =========================================================

def render_file_tables(files: list[dict]) -> str:
    """
    Renders the download file tables as specified in the template.
    """
    if not files:
        return ""

    md = "\n---\n\n## 💾 Model Download\n\n"

    for idx, file in enumerate(files, 1):
        name = file.get("name", "")
        ftype = file.get("type", "")
        fmt = file.get("format", "")
        size_kb = file.get("sizeKB")
        size = f"{size_kb / 1024 / 1024:.2f} GB" if size_kb else ""
        url = file.get("downloadUrl", "")

        fp = ""
        if "fp=fp16" in url:
            fp = "fp16"
        elif "fp=fp32" in url:
            fp = "fp32"

        md += f"""### File {idx}

| Field | Value |
|-------|-------|
| Name | {name} |
| Type | {ftype} |
| Format | {fmt} |
| FP | {fp} |
| Download | {url} |
| Size | {size} |

---

"""

    return md

# =========================================================
# MAIN
# =========================================================

def main(
    model_id: int,
    version_name: str,
    progress_callback=None,
    cancel_event=None,
    md_output_dir: Optional[Path] = None,
    img_output_dir: Optional[Path] = None
):
    """
    Main function to fetch and save AI model data and documentation.
    """
    if md_output_dir is None:
        md_output_dir = DEFAULT_MD_OUT_DIR
    if img_output_dir is None:
        img_output_dir = DEFAULT_IMG_OUT_DIR
    
    # Ensure directories exist
    md_output_dir.mkdir(parents=True, exist_ok=True)
    img_output_dir.mkdir(parents=True, exist_ok=True)
    
    # -------- Fetch from API --------
    response = requests.get(API_MODEL_URL.format(model_id), timeout=API_TIMEOUT)
    response.raise_for_status()
    data = response.json()

    model_name = data.get("name", "")
    model_type = data.get("type", "")
    base_model = data.get("baseModel") or ""

    # -------- Find version --------
    version = next(
        (v for v in data.get("modelVersions", [])
         if v.get("name", "").lower() == version_name.lower()),
        None
    )

    if not version:
        print(f"[ERROR] Version '{version_name}' not found.")
        return

    # -------- Save images --------
    model_img_dir = img_output_dir / sanitize_filename(model_name)
    version_img_dir = model_img_dir / sanitize_filename(version.get("name", ""))
    version_img_dir.mkdir(parents=True, exist_ok=True)

    images = version.get("images", [])
    saved_images = []

    total = len(images)

    for idx, img in enumerate(images, 1):
        url = img.get("url")
        if not url:
            print(f"[SKIP] Image {idx}/{total}: no URL")
            continue

        print(f"[INFO] Downloading image {idx}/{total} ...")

        base_name = f"{sanitize_filename(model_name)}_{sanitize_filename(version.get('name',''))}_{idx}"
        saved = download_image(url, version_img_dir / base_name)

        if saved:
            saved_images.append(saved)
            print(f"[OK] Image saved: {saved}")
        else:
            print(f"[WARN] Image {idx}/{total} could not be saved")

        # Fortschritt für Progressbar nur über Callback
        if progress_callback:
            percent = (idx / total) * 100 if total else 0
            progress_callback(percent)

        # Check for cancellation
        if cancel_event and cancel_event.is_set():
            print("[WARN] Download cancelled")
            break


    # -------- Collect metadata --------
    samplers = extract_sampler_scheduler(images)
    resolutions = extract_resolutions(images)
    pos_prompts, neg_prompts = extract_prompts(images)
    loras = extract_loras(version)
    files_data = version.get("files", [])

    # =========================================================
    # RENDER TEMPLATE
    # =========================================================

    version_str = version.get('name', '')
    
    # Prepare simple variables for template
    variables = {
        "sanitized_model_name": sanitize_filename(model_name),
        "model_name": model_name,
        "base_model": base_model,
        "model_type": model_type,
        "version": version_str,
        "civitai_id": model_id,
        "description": re.sub(
            r'<edge-media[^>]*>',
            '',
            data.get("description", "").strip(),
            flags=re.IGNORECASE
        )
    }
    
    # Prepare lists for repeated blocks
    lists = {}
    
    # Sample Images
    lists["SAMPLE_IMAGES"] = [
        {"image_filename": img} for img in saved_images
    ]
    
    # Samplers
    lists["SAMPLERS"] = [
        {"sampler_name": s[0], "scheduler_name": s[1]} for s in samplers
    ]
    
    # Resolutions
    lists["RESOLUTIONS"] = [
        {"resolution_value": res} for res in resolutions
    ]
    
    # Positive Prompts
    lists["POSITIVE_PROMPTS"] = [
        {"prompt_text": p} for p in pos_prompts
    ]
    
    # Negative Prompts
    lists["NEGATIVE_PROMPTS"] = [
        {"prompt_text": n} for n in neg_prompts
    ]
    
    # LoRAs
    lists["LORAS"] = [
        {"lora_name": l} for l in loras
    ]
    
    # Files
    files_list = []
    for idx, file in enumerate(files_data, 1):
        name = file.get("name", "")
        ftype = file.get("type", "")
        fmt = file.get("format", "")
        size_kb = file.get("sizeKB")
        size = f"{size_kb / 1024 / 1024:.2f} GB" if size_kb else ""
        url = file.get("downloadUrl", "")
        
        fp = ""
        if "fp=fp16" in url:
            fp = "fp16"
        elif "fp=fp32" in url:
            fp = "fp32"
        
        files_list.append({
            "file_index": str(idx),
            "file_name": name,
            "file_type": ftype,
            "file_format": fmt,
            "file_fp": fp,
            "file_url": url,
            "file_size": size
        })
    
    lists["FILES"] = files_list
    
    # Load and render template
    template = load_template()
    md = render_template(template, variables, lists)

    # -------- Save --------
    # Create model-specific directory for markdown files
    model_dir = md_output_dir / sanitize_filename(model_name)
    model_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = model_dir / f"{sanitize_filename(model_name)}{version_str}.md"
    out_file.write_text(md, encoding="utf-8")

    print(f"[OK] Markdown created: {out_file}")
    print(f"Done!")

if __name__ == "__main__":
    # Example usage - replace with actual model ID and version
    print("[INFO] Example usage: python civitai_fetch_model.py")
    print("[INFO] Import this module and call main(model_id, version_name)")
    # Uncomment the line below to test with a specific model:
    # main(3149, "v16.0")

