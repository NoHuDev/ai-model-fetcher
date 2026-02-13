# Contributing to AI Model Fetcher

Thank you for your interest in contributing! We welcome bug reports, feature requests, and pull requests.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/nohumangaming/ai-model-fetcher/issues)
2. If not, open a new issue using the **Bug Report** template
3. Include:
   - Your OS and Python version
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Error logs or screenshots

### Suggesting Features

1. Check existing [Issues](https://github.com/nohumangaming/ai-model-fetcher/issues) to avoid duplicates
2. Open a new issue using the **Feature Request** template
3. Describe the problem it solves and how it should work

### Submitting Pull Requests

1. **Fork the repository** on GitHub
2. **Clone your fork locally:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-model-fetcher.git
   cd ai-model-fetcher
   ```

3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes:**
   - Keep changes focused on a single feature or bug fix
   - Follow existing code style (4-space indentation, descriptive names)
   - Add comments for complex logic
   - Update README if needed

5. **Test your changes:**
   - Test on at least one platform (Ubuntu, Manjaro, or Windows)
   - Verify the GUI still works as expected
   - Check that no new errors are introduced

6. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Concise description of changes"
   ```

7. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request:**
   - Use the PR template
   - Link any related issues
   - Describe your changes clearly
   - Include testing details

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Setting up your environment

```bash
# Clone the repository
git clone https://github.com/nohumangaming/ai-model-fetcher.git
cd ai-model-fetcher

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python ui.py
```

## Code Guidelines

- **Python Version:** Code must support Python 3.10+
- **Type Hints:** Use modern type hints (e.g., `str | None` instead of `Optional[str]`)
- **Comments:** Add comments for complex functions or algorithms
- **Imports:** Use absolute imports, organize by standard library, third-party, then local
- **Naming:** Use descriptive names for variables and functions
- **File Handling:** Always use `pathlib.Path` for cross-platform compatibility

## Commit Message Guidelines

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Refactor", etc.
- Example: `Add support for bulk model downloads`

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License (same as the project).

## Questions or Issues?

- Open a discussion in the [GitHub Discussions](https://github.com/nohumangaming/ai-model-fetcher/discussions) tab
- Check existing issues first to avoid duplicates

Thank you for helping improve AI Model Fetcher! 🎉
