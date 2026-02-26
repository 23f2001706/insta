# Publish to PyPI - Quick Start Guide (Windows) 📦

## In 5 Steps:

### Step 1: Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Create your account
3. Verify your email

### Step 2: Generate API Token
1. Login to https://pypi.org/account/
2. Go to **Account settings** → **API tokens**
3. Click **Add API token**
4. Name it `insta-bot-upload`
5. Select **Entire account** scope
6. Generate and **COPY the token** (you won't see it again!)

### Step 3: Install Build Tools
```powershell
pip install --upgrade build twine
```

### Step 4: Build Your Package
```powershell
# Clean old builds
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# Build
python -m build
```

You'll see:
```
Successfully built insta-bot-gemini-1.0.0.tar.gz
Successfully built insta-bot-gemini-1.0.0-py3-none-any.whl
```

### Step 5: Upload to PyPI
```powershell
twine upload dist/*
```

When prompted:
- **Username:** `__token__`
- **Password:** Paste your API token

## Done! ✅

Anyone can now install your bot:
```bash
pip install insta-bot-gemini
```

---

## Test Before Publishing (Recommended)

### Test on TestPyPI First

```powershell
# Upload to test repository
twine upload --repository testpypi dist/*

# Install from test repository to verify
pip install --index-url https://test.pypi.org/simple/ insta-bot-gemini

# Then test it works:
insta-bot init
```

If all works, then upload to real PyPI.

---

## Automatic Publishing with GitHub Actions (Optional)

Your repo already has GitHub Actions configured!

### Setup Auto-Publishing

1. Generate PyPI API token (see Step 2 above)

2. Go to your GitHub repo:
   - Settings → Secrets and variables → Actions
   - Click **New repository secret**
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI API token
   - Click **Add secret**

3. Create a release on GitHub:
   - Go to Releases
   - Click **Create a new release**
   - Tag: `v1.0.0`
   - Title: `1.0.0 - Initial release`
   - Description: Copy from CHANGELOG.md
   - Click **Publish release**

**Boom!** Your package automatically publishes to PyPI! 🚀

---

## Updating Your Package

For future releases:

1. Update version in `setup.py`:
   ```python
   version="1.0.1",
   ```

2. Update `CHANGELOG.md`

3. Commit and push:
   ```powershell
   git add .
   git commit -m "Release v1.0.1"
   git push
   ```

4. Create a new release on GitHub (v1.0.1)

5. GitHub Actions automatically publishes! ✅

---

## Semantic Versioning

```
1.0.0  ← Initial release (MAJOR.MINOR.PATCH)
1.0.1  ← Bug fixes only (patch update)
1.1.0  ← New features, no breaking changes (minor update)
2.0.0  ← Breaking changes (major update)
```

---

## Check Your Package on PyPI

After publishing, view it at:
```
https://pypi.org/project/insta-bot-gemini/
```

---

## Common Commands

```powershell
# Build distribution
python -m build

# Check package validity
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from PyPI
pip install insta-bot-gemini

# Install specific version
pip install insta-bot-gemini==1.0.0

# List PyPI versions
pip index versions insta-bot-gemini
```

---

## Troubleshooting

### "403 Forbidden"
- ❌ Token is wrong or expired
- ✅ Generate a new token from PyPI

### "409 Conflict"
- ❌ This version already exists
- ✅ Update version number in setup.py

### "Invalid distribution"
- ❌ Build has issues
- ✅ Run `twine check dist/*` to see problems

### "Module not found"
- ❌ Requirements not installed
- ✅ Run `pip install -r requirements.txt`

---

## Your Package is Live! 🎉

Now anyone in the world can use:
```bash
pip install insta-bot-gemini
```

---

**Need help?** Check [PUBLISHING.md](./PUBLISHING.md) for detailed info.
