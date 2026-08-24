#!/usr/bin/env bash
# Drive the ScrapingBee web scraping API from the terminal with the official CLI.
set -euo pipefail

# One page to stdout.
scrapingbee scrape "https://news.ycombinator.com"

# Let Auto-Mode pick the cheapest configuration that works, capped at 25 credits.
scrapingbee scrape "https://news.ycombinator.com" --mode auto --max-cost 25

# Save a full-page screenshot.
scrapingbee scrape "https://news.ycombinator.com" --screenshot True --screenshot-full-page True
