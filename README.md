# changelinglabs.com

Central hub for [changelinglabs.com](https://changelinglabs.com/) — Changeling Labs' static
`index.html` listing our apps, plus the site-wide `privacy.html`.

> **Brand:** Changeling Labs — *Measure. Optimize. Transform.* The Chrysalis Mark, the
> Electric Deep Blue (`#0056D2`) / Glowing Turquoise (`#00F5FF`) palette and the deep-navy/charcoal
> text system are defined in the brand guide (Obsidian Vault → 💰 Business Ideas → Changeling Labs Branding).
> Keep changes consistent with it.

## Brand assets

The mark in `icons/chrysalis-mark.png`, the PWA icons `icons/icon-{192,512}.png` and the
`icons/lockup.png` banner are extracted directly from the brand guide's own renders (the
transparency spec-sheet image and the style-guide header) by `tools/make-brand-icons.py`:

```sh
python3 tools/make-brand-icons.py   # requires Pillow and read access to the vault
```

Nothing is redrawn or re-generated — the artwork is keyed off its background and cleaned of
the guide's hairlines. Do not hand-edit the PNGs; change the script or the source images instead.

Each app lives in **its own repo** with its own GitHub Pages site, and the hub links to it
at `/<repo>/` (e.g. `iron-log`, `car-wash`) under the shared custom domain. A link to an app
whose repo has no Pages site enabled will 404, so add the card only once the app is deployed.

## Domain & deployment

- `changelinglabs.com` is a **custom domain on this repo's GitHub Pages** (Settings → Pages → Custom domain),
  and is also committed as a **`CNAME`** file so the config travels with the repo.
- DNS (registrar: Spaceship) points the apex at GitHub Pages (`CNAME edmundashdown.github.io` + the
  four `185.199.10x.153` A records). Until the GitHub org exists, the serving repo keeps its name
  `edmundashdown.github.io` — renaming it would drop the `edmundashdown.github.io → changelinglabs.com`
  redirect and orphan deep links. Nothing on the site presents the name.
- `edmundashdown.github.io/*` redirects to `changelinglabs.com/*`, so old links keep working.
- **App data is origin-scoped.** Apps served from `changelinglabs.com` share that origin (as they
  previously shared `edmundashdown.github.io`) — IndexedDB/localStorage do not cross over, so switching
  a user between the two origins starts them with a fresh store (export/import covers moving data).

## Styling

Tailwind is compiled to a static stylesheet. There is no CDN and no runtime build.

**`css/styles.css` is committed** — GitHub Pages serves this repo statically and does not
run a build step, so the built file must be in the repo.

After editing `index.html` or `privacy.html` (especially when adding new utility classes),
rebuild and commit the output:

```sh
npm install        # first time only
npm run build:css  # rewrites css/styles.css
```

`npm run watch:css` rebuilds on save while working locally.

**Cache-busting:** Pages serves `css/styles.css` with a 10-minute cache, so a stale
stylesheet can survive a push and render new markup with old styles. The link tag in
`index.html`/`privacy.html` carries a `?v=<date>-<n>` suffix — **bump it whenever the CSS changes**,
and browsers with the old file fetch the new one immediately.

Source of truth for the stylesheet is `src/input.css` plus the theme in
`tailwind.config.js` (the `brand` ramp is Electric Deep Blue). Tailwind scans `./index.html`
and `./privacy.html` for class names (the `content` array).

## Adding an app card

1. Deploy the app (own repo + its own Pages site or a path on this domain).
2. Add a card to `index.html` — one accent hue per card, applied end-to-end
   (icon tile → status pill → Launch CTA), everything else neutral.
3. `npm run build:css`, bump the `?v=` cache-bust, commit, push.
4. Link the app's repo from the hub and note it in `privacy.html` if it stores data.

## Future: migrating to the `changelinglabs` org

The optimal end state is a GitHub org `changelinglabs` with the hub as `changelinglabs.github.io`
and the app repos transferred into it. GitHub redirects old repo URLs automatically after a
transfer, so history and most links survive. The critical sequence:

1. Create the `changelinglabs` org (needs an org-admin account — the hub currently lives under a personal account).
2. Create `changelinglabs.github.io` in the org with the hub contents.
3. Move the custom domain to it (Pages settings → custom domain `changelinglabs.com`).
4. Transfer `pulse`, `iron-log`, `bible-tracker`, `car-wash` into the org one at a time.
5. Point source-code links in `index.html`/`privacy.html`/READMEs at `github.com/changelinglabs/*`.
6. Keep the user-site repo until the org site builds; then retire it or leave it as a redirect-free archive.

Until step 3 happens, **do not** change `CNAME` or Pages settings here — the domain serves from this repo.

 
x