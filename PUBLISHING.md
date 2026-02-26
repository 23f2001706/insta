# Publishing to PyPI 📦

Complete guide to publish your Instagram Gemini Bot package to PyPI.

## Prerequisites

- PyPI account (free): https://pypi.org/account/register/
- TestPyPI account (optional): https://test.pypi.org/account/register/

## Step 1: Install Build Tools

```bash
pip install build twine
```

## Step 2: Update Package Information

Edit `setup.py` with your details:

```python
setup(
    name="insta-bot-gemini",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Instagram DM bot powered by Google Gemini AI",
    url="https://github.com/yourusername/insta-bot-gemini",
    # ... rest of config
)
```

Or in `pyproject.toml`:

```toml
[project]
name = "insta-bot-gemini"
version = "1.0.0"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
```

## Step 3: Build Distribution

```bash
python -m build
```

This creates:
- `dist/insta-bot-gemini-1.0.0.tar.gz` (source distribution)
- `dist/insta-bot-gemini-1.0.0-py3-none-any.whl` (wheel)

## Step 4: Test Upload (Optional but Recommended)

Test on TestPyPI first:

```bash
twine upload --repository testpypi dist/*
```

Then test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ insta-bot-gemini
```

## Step 5: Upload to PyPI

```bash
twine upload dist/*
```

When prompted, enter your PyPI credentials:
- Username: `__token__`
- Password: Your PyPI API token

## Step 6: Generate PyPI API Token

1. Go to https://pypi.org/account/
2. Login
3. Go to **Account settings** → **API tokens**
4. Click **Add API token**
5. Generate a token for "Entire account" or specific project
6. Copy the token (you'll only see it once!)

## Step 7: Use Token for Uploads

Option A: Use token directly

```bash
twine upload dist/* --username __token__ --password pypi-AgEI...
```

Option B: Create `~/.pypirc` file

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEI...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEI...
```

Then upload:
```bash
twine upload dist/*
```

## Step 8: Verify Installation

```bash
pip install insta-bot-gemini
```

If successful, you'll see:
```
Successfully installed insta-bot-gemini-1.0.0
```

## Step 9: Update & Re-Release

To release a new version:

1. Update version in `setup.py` or `pyproject.toml`
2. Update `CHANGELOG.md` with changes
3. Rebuild and upload:

```bash
rm -rf dist/
python -m build
twine upload dist/*
```

## Versioning

Follow semantic versioning: `MAJOR.MINOR.PATCH`

```
1.0.0  ← Initial release
1.0.1  ← Bug fixes
1.1.0  ← New features
2.0.0  ← Breaking changes
```

## Creating CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-26

### Added
- Initial release
- CLI tool for bot initialization
- Conversation memory with SQLite
- Gemini AI integration
- Instagram webhook support

### Fixed
- Webhook verification issues

### Changed
- Refactored code into package structure
```

## Common Issues

### "403 Forbidden"
- Check your API token is correct
- Make sure token hasn't expired
- Try generating a new token

### "Project name already exists"
- Choose a different package name
- Check https://pypi.org/search/

### "Invalid distribution"
- Run: `twine check dist/*`
- Fix any reported issues

### "Bad statusline"
- Update twine: `pip install --upgrade twine`

## Next Steps

1. ✅ Build: `python -m build`
2. ✅ Test: `twine upload --repository testpypi dist/*`
3. ✅ Upload: `twine upload dist/*`
4. ✅ Verify: `pip install insta-bot-gemini`

## GitHub Actions Automation (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Build and publish
      run: |
        python -m pip install build twine
        python -m build
        twine upload dist/* --username __token__ --password ${{ secrets.PYPI_API_TOKEN }}
```

Then every GitHub release will automatically upload to PyPI!

## Set up GitHub Actions Secret

1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token
6. Click **Add secret**

Now when you create a release, it auto-publishes to PyPI! 🚀

---

**Your package is now on PyPI for the whole world to use!** 🌍
