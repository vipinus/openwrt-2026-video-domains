#!/usr/bin/env python3
"""Emit the upstream gfwlist in plain AutoProxy form, with our extras appended.

Two consumers share one source:
  * the router firmware wants a plain domain list  -> gfwlist2domains.py
  * the browser proxy extension (ZeroOmega) wants AutoProxy rules -> this file

Upstream ships AutoProxy base64-encoded. ZeroOmega can read either, but only
re-downloads what its `sourceUrl` points at, so we publish a decoded copy that
already carries `gfwlist-extra.txt` — otherwise proxy users would silently miss
the curated additions the routers get.
"""
import base64
import sys
from urllib.request import urlopen

UPSTREAM = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else UPSTREAM
    raw = open(src, "rb").read() if not src.startswith("http") else urlopen(src, timeout=60).read()
    text = base64.b64decode(raw).decode("utf-8", "ignore").rstrip("\n")
    if not text.startswith("[AutoProxy"):
        print("upstream is not AutoProxy format", file=sys.stderr)
        return 1

    extra = []
    try:
        with open("gfwlist-extra.txt", encoding="utf-8") as fh:
            extra = [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    except FileNotFoundError:
        pass

    out = [text]
    if extra:
        out.append("! ---- curated additions (gfwlist-extra.txt) ----")
        # `||host` matches the domain and every sub-domain, same semantics the
        # firmware gets from `server=/host/...`.
        out += [f"||{d}" for d in sorted(extra)]
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
