# t0x.dev GitHub Pages setup (how it is today + how to finish HTTPS)

## What is already in place

- **Repo:** https://github.com/t0xstandard/T0x (branch `main`)
- **Pages source:** deploy from `main` root (Jekyll builds `Readme.md` into the site)
- **Custom domain file:** repo root `CNAME` contains exactly:
  ```
  t0x.dev
  ```
- **DNS (apex):** `t0x.dev` has **A records** to GitHub Pages (no CNAME on the apex):
  - 185.199.108.153
  - 185.199.109.153
  - 185.199.110.153
  - 185.199.111.153
- **www:** not configured (no `www.t0x.dev` CNAME)
- **HTTPS today:** broken — TLS presents the default `*.github.io` certificate, so strict clients fail and browsers warn. Plain HTTP still serves the site. Jekyll canonical / og links were `http://t0x.dev/` because no `_config.yml` set `url: https://t0x.dev`.

## Files to drop into the repo

1. `t0x.py` — restored `m.group(...)` lookups, UTC-only parse, left-padded ms
2. `Readme.md` (and optionally `Readme`) — spec wording locked to 19-char / required 3-digit ms; site link uses `https://t0x.dev`
3. `_config.yml` — `url: "https://t0x.dev"` so generated canonical and Open Graph URLs are HTTPS
4. Keep existing `CNAME` as `t0x.dev`

## Steps for John (HTTPS clean)

1. Commit and push the three files above to `main` on `t0xstandard/T0x`.
2. GitHub → **Settings → Pages**:
   - Source: Deploy from branch `main` / `/ (root)`
   - Custom domain: `t0x.dev` (should match `CNAME`)
   - Wait until the DNS check is green
   - Enable **Enforce HTTPS** (only available after GitHub finishes issuing the Let’s Encrypt cert for `t0x.dev`)
3. DNS (if anything drifted): keep the four A records above on `@` / apex. Optional: `www` → CNAME to `t0xstandard.github.io` (or the pages host GitHub shows).
4. Verify:
   - `curl -I https://t0x.dev` succeeds **without** `-k` / insecure
   - Certificate SAN includes `t0x.dev`
   - View source: `rel="canonical"` and `og:url` are `https://t0x.dev/`
