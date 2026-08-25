# ScrapingBee Web Scraping API

[![checks](https://github.com/ScrapingBee/ScrapingBee/workflows/checks/badge.svg)](https://github.com/ScrapingBee/ScrapingBee/actions)
[![pypi](https://img.shields.io/pypi/v/web-scraping-api-sdk.svg)](https://pypi.org/project/web-scraping-api-sdk/)
[![python](https://img.shields.io/pypi/pyversions/web-scraping-api-sdk.svg)](https://pypi.org/project/web-scraping-api-sdk/)
[![npm](https://img.shields.io/npm/v/web-scraping-api-sdk.svg)](https://www.npmjs.com/package/web-scraping-api-sdk)
[![node](https://img.shields.io/node/v/web-scraping-api-sdk.svg)](https://www.npmjs.com/package/web-scraping-api-sdk)
[![license](https://img.shields.io/github/license/ScrapingBee/ScrapingBee.svg)](LICENSE)

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="https://github.com/user-attachments/assets/78927667-6375-4266-bd58-e049208a4922" alt="ScrapingBee" />
  </a>
</p>




ScrapingBee is a [web scraping API](https://www.scrapingbee.com/features/ai-web-scraping-api/) that takes one HTTP request and returns the rendered page, a screenshot, or structured JSON. It runs the headless browser, rotates the proxies, and handles the anti-bot layer, so the only thing your code sends is a URL and a few parameters.

This repository holds runnable examples for every endpoint, in eight languages, with the exact parameters and credit costs from the official documentation.

## Contents

- [How it works](#how-it-works)
- [What a request costs](#what-a-request-costs)
- [Auto-Mode](#auto-mode)
- [Quickstart](#quickstart)
- [Examples by language](#examples-by-language)
- [Dedicated scrapers](#dedicated-scrapers)
- [Integrations](#integrations)
- [Use cases](#use-cases)
- [Parameters](#parameters)
- [License](#license)

## How it works

Every call goes to one base endpoint and authenticates with a Bearer token:

```bash
curl "https://app.scrapingbee.com/api/v1?url=YOUR-URL" \
     -H "Authorization: Bearer YOUR-API-KEY"
```

Passing the key as an `api_key` query parameter still works but is deprecated. Use the `Authorization` header for anything new.

Three things happen behind that request:

1. **Proxy selection.** Rotating datacenter IPs by default, residential IPs with `premium_proxy=true`, anti-bot-grade IPs with `stealth_proxy=true`.
2. **Rendering.** A real browser executes the page JavaScript. On by default, switched off with `render_js=false`. Default wait is 2000ms, adjustable with `wait`, `wait_for`, or `wait_browser`.
3. **Extraction.** Return raw HTML, text, markdown, a PNG screenshot, or JSON shaped by CSS selectors (`extract_rules`) or a natural-language prompt (`ai_query`, `ai_extract_rules`).

Get an API key from the [ScrapingBee dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts start with 1,000 free credits and no card.

## What a request costs

Credits are charged per successful call, and the amount depends only on which configuration you asked for:

| Configuration | Credits |
| --- | --- |
| Rotating proxy, no JavaScript | 1 |
| Rotating proxy with JavaScript (default) | 5 |
| Premium proxy, no JavaScript | 10 |
| Premium proxy with JavaScript | 25 |
| Stealth proxy, no JavaScript | coming soon |
| Stealth proxy with JavaScript | 75 |
| `ai_query` or `ai_extract_rules` | +5 on top of the base cost |

So `render_js=true` with `ai_query` costs 10. Add `premium_proxy=true` and it costs 30. A 500 response is not charged, which makes retrying on 500 safe. Every response carries the exact figure in the `Spb-cost` header, and `/api/v1/usage` reports the running total (6 calls per minute, real time).

## Auto-Mode

Picking the proxy tier by hand means either overpaying on easy pages or getting blocked on hard ones. `mode=auto` removes the guess. ScrapingBee tries configurations from cheapest to most expensive, stops at the first one that returns the page, and charges only for that one:

```bash
curl "https://app.scrapingbee.com/api/v1?url=YOUR-URL&mode=auto" \
     -H "Authorization: Bearer YOUR-API-KEY"
```

The charge lands on one of 1, 5, 10, 25 or 75 credits. **If every configuration fails, the request costs 0 credits.** The figure charged comes back in the `Spb-auto-cost` header.

Cap how far it is allowed to climb with `max_cost`:

```bash
curl "https://app.scrapingbee.com/api/v1?url=YOUR-URL&max_cost=25&mode=auto" \
     -H "Authorization: Bearer YOUR-API-KEY"
```

`max_cost=25` lets Auto-Mode reach premium proxy with JavaScript but never the 75-credit stealth tier.

## Quickstart

```bash
curl "https://app.scrapingbee.com/api/v1?url=https%3A%2F%2Fnews.ycombinator.com&render_js=false" \
     -H "Authorization: Bearer YOUR-API-KEY"
```

```python
import requests

response = requests.get(
    "https://app.scrapingbee.com/api/v1",
    headers={"Authorization": "Bearer YOUR-API-KEY"},
    params={"url": "https://news.ycombinator.com", "render_js": "false"},
)

print(response.status_code, response.headers.get("Spb-cost"))
print(response.text)
```

```javascript
const response = await fetch(
  "https://app.scrapingbee.com/api/v1?" +
    new URLSearchParams({ url: "https://news.ycombinator.com", render_js: "false" }),
  { headers: { Authorization: "Bearer YOUR-API-KEY" } }
);

console.log(response.status, response.headers.get("spb-cost"));
console.log(await response.text());
```

HTTP/2 lowercases header names, so read `Spb-cost` and `Spb-request-id` case-insensitively.

## Examples by language

Each folder is self-contained: a script, a dependency manifest, and a README covering install, configuration and the run command.

| Folder | Runtime | Client used |
| --- | --- | --- |
| [python](python/) | Python 3.8+ | `requests`, plus the official `scrapingbee` SDK |
| [nodejs](nodejs/) | Node 18+ | built-in `fetch`, plus the official `scrapingbee` SDK |
| [curl](curl/) | any shell | curl |
| [cli](cli/) | Python 3.8+ | `scrapingbee-cli` |
| [go](go/) | Go 1.21+ | `net/http` |
| [java](java/) | Java 11+ | `java.net.http` |
| [php](php/) | PHP 8.0+ | cURL extension |
| [ruby](ruby/) | Ruby 3.0+ | `net/http` |

## Dedicated scrapers

Nine endpoints return parsed JSON, so there is no HTML to select against and no selectors to repair when a layout changes.

| Scraper | Endpoint | Credits |
| --- | --- | --- |
| [Google](https://www.scrapingbee.com/documentation/google-api/) | `/api/v1/google` | 10 light, 15 standard |
| [Fast Search](https://www.scrapingbee.com/documentation/fast-search/) | `/api/v1/fast_search` | 10 |
| [Amazon](https://www.scrapingbee.com/documentation/amazon/) | `/api/v1/amazon/search`, `/product`, `/pricing` | 5 light, 15 standard |
| [Walmart](https://www.scrapingbee.com/documentation/walmart/) | `/api/v1/walmart/search`, `/product` | 10 light, 15 standard |
| [YouTube](https://www.scrapingbee.com/documentation/youtube/) | `/api/v1/youtube/search`, `/metadata`, `/subtitles` | 5 |
| [ChatGPT](https://www.scrapingbee.com/documentation/chatgpt/) | `/api/v1/chatgpt` | 15 |
| [Gemini](https://www.scrapingbee.com/documentation/gemini/) | `/api/v1/gemini` | 15 |
| [Shopee](https://www.scrapingbee.com/documentation/shopee/) | `/api/v1/shopee` | 75 |
| [Agentic Employee Search](https://www.scrapingbee.com/documentation/agentic-employee-search/) | `/api/v1/agentic_search` | 3,750 |

The Google endpoint covers eight surfaces through one `search_type` parameter:

| `search_type` | Returns | Landing page |
| --- | --- | --- |
| `classic` | Organic results, the default | [Google search API](https://www.scrapingbee.com/scrapers/google-search-api/) |
| `news` | News results | [Google News API](https://www.scrapingbee.com/scrapers/google-news-api/) |
| `maps` | Local listings | [Google Maps API](https://www.scrapingbee.com/scrapers/google-maps-api/) |
| `images` | Image results | [Google Images API](https://www.scrapingbee.com/scrapers/images-results-api/) |
| `lens` | Visual matches for an image URL | [Google Lens API](https://www.scrapingbee.com/scrapers/google-lens-api/) |
| `shopping` | Product listings, sortable and price-filtered | [Google Shopping API](https://www.scrapingbee.com/scrapers/google-shopping-api/) |
| `ai_mode` | The AI-generated answer, 400-character query cap | [Google AI Mode API](https://www.scrapingbee.com/scrapers/google-ai-mode-api/) |
| `ads` | Paid placements | [Google Ads API](https://www.scrapingbee.com/scrapers/google-ads-api/) |

```bash
curl -G "https://app.scrapingbee.com/api/v1/google" \
     -H "Authorization: Bearer YOUR-API-KEY" \
     --data-urlencode "search=web scraping api" \
     --data-urlencode "search_type=news" \
     --data-urlencode "country_code=us"
```

Two notes from the documentation: `search_type=news` is not available with `device=mobile`, and `search_type=lens` accepts image URLs only. ChatGPT responses return citations when the prompt produces them, not on every call.

## Integrations

**Official SDKs**

- [scrapingbee-python](https://github.com/ScrapingBee/scrapingbee-python), `pip install scrapingbee`
- [scrapingbee-node](https://github.com/ScrapingBee/scrapingbee-node), `npm install scrapingbee`
- [scrapingbee-cli](https://github.com/ScrapingBee/scrapingbee-cli), `pip install scrapingbee-cli`

**Frameworks**

- [scrapy-scrapingbee](https://github.com/ScrapingBee/scrapy-scrapingbee) middleware for Scrapy
- [Proxy Mode](https://www.scrapingbee.com/documentation/proxy-mode/) points Selenium, Postman or any HTTP client at the API without rewriting the request layer

**AI and agents**

- [langchain-scrapingbee](https://github.com/ScrapingBee/langchain-scrapingbee) document loaders, see the [LangChain docs](https://www.scrapingbee.com/documentation/langchain/)
- [mcp-server](https://github.com/ScrapingBee/mcp-server) gives MCP clients live web access, also available as a [remote MCP endpoint](https://www.scrapingbee.com/documentation/remote-mcp/)

**No-code**

- [n8n](https://www.scrapingbee.com/documentation/n8n/) via [scrapingbee-n8n](https://github.com/ScrapingBee/scrapingbee-n8n)
- [Zapier](https://www.scrapingbee.com/documentation/zapier/) and [Make](https://www.scrapingbee.com/documentation/make/)

## Use cases

Worked examples that go past a single request:

| Repository | What it builds |
| --- | --- |
| [google-search-api](https://github.com/ScrapingBee/google-search-api) | Paginated SERP collection with structured output |
| [ai-web-scraper](https://github.com/ScrapingBee/ai-web-scraper) | Extraction driven by a natural-language prompt |
| [amazon-review-scraper](https://github.com/ScrapingBee/amazon-review-scraper) | Review pagination and rating breakdowns |
| [youtube-scraper-api](https://github.com/ScrapingBee/youtube-scraper-api) | Video metadata, search results and transcripts |
| [google-flights-scraper](https://github.com/ScrapingBee/google-flights-scraper) | Live fares, routes and schedules |
| [google-jobs-api](https://github.com/ScrapingBee/google-jobs-api) | Job listings with company and location fields |
| [costco-scraper](https://github.com/ScrapingBee/costco-scraper) | Retail product data and pricing |
| [n8n-no-code-web-scraper](https://github.com/ScrapingBee/n8n-no-code-web-scraper) | A scraping workflow without writing code |

## Parameters

The full set accepted by `/api/v1`, documented in the [API reference](https://www.scrapingbee.com/documentation/):

| Group | Parameters |
| --- | --- |
| Request | `url`, `api_key`, `tag`, `timeout`, `transparent_status_code`, `scraping_config` |
| Proxies | `premium_proxy`, `stealth_proxy`, `own_proxy`, `country_code`, `session_id` |
| Cost control | `mode`, `max_cost` |
| Rendering | `render_js`, `wait`, `wait_for`, `wait_browser`, `js_scenario`, `block_ads`, `block_resources`, `device`, `window_width`, `window_height` |
| Output | `return_page_source`, `return_page_text`, `return_page_markdown`, `json_response`, `screenshot`, `screenshot_full_page`, `screenshot_selector` |
| Extraction | `extract_rules`, `ai_query`, `ai_selector`, `ai_extract_rules` |
| Headers and cookies | `forward_headers`, `forward_headers_pure`, `cookies` |

Response headers worth reading: `Spb-cost`, `Spb-auto-cost`, `Spb-initial-status-code`, `Spb-resolved-url`, and `Spb-request-id`, which identifies the call in support requests.

## Scope

These examples target publicly accessible pages. Scraping behind login credentials is prohibited by the [ScrapingBee terms](https://www.scrapingbee.com/terms-and-conditions/). Keep your API key out of shared environments, including AI coding assistants.

## License

MIT. See [LICENSE](LICENSE).

Documentation: [scrapingbee.com/documentation](https://www.scrapingbee.com/documentation/) - Plans and credits: [scrapingbee.com/pricing](https://www.scrapingbee.com/pricing/)
