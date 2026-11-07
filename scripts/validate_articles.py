#!/usr/bin/env python3
"""Reject malformed or unsourced published article data."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from publish import looks_hungarian

root = Path(__file__).resolve().parents[1]
path = root / "articles.json" if (root / "articles.json").exists() else root / "dist" / "articles.json"
data = json.loads(path.read_text(encoding="utf-8"))
assert isinstance(data, dict) and isinstance(data.get("articles"), list), "articles list missing"
titles = set()
for i, article in enumerate(data["articles"], 1):
    where = f"article {i}"
    assert article.get("status") == "published", f"{where}: invalid status"
    assert article.get("category") in ("gaming", "bulvar"), f"{where}: invalid category"
    for field, minimum, maximum in (("title", 12, 140), ("excerpt", 30, 260)):
        value = article.get(field)
        assert isinstance(value, str) and minimum <= len(value.strip()) <= maximum, f"{where}: invalid {field}"
        assert "<" not in value and ">" not in value, f"{where}: HTML not allowed"
    title = article["title"].strip().casefold()
    assert title not in titles, f"{where}: duplicate title"
    titles.add(title)
    body = article.get("body")
    assert isinstance(body, list) and len(body) >= 2 and all(isinstance(p, str) and p.strip() for p in body), f"{where}: invalid body"
    assert len(re.findall(r"\S+", " ".join(body))) >= 120, f"{where}: too short"
    assert looks_hungarian(article["title"], article["excerpt"], body), f"{where}: Hungarian language check failed"
    assert isinstance(article.get("claims"), list) and len(article["claims"]) >= max(2, len(body)), f"{where}: insufficient evidenced claims"
    sources = article.get("sources")
    assert isinstance(sources, list) and sources, f"{where}: no sources"
    for source in sources:
        assert isinstance(source, dict) and isinstance(source.get("name"), str) and source["name"].strip(), f"{where}: source name missing"
        url = urlsplit(source.get("url", ""))
        assert url.scheme == "https" and url.hostname and not url.username and not url.password, f"{where}: invalid source URL"
    assert isinstance(article.get("published_at"), str) and article["published_at"].endswith("Z"), f"{where}: invalid UTC timestamp"
print(f"Validated {len(data['articles'])} published articles")
