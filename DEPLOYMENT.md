# GitHub Pages Deployment Guide

This guide explains how to deploy the DataDistiller AI documentation to GitHub Pages.

## Overview

The documentation is built using **MkDocs Material** and automatically deployed to GitHub Pages using GitHub Actions.

**Live Site**: https://branchzerodevs.github.io/DataDistillerAI/

## Automatic Deployment

The documentation is automatically deployed when you push to the `main` branch.

### Workflow

1. Push changes to `main` branch
2. GitHub Actions runs `.github/workflows/docs.yml`
3. MkDocs builds the site from `docs_site/`
4. Site is deployed to GitHub Pages
5. Available at the URL above

## Setup GitHub Pages (One-Time)

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in left sidebar)
3. Under **Source**, select:
   - Source: **GitHub Actions**
4. Save changes

That's it! The site will auto-deploy on the next push to `main`.

## Local Development

### Install Dependencies

```bash
pip install mkdocs-material mkdocs-minify-plugin
```

### Preview Locally

```bash
# Serve with hot-reload
mkdocs serve

# Open browser to http://localhost:8000
```

### Build Locally

```bash
# Build static site
mkdocs build

# Output in site/ directory
```

## Project Structure

```
DataDistillerAI/
├── mkdocs.yml              # MkDocs configuration
├── docs_site/              # Documentation source
│   ├── index.md           # Home page
│   ├── getting-started/   # Setup guides
│   ├── architecture/      # Technical docs
│   ├── guides/            # User guides
│   ├── advanced/          # Advanced topics
│   └── about/             # License, changelog
└── .github/
    └── workflows/
        └── docs.yml       # Deployment workflow
```

## Adding New Pages

1. Create markdown file in appropriate `docs_site/` subdirectory
2. Add entry to `nav:` section in `mkdocs.yml`
3. Commit and push to `main`

Example:

```yaml
# mkdocs.yml
nav:
  - Home: index.md
  - Getting Started:
      - Quick Start: getting-started/quickstart.md
      - New Page: getting-started/new-page.md  # Add this
```

## Customization

### Theme Colors

Edit `mkdocs.yml`:

```yaml
theme:
  palette:
    - scheme: default
      primary: indigo  # Change color
      accent: indigo
```

### Features

Enable/disable features in `mkdocs.yml`:

```yaml
theme:
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
    - content.code.copy
```

## Troubleshooting

### Build Fails

Check GitHub Actions logs:
1. Go to **Actions** tab
2. Click failed workflow run
3. View error logs

### Local Build Issues

```bash
# Clear cache
rm -rf site/

# Rebuild
mkdocs build --strict
```

### Pages Not Updating

1. Check GitHub Actions completed successfully
2. Wait 1-2 minutes for CDN cache
3. Hard refresh browser (Ctrl+Shift+R)

## Manual Deployment

If needed, you can deploy manually:

```bash
# Build and deploy
mkdocs gh-deploy --force
```

This builds and pushes to `gh-pages` branch.

## Best Practices

1. **Preview locally** before pushing
2. **Use `mkdocs build --strict`** to catch errors
3. **Keep navigation organized** in mkdocs.yml
4. **Use relative links** in markdown
5. **Add images to docs_site/assets/** if needed

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

## Support

Issues with documentation deployment? [Open an issue](https://github.com/BranchZeroDevs/DataDistillerAI/issues)
