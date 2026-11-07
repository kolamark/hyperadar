#!/usr/bin/env python3
"""Collect RSS metadata for editorial review. Never publishes articles."""
import json
import hashlib
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEDS = json.loads((ROOT / "config" / "feeds.json").read_text(encoding="utf-8"))
OUT = ROOT / "data" / "candidates.json"


def clean_url(raw):
    parsed = urllib.parse.urlsplit(raw.strip())
    if parsed.scheme not in ("http", "https"):
        return ""
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query = [(k, v) for k, v in query if not k.lower().startswith("utm_")]
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/"), urllib.parse.urlencode(query), ""))


def parse_feed(xml, source):
    root = ET.fromstring(xml)
    atom = "{http://www.w3.org/2005/Atom}"
    items = root.findall(".//item") if root.tag != atom + "feed" else root.findall(atom + "entry")
    found = []
    for item in items:
        title = (item.findtext("title") or item.findtext(atom + "title") or "").strip()
        link = item.findtext("link") or ""
        if not link:
            atom_link = item.find(atom + "link")
            link = atom_link.get("href", "") if atom_link is not None else ""
        url = clean_url(link)
        if not title or not url:
            continue
        raw_date = item.findtext("pubDate") or item.findtext(atom + "published") or item.findtext(atom + "updated") or ""
        try:
            date = parsedate_to_datetime(raw_date) if "," in raw_date else datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            published = date.astimezone(timezone.utc).isoformat()
        except (ValueError, TypeError):
            published = None
        found.append({"id": hashlib.sha256(url.encode()).hexdigest()[:20], "source": source["name"],
                      "category": source["category"], "original_title": title, "url": url,
                      "published_at": published, "status": "candidate"})
    return found


def collect():
    existing = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else []
    by_id = {entry["id"]: entry for entry in existing}
    errors = []
    for feed in FEEDS:
        try:
            request = urllib.request.Request(feed["url"], headers={"User-Agent": "HypeRadarEditorial/0.1 (+https://github.com/kolamark/hyperadar)"})
            with urllib.request.urlopen(request, timeout=15) as response:
                xml = response.read(2_000_001)
            if len(xml) > 2_000_000:
                raise ValueError("Feed too large")
            for entry in parse_feed(xml, feed):
                by_id.setdefault(entry["id"], entry)
        except (OSError, ValueError, ET.ParseError) as exc:
            errors.append(f'{feed["name"]}: {type(exc).__name__}: {exc}')
    entries = sorted(by_id.values(), key=lambda e: e["published_at"] or "", reverse=True)[:1000]
    OUT.parent.mkdir(exist_ok=True)
    result = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != result:
        OUT.write_text(result, encoding="utf-8")
    print(f"{len(entries)} candidates stored; {len(errors)} feed errors")
    for error in errors:
        print(error)
    if errors and len(errors) == len(FEEDS):
        raise SystemExit(1)
    return entries


if __name__ == "__main__":
    collect()
