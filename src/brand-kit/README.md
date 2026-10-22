# N&A Auto Repair & Towing Service — Logo Kit (Shop Blue)

Vector recreation of the existing logo, recolored to match the **Shop Blue** website design. The shapes and lettering are unchanged. All text is converted to outlines, so the SVGs render the same everywhere with no font install needed.

## Colors (taken from the Shop Blue site tokens)
| Role | Hex | Site token |
|---|---|---|
| N on light backgrounds | `#3E73D6` | `--brand` (dark mode) |
| A on light backgrounds / brand blue | `#1F4FA3` | `--brand` |
| N on dark backgrounds | `#6E9BF0` | one step lighter than `#3E73D6` |
| A on dark backgrounds | `#3E73D6` | `--brand` (dark mode) |
| Deep band | `#143A80` | `--band` |
| Ink (text on light) | `#0E1B33` | `--ink` |
| Night (dark background) | `#0A1426` | `--bg` (dark mode) |
| Signal red | `#C62A2F` | `--signal` |
| Pale blue | `#AFC1E0` | `--band-muted` |

The mark keeps the original's two-tone logic, a lighter N and a deeper A. On dark backgrounds both shift one step lighter, the same way the site's dark mode does.

## Typeface
**Montserrat Bold (700)** is used for the logo lettering, kept from the original. The site's own headings and body use Big Shoulders Display and Public Sans, and Montserrat sits fine alongside them as a logo face.

## Which file to use on the site
- **Header in light mode:** `01-primary/logo-horizontal-for-light-bg.svg`
- **Header in dark mode:** `01-primary/logo-horizontal-reversed-transparent.svg`
- **On the brand-blue ticker, CTA band or blue footer:** `01-primary/logo-horizontal-on-brand-blue.svg` (white + pale), or `02-one-color/logo-horizontal-white.svg`
- **Square slots:** `01-primary/mark.svg`, `logo-stacked-*`
- **Over photos, red backgrounds, print:** `02-one-color/` (white, navy, blue)
- **PNG fallbacks:** `png/`, where `@600w` means 600 px wide.

Recommended header size: 200–260 px wide on desktop and 160–180 px on mobile.

To swap the logo into the current header, replace the `<span class="badge">N&A</span>` + brand-name pair with:

```html
<a class="brand" href="index.html" aria-label="N&A Auto Repair & Towing Service, home">
  <img src="logo-horizontal-for-light-bg.svg" alt="N&A Auto Repair & Towing Service" width="240" height="68">
</a>
```

## Favicons
Copy `03-favicons/` to the site root. They show a white mark on brand blue, matching the site's blue N&A badge. Add this to `<head>`:

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#1F4FA3">
```

## Social
- `png/04-social/og-image-1200x630.png`: link-preview image on Night blue with a blue/red bottom stripe.
- `png/04-social/profile-avatar.png`: square avatar for Google Business, Facebook and Yelp.

## Alternatives (`05-alternatives/`)
- **A — Refined:** gradient mark plus an "EVANSTON, IL" tagline in signal red.
- **B — Compact header:** a one-line version for the mobile nav.
- **C — Circle badge:** brand blue, for stickers, shirts or the truck door.
- **D — Navy app tile:** an alternate icon.
- **E — Red ampersand:** the & filled in storefront-sign red, tying the logo to the site's red call buttons.
