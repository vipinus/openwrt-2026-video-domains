# openwrt-2026-video-domains

Domain list consumed by the `video_direct` feature in
[openwrt-2026](https://github.com/vipinus/openwrt-2026).
The firmware fetches `direct.txt` via weekly cron.

## Files

- `direct.txt` — one domain per line; `#` for comments.
  Matches parent-domain and all subdomains via dnsmasq-full nftset.
- `gfwlist.txt` — one domain per line; `#` for comments. **Generated —
  do not edit.** Synced daily from [gfwlist](https://github.com/gfwlist/gfwlist)
  by `.github/workflows/gfwlist-sync.yml`, merged with `gfwlist-extra.txt`.
  A parent domain already covers its sub-domains, so sub-domains whose parent
  is present are dropped. Consumers reject a file with fewer than 1000 entries,
  so a truncated download cannot wipe a working list.
- `gfwlist-autoproxy.txt` — **generated — do not edit.** The same source in
  AutoProxy form, for browser proxy extensions (ZeroOmega and friends) that
  fetch a rule list by URL. Produced in the same workflow step as
  `gfwlist.txt`, so the router list and the browser list cannot drift apart.
- `gfwlist-extra.txt` — manually curated additions merged into both generated
  files. Edit this one, never the generated ones.

## Contributing

Domains must be **pure CDN / segment streaming endpoints**.
Do NOT add API, login, manifest, or DRM domains — they will cause
geo-restriction errors when direct-routed. Verify with `dig` + traffic
capture before opening a PR.

Examples of what goes in:
- `bilivideo.com` (Bilibili segment CDN)
- `nflxvideo.net` (Netflix OCA)
- `apdcdn.tc.qq.com` (Tencent Video APD CDN)

Examples of what does NOT belong:
- `netflix.com` (control plane, would break login)
- `v.qq.com` (API, would return geo-blocked manifest)

## License

MIT.
