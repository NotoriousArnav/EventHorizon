# UV vs PIP in Event Horizon

## Why Two Dependency Systems?

Event Horizon uses **both** `uv` (with `pyproject.toml`) and traditional `pip` (with `requirements.txt`). Here's why:

## Development: UV (Recommended)

**Use `pyproject.toml` and `uv` for local development:**

```bash
# Install dependencies
uv sync

# Run Django
uv run python manage.py runserver

# Run Gunicorn
uv run gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
```

**Benefits:**
- ⚡ **Faster**: 10-100x faster than pip
- 🔒 **Reliable**: Better dependency resolution
- 📦 **Modern**: Python's future package manager
- 🎯 **Precise**: Lock file ensures reproducibility

## Production: Mixed Approach

### Platforms Using requirements.txt (Most Common)

**Why requirements.txt?**
- Vercel, Heroku, and many PaaS platforms don't support `uv` yet
- They expect `requirements.txt` by default
- `requirements.txt` is universally compatible

**Platforms:**
- ✅ Vercel
- ✅ Heroku
- ✅ Railway (can use either)
- ✅ Render (can use either)

**Configuration:**
```json
// vercel.json
"installCommand": "pip install -r requirements.txt"
```

```
# Procfile
web: gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
```

### Platforms That Can Use UV

**VPS/Self-Hosted:**
- Full control over the environment
- Can install `uv` globally
- Better performance

**Setup:**
```bash
# Install uv on server
curl -LsSf https://astral.sh/uv/install.sh | sh

# Deploy
git pull
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic
uv run gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
```

## Keeping requirements.txt in Sync

**When to regenerate:**
- After adding dependencies to `pyproject.toml`
- After updating dependency versions
- Before deploying to platforms that use pip

**How to regenerate:**
```bash
uv pip compile pyproject.toml -o requirements.txt
```

**Automate it (recommended):**
```bash
# Add to pre-commit hook or CI/CD
uv pip compile pyproject.toml -o requirements.txt
git add requirements.txt
```

## Best Practices

### Local Development
```bash
# ✅ DO: Use uv
uv sync
uv run python manage.py runserver

# ❌ DON'T: Use pip locally (slower)
pip install -r requirements.txt
```

### Production Deployment
```bash
# Platform uses pip? ✅ Use requirements.txt
git push heroku main

# Self-hosted? ✅ Use uv
uv sync && uv run gunicorn ...
```

### Dependency Updates
```bash
# 1. Update pyproject.toml
nano pyproject.toml

# 2. Sync locally with uv
uv sync

# 3. Test locally
uv run python manage.py check

# 4. Regenerate requirements.txt
uv pip compile pyproject.toml -o requirements.txt

# 5. Commit both files
git add pyproject.toml uv.lock requirements.txt
git commit -m "Update dependencies"
```

## Platform Comparison

| Platform | Dependency System | Speed | Setup Complexity |
|----------|------------------|-------|------------------|
| **Local Dev** | `uv` + `pyproject.toml` | ⚡⚡⚡ Fast | ⭐ Easy |
| **Vercel** | `pip` + `requirements.txt` | 🐢 Slow | ⭐ Easy |
| **Heroku** | `pip` + `requirements.txt` | 🐢 Slow | ⭐ Easy |
| **Railway** | `pip` + `requirements.txt` | 🐢 Slow | ⭐ Easy |
| **Render** | `pip` + `requirements.txt` | 🐢 Slow | ⭐ Easy |
| **VPS** | `uv` + `pyproject.toml` | ⚡⚡⚡ Fast | ⭐⭐⭐ Complex |

## Common Questions

### Q: Can I use only requirements.txt everywhere?
**A:** Yes, but you'll lose the speed and reliability benefits of `uv` in development.

### Q: Can I use only pyproject.toml everywhere?
**A:** Not yet. Most PaaS platforms don't support `uv`. You need `requirements.txt` for compatibility.

### Q: Will requirements.txt become outdated?
**A:** Yes, if you don't regenerate it after updating `pyproject.toml`. Always run:
```bash
uv pip compile pyproject.toml -o requirements.txt
```

### Q: Which file is the "source of truth"?
**A:** `pyproject.toml` is the source. `requirements.txt` is generated from it.

### Q: Can Railway/Render use uv?
**A:** Technically yes (they support custom build scripts), but `requirements.txt` is simpler and more standard.

## Migration Path (Future)

When more platforms support `uv`:

1. **Now (2024-2025):**
   - Development: `uv`
   - Production: `requirements.txt`

2. **Future (2026+):**
   - Development: `uv`
   - Production: `uv` (when platforms add support)

3. **Eventually:**
   - Remove `requirements.txt`
   - Use only `pyproject.toml` + `uv.lock`

## Example Workflows

### Adding a New Dependency

```bash
# 1. Add to pyproject.toml
# dependencies = [
#     "new-package>=1.0.0",
# ]

# 2. Install with uv
uv sync

# 3. Test locally
uv run python manage.py check

# 4. Update requirements.txt
uv pip compile pyproject.toml -o requirements.txt

# 5. Commit
git add pyproject.toml uv.lock requirements.txt
git commit -m "Add new-package dependency"
```

### Deploying to Different Platforms

**Vercel/Heroku:**
```bash
git push origin main
# Uses requirements.txt automatically
```

**VPS with uv:**
```bash
git pull origin main
uv sync
sudo systemctl restart eventhorizon
```

## Conclusion

- 🏠 **Local Development**: Use `uv` for speed and reliability
- 🌐 **Production Platforms**: Use `requirements.txt` for compatibility
- 🔄 **Keep in Sync**: Regenerate `requirements.txt` after dependency changes
- 🚀 **Future**: Transition to `uv`-only when platforms add support

The dual approach gives you the best of both worlds: modern development experience with maximum deployment compatibility.
