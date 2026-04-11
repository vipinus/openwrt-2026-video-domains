# openwrt-2026-video-domains

Supplement and blacklist for the `video_direct` feature in
[openwrt-2026](https://github.com/vipinus/openwrt-2026) firmware.
Consumed at firmware build time AND on-router via weekly cron refresh.

## Files

- `supplement.txt` — domains not covered by v2fly community lists
- `blacklist.txt` — control-plane domains that must never enter the direct set

## Contributing a new streaming CDN domain

1. **Verify the domain is a pure CDN endpoint.** Use:

   ```
   dig +short your-domain.example.com
   whois $(dig +short your-domain.example.com | head -1)
   ```

   Confirm the IP belongs to a CDN provider (Akamai, Fastly, China
   Telecom CDN, Tencent Cloud CDN, etc.) and not the site's origin
   backend.

2. **Verify it is NOT an API/login/manifest domain.** Test by fetching
   it with curl and checking the Content-Type. JSON/HTML → API, reject.
   video/mp2t or application/octet-stream → CDN, accept.

3. **Open a PR** adding the domain to `supplement.txt` under the
   appropriate platform comment. Include your verification output.

4. **PRs without verification evidence are rejected.** We maintain
   this list fact-driven, not speculatively.

## Blacklist updates

If a v2fly category accidentally includes an API domain that should
not be direct-routed, add it to `blacklist.txt`. This takes effect on
the next firmware build OR the next weekly cron refresh on routers.

## License

MIT.
