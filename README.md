# AI Model Fetcher [WIP]

A Python GUI application for downloading AI model metadata and sample images to generate a Markdown knowledge base file.

Why? I just wanted to automate the process of creating my local AI model knowledge base in [Obsidian](https://obsidian.md/)

## 🎯 Features

- **Easy Model Discovery** - Search by Model ID or API link
- **Automatic Metadata Extraction**: Downloads model metadata including:
  - Sample images
  - Positive & negative prompts
  - Sampler and scheduler configurations
  - Model resolutions
  - Recommended LoRAs
  - File information
- **Markdown Documentation** - Auto-generates well-structured markdown with embedded images
- **GUI Configuration** - Set output paths directly from the app
- **Progress Tracking** - Real-time progress bar for downloads
- **Color-Coded Logging** - Debug console with detailed status messages

## 📋 Requirements

- **Python 3.10 or higher** (required for type annotation syntax)
- tkinter (usually bundled with Python, see platform-specific instructions below)
- requests library
- Pillow (PIL) library

## 🚀 Installation

### 1. Clone or download the repository

```bash
git clone https://github.com/nohumangaming/ai-model-fetcher.git
cd ai-model-fetcher
```

### 2. Create a virtual environment (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Ubuntu/Manjaro/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure paths (optional)

Copy the example configuration to get started:

```bash
cp config.json.example config.json
```

Then adjust the paths in `config.json` as needed, or use the Settings tab in the application.

### 5. Run the application

```bash
python ui.py
```

## �️ Platform-Specific Setup

### Ubuntu / Debian

**1. Install Python 3.10+:**

```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-tk python3-pip
```

**2. Verify installation:**

```bash
python3.10 --version  # Should show 3.10.x or higher
```

**3. Follow the general installation steps above, but use `python3.10` instead of `python`:**

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3.10 ui.py
```

**Troubleshooting for Ubuntu:**
- If `python3.10-tk` is not found, try: `sudo apt install python3-tk`
- For Debian Bookworm or newer, use `python3` directly (usually 3.11+)
- If tkinter still won't load, install: `sudo apt install tk`

---

### Manjaro / Arch Linux

**1. Install Python 3.10+ (if not already installed):**

```bash
sudo pacman -Syu
sudo pacman -S python tk
```

**2. Verify installation:**

```bash
python --version  # Should show 3.10.x or higher
```

**3. Follow the general installation steps:**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ui.py
```

**Troubleshooting for Manjaro:**
- If tkinter won't load, ensure `tk` package is installed: `sudo pacman -Sy tk`
- For development headers, install: `sudo pacman -S base-devel`
- If you see permission errors, ensure the project directory is readable: `chmod -R u+rx .`

---

### Windows 10/11

**1. Install Python 3.10+:**

- Download from [python.org](https://www.python.org/downloads/)
- **Important:** During installation, check the boxes for:
  - ✅ **"Add Python to PATH"**
  - ✅ **"tcl/tk and IDLE"** (required for tkinter)
  
- Verify installation in PowerShell or Command Prompt:
  ```cmd
  python --version
  ```

**2. Create and activate virtual environment:**

```cmd
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**

```cmd
pip install -r requirements.txt
```

**4. Run the application:**

```cmd
python ui.py
```

**Troubleshooting for Windows:**
- If `python` command is not recognized, reinstall Python and ensure "Add Python to PATH" is checked
- If tkinter won't import, reinstall Python and check the "tcl/tk and IDLE" option
- If you see certificate errors when downloading models, your antivirus might be interfering (temporarily disable it for the download)
- For Windows 11, consider using Windows Terminal (better experience than Command Prompt)

---

## �💻 Usage

### Basic Workflow

1. **Enter Model ID or Link**:
   - Paste a model link from AI model platform: `https://civitai.com/models/3149`
   - Or just enter the ID: `3149`

2. **Fetch Versions**:
   - Click `↻ Versionen abrufen`
   - The app displays the model name and available versions

3. **Select Version**:
   - Choose a version from the dropdown
   - Model information (name, type) is shown in the "Model Info" section

4. **Download**:
   - Click `▶ Start` to begin the download
   - Monitor progress in the log window
   - Click `⏹ Abbrechen` to cancel if needed
. On first run, a default configuration is created. You can:

1. **Use the default paths** (recommended for first-time users):
   - Models: `./models`
   - Images: `./images`
   - Downloads: `./downloads`

2. **Customize paths** via the GUI:
   - Open the **⚙️ Einstellungen** (Settings) tab
   - Adjust directory paths
   - Click **💾 Speichern** (Save)

3. **Manual configuration**:
   - Edit `config.json` directly:

```json
{
  "model_output_dir": "./models",
  "image_output_dir": "./images",
  "model_download_dir": "./downloads",
  "api_timeout": 30,
  "image_placeholder_count": 2
}
```

**Note:** Do not commit `config.json` to version control (it's in `.gitignore`). Use `config.json.example` as a template for documentation. Organized in model-specific directories
  - Pre-formatted YAML frontmatter
  - Sample images section
  - Model description and metadata
  - Test setup templates
  - LoRA recommendations

- **Images**: `./images/{ModelName}/{VersionName}/`
  - All sample images from the model version
  - Automatically converted to optimal format (PNG, JPEG, or GIF)

## 📁 Configuration

Settings are saved in `config.json`:

```json
{
  "model_output_dir": "./models",
  "image_output_dir": "./images",
  "api_timeout": 30,
  "image_placeholder_count": 2
}
```

## 🏗️ Project Structure

```
ai-model-fetcher/
├── ui.py                      # Main GUI application
├── civitai_fetch_model.py     # Model fetching and markdown generation
├── civitai_api_helper.py      # AI Model API wrapper
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── config.json               # User configuration (auto-generated)
└── README.md                 # This file
```

## 🔧 How It Works

### API Integration
- Fetches model metadata from AI model API
- Extracts model versions, images, and metadata
- Downloads images with automatic format optimization

### Markdown Generation
- Creates structured markdown files following a template
- Includes YAML frontmatter for metadata
- Uses media sliders for image galleries
- Pre-formatted tables for settings and configurations

### Threading
- Downloads run in background threads to keep UI responsive
- Supports cancellation at any time
- Real-time progress updates via callback mechanism

## 🐛 Troubleshooting

### "Modell nicht gefunden"
- Verify the Model ID is correct
- Check your internet connection
- Ensure the model hasn't been removed from the AI model platform

### Images not downloading
- Check your internet connection
- Some models may have restricted image access
- The app logs warnings for failed image downloads

### Config.json issues
- Delete `config.json` to reset to defaults
- Ensure directories have proper permissions

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🎨 Template Customization

The application uses an external markdown template (`model_template.md`) for generating model documentation. Users can easily customize the template without modifying any Python code.

### Template System

The template uses:
- **Simple Variables**: `{{variable_name}}` - replaced with corresponding values
- **Repeated Blocks**: `<!-- BEGIN SECTION_NAME -->` ... `<!-- END SECTION_NAME -->` - dynamically filled with list items

### Available Template Variables

#### Simple Variables (Direct Replacement)

| Variable | Description | Example |
|----------|-------------|---------|
| `{{model_name}}` | Full model name from AI model platform | "Cyberrealistic Pony" |
| `{{sanitized_model_name}}` | URL-safe version of model name | "Cyberrealistic_Pony" |
| `{{version}}` | Version name of the model | "v16.0" |
| `{{base_model}}` | Base model used (e.g., Stable Diffusion) | "SDXL 1.0" |
| `{{model_type}}` | Type of model | "Checkpoint" |
| `{{civitai_id}}` | AI Model ID | "3149" |
| `{{description}}` | Full model description from AI model platform (HTML tags removed) | "A realistic pony model..." |

#### Repeated Blocks (Lists)

##### Sample Images: `<!-- BEGIN SAMPLE_IMAGES -->` ... `<!-- END SAMPLE_IMAGES -->`

Used for: All downloaded sample images

Variables inside block:
- `{{image_filename}}` - Filename of the saved image

Example template:
```markdown
<!-- BEGIN SAMPLE_IMAGES -->
![[{{image_filename}}]]
<!-- END SAMPLE_IMAGES -->
```

Result:
```markdown
![[model_image_1.png]]
![[model_image_2.png]]
![[model_image_3.png]]
```

##### Samplers: `<!-- BEGIN SAMPLERS -->` ... `<!-- END SAMPLERS -->`

Used for: Recommended sampler/scheduler combinations

Variables inside block:
- `{{sampler_name}}` - Sampler name (e.g., "DPM++ 2M")
- `{{scheduler_name}}` - Scheduler name (e.g., "Karras")

##### Resolutions: `<!-- BEGIN RESOLUTIONS -->` ... `<!-- END RESOLUTIONS -->`

Used for: Supported image resolutions

Variables inside block:
- `{{resolution_value}}` - Resolution dimensions (e.g., "768x1024")

##### Positive Prompts: `<!-- BEGIN POSITIVE_PROMPTS -->` ... `<!-- END POSITIVE_PROMPTS -->`

Used for: Positive prompt examples from model metadata

Variables inside block:
- `{{prompt_text}}` - A positive prompt example

##### Negative Prompts: `<!-- BEGIN NEGATIVE_PROMPTS -->` ... `<!-- END NEGATIVE_PROMPTS -->`

Used for: Negative prompt examples from model metadata

Variables inside block:
- `{{prompt_text}}` - A negative prompt example

##### LoRAs: `<!-- BEGIN LORAS -->` ... `<!-- END LORAS -->`

Used for: Recommended LoRAs/extensions for this model

Variables inside block:
- `{{lora_name}}` - Name of recommended LoRA

##### Files: `<!-- BEGIN FILES -->` ... `<!-- END FILES -->`

Used for: Download file information

Variables inside block:
- `{{file_index}}` - File number (1, 2, 3, ...)
- `{{file_name}}` - Filename on the AI model platform
- `{{file_type}}` - File type (e.g., "Model")
- `{{file_format}}` - Format (e.g., "SafeTensors")
- `{{file_fp}}` - Precision type (fp16, fp32, or empty)
- `{{file_url}}` - Direct download URL
- `{{file_size}}` - File size in GB

### Customizing the Template

1. Open `model_template.md` in your text editor
2. Modify the structure, add/remove sections, change headings, etc.
3. Keep all `{{variable}}` placeholders intact
4. When you fetch a new model, the placeholder values will be automatically filled

**Example modifications:**

**Change** heading levels:
```markdown
# Before
## 🗼 Sample Images from Models

# After
### 📸 Sample Gallery
```

**Reorder** sections by moving blocks around

**Add** new static content (won't be replaced):
```markdown
### Custom Section
This is my custom note about this model.
```

**Remove** unused sections entirely by deleting the blocks

### Important Notes

- Template file must be named `model_template.md` and located in the project root (same directory as `ui.py`)
- Do NOT rename or move variable placeholders - they must match exactly: `{{variable_name}}`
- Do NOT modify the `<!-- BEGIN/END -->` markers - they control which blocks get repeated
- Empty lists will result in empty blocks (this is expected behavior)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📸 Screenshots

*Coming soon - Submit a PR with usage examples!*

## 🙏 Acknowledgments

- AI model platform (civitai.com) for providing the API
- Built with ❤️(AI) by the community

## 📞 Support

- Open an issue on GitHub for bug reports
- Feature requests welcome!
- Join the discussions tab for questions

---

**Version**: 0.1.0-beta  
**Last Updated**: February 2026  
**Status**: Active Development
