# Web scraping from the shell with curl

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="https://github.com/user-attachments/assets/78927667-6375-4266-bd58-e049208a4922" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

The shortest path to a first response. Useful for checking a target before writing any code.

## Prerequisites

- curl, preinstalled on macOS and most Linux distributions
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
chmod +x scrape.sh
```

## The example

```bash
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
```

## Run it

```bash
./scrape.sh
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.

### Why `--data-urlencode`

Target URLs usually carry their own query string. Passing one unencoded truncates the
request at the first `&`. Letting curl encode it with `-G` and `--data-urlencode` keeps
the full target intact.

## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
