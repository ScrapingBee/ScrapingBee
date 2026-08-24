# Web scraping from the terminal with the ScrapingBee CLI

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="REPLACE_WITH_SCREENSHOT_URL" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

The official CLI wraps the same API, adds batch input, sitemap crawling and scheduling.

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
pip install -r requirements.txt
```

## The example

```bash
#!/usr/bin/env bash
# Drive the ScrapingBee web scraping API from the terminal with the official CLI.
set -euo pipefail

# One page to stdout.
scrapingbee scrape "https://news.ycombinator.com"

# Let Auto-Mode pick the cheapest configuration that works, capped at 25 credits.
scrapingbee scrape "https://news.ycombinator.com" --mode auto --max-cost 25

# Save a full-page screenshot.
scrapingbee scrape "https://news.ycombinator.com" --screenshot True --screenshot-full-page True
```

## Run it

```bash
./scrape.sh
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.

### Configuration

The CLI reads the key from the environment:

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
```

Beyond single pages it handles `scrapingbee crawl --from-sitemap`, batch runs with
`--input-file`, in-place CSV enrichment with `--update-csv`, and recurring jobs with
`scrapingbee schedule`. Full command reference in the
[CLI documentation](https://www.scrapingbee.com/documentation/cli/).

## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
