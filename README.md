# N&A Auto Repairs website

Static site for N&A Auto Repairs, 1701 W Howard St, Evanston, IL. The pages are generated from `src/` by a small Python script (standard library only, no dependencies).

## Build

```
python3 src/build.py --standalone            # production build -> dist/
python3 src/build.py --standalone --staging  # staging build: noindex, robots Disallow, no sitemap
```

`--standalone` writes full HTML pages and embeds the live Google map. Without it, `index.html` is built for the Claude Artifact preview.

## Cloudflare Pages

- Build command: `python3 src/build.py --standalone --staging`
- Build output directory: `dist`
- Custom domain: `naauto.davidfonseca.io` (staging)

Drop `--staging` once the site moves to the real domain.

## Layout

- `src/build.py`: page content and templates
- `src/styles.css`, `src/site.js`: shared styles and scripts
- `src/img/`: photos, service images (credits in `src/img/services/credits.md`), logos
- `src/brand-kit/`: full logo kit; favicons and the share image are copied from here at build time
