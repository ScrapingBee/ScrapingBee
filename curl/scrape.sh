#!/usr/bin/env bash
# Fetch a page through the ScrapingBee web scraping API.
# Auth is the Authorization: Bearer header. The api_key query parameter is deprecated.
set -euo pipefail

API_KEY="${SCRAPINGBEE_API_KEY:-YOUR-API-KEY}"

# --data-urlencode lets curl encode the target URL, so nested query strings survive.
# render_js=false keeps this call at 1 credit instead of the 5-credit default.
curl -sS -G "https://app.scrapingbee.com/api/v1" \
  -H "Authorization: Bearer ${API_KEY}" \
  --data-urlencode "url=https://news.ycombinator.com" \
  --data-urlencode "render_js=false" \
  -D headers.txt

echo
grep -i "^spb-" headers.txt
