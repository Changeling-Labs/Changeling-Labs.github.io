# edmundashdown.github.io

Central hub for [edmundashdown.github.io](https://edmundashdown.github.io/) — a static
`index.html` listing the apps, plus the site-wide `privacy.html`.

Each app lives in **its own repo** with its own GitHub Pages site, and the hub links to it
at `/<repo>/` (e.g. `iron-log`, `car-wash`). A link to an app whose repo has no
Pages site enabled will 404, so add the card only once the app is deployed.

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
`index.html`/`privacy.html` carries a `?v=<date>-<n>` suffix — **bump it whenever the
CSS changes**, and browsers with the old file fetch the new one immediately.

Source of truth for the stylesheet is `src/input.css` plus the theme in
`tailwind.config.js` (the `brand` colour ramp and `darkMode: 'class'`). Tailwind scans
`./index.html` and `./privacy.html` for class names (the `content` array), including
classes that appear only inside JavaScript strings.
