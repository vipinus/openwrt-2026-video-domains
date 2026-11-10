# openwrt-2026-video-domains

Public domain and IP lists used by the LeoTun router firmware for split
routing. Routers fetch them anonymously, which is why this repository is
public. Routers first try our own mirror of these files and fall back to
`raw.githubusercontent.com`.

## Files in use

| File | What it is | Maintained by |
|---|---|---|
| `direct.txt` | Video CDN domains that bypass the tunnel (`video_direct`). One domain per line, `#` for comments; dnsmasq matches the domain and all its subdomains. | Hand-curated |
| `gfwlist.txt` | Blocked domains that go through the tunnel (blocked-sites-only split mode). **Generated — do not edit.** Upstream [gfwlist](https://github.com/gfwlist/gfwlist) merged with `gfwlist-extra.txt`; sub-domains whose parent is listed are dropped. Consumers reject a file with fewer than 1000 entries. | `.github/workflows/gfwlist-sync.yml`, daily |
| `gfwlist-autoproxy.txt` | Same list in AutoProxy form, for browser proxy extensions that load a rule list by URL. **Generated — do not edit.** | Same workflow step as `gfwlist.txt` |
| `gfwlist-extra.txt` | Additions the upstream gfwlist does not carry. Edit this one, never the generated files. Entries upstream picks up are removed automatically. | Hand-curated |
| `force-cn-cidrs.txt` | Tencent overseas BGP prefixes (AS132203, AS139341) treated as domestic. **Generated.** | `.github/workflows/monthly-force-cn-refresh.yml`, monthly |

The firmware bakes `direct.txt` and `force-cn-cidrs.txt` in at build time;
`gfwlist.txt` is refreshed on the router daily.

## Legacy files (no longer read by current firmware)

`domains.txt` (old name of `direct.txt`), `dns.txt` (retired DNS upstream
list), `supplement.txt`, `blacklist.txt` and `cn-video-full.txt` (inputs of
an earlier list generator). Kept for history only; do not rely on them.

## Contributing to `direct.txt`

Domains must be **pure CDN / segment streaming endpoints**. Do NOT add API,
login, manifest or DRM domains — direct-routing them causes geo-restriction
errors. Verify with `dig` and a traffic capture before opening a PR.

- In: `bilivideo.com` (Bilibili segment CDN), `nflxvideo.net` (Netflix OCA)
- Out: `netflix.com` (control plane, breaks login), `v.qq.com` (API, returns a geo-blocked manifest)

## License

MIT.
