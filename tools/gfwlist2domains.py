#!/usr/bin/env python3
"""Convert the upstream gfwlist (base64 AutoProxy) into a plain domain list.

Upstream: https://github.com/gfwlist/gfwlist  (gfwlist.txt, base64-encoded)

Output is one domain per line, sorted and de-duplicated. Sub-domains whose
parent is already present are dropped: the consumer feeds these to dnsmasq as
`server=/<domain>/<resolver>`, which already matches every sub-domain, so
keeping both only bloats the file.

Whitelist rules (`@@`) and regex rules (`/.../`) are skipped: the consumer has
no way to express an exception, and a regex is not a domain.
"""
import base64
import re
import sys
from urllib.request import urlopen

UPSTREAM = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
VALID = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")
# Public suffixes that must never be emitted on their own: routing an entire
# TLD (or a two-label suffix like com.cn) through a different resolver would
# capture far more than intended.
SUFFIXES = {
    "com", "net", "org", "edu", "gov", "info", "biz", "io", "co", "me", "tv",
    "cc", "asia", "mobi", "name", "pro", "xyz", "top", "site", "online",
    "com.cn", "net.cn", "org.cn", "gov.cn", "edu.cn", "com.hk", "com.tw",
    "org.tw", "com.sg", "co.jp", "co.uk", "co.kr", "com.au", "co.nz",
}


def extract(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith(("!", "[")):
        return None
    if line.startswith("@@"):          # whitelist — no way to express it downstream
        return None
    if line.startswith("/") and line.endswith("/"):   # regex rule
        return None
    line = line.lstrip("|")            # ||host  /  |http://host
    line = re.sub(r"^https?://", "", line)
    line = line.split("/")[0]          # drop path
    line = line.split(":")[0]          # drop port
    line = line.lstrip(".")            # .host
    if "*" in line:
        # `*.example.com` is the only wildcard worth keeping; anything else
        # (a*b.com, foo.*) has no sensible domain to extract.
        if not line.startswith("*."):
            return None
        line = line[2:]
    line = line.strip().lower()
    if not VALID.match(line) or line in SUFFIXES:
        return None
    return line


def collapse(domains: set[str]) -> list[str]:
    """Drop d if any proper parent of d is present."""
    out = []
    for d in sorted(domains):
        parts = d.split(".")
        if any(".".join(parts[i:]) in domains for i in range(1, len(parts))):
            continue
        out.append(d)
    return out


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else UPSTREAM
    raw = open(src, "rb").read() if not src.startswith("http") else urlopen(src, timeout=60).read()
    try:
        text = base64.b64decode(raw).decode("utf-8", "ignore")
    except Exception as e:                      # noqa: BLE001
        print(f"decode failed: {e}", file=sys.stderr)
        return 1
    domains = {d for d in (extract(l) for l in text.splitlines()) if d}
    result = collapse(domains)
    if len(result) < 1000:
        print(f"only {len(result)} domains, refusing to emit", file=sys.stderr)
        return 1
    sys.stdout.write("\n".join(result) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
