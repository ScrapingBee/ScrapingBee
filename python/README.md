# Python web scraping with the ScrapingBee API

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="REPLACE_WITH_SCREENSHOT_URL" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

Two ways to call the API from Python: raw `requests`, shown below, or the official SDK.

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
pip install -r requirements.txt
```

## The example

```python
"""Fetch a page through the ScrapingBee web scraping API.

Auth is the Authorization: Bearer header. The api_key query parameter is deprecated.
"""

import os
import requests

API_URL = "https://app.scrapingbee.com/api/v1"
API_KEY = os.environ.get("SCRAPINGBEE_API_KEY", "YOUR-API-KEY")


def scrape(url, **params):
    response = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"url": url, **params},
        timeout=140,
    )
    response.raise_for_status()
    return response


if __name__ == "__main__":
    # render_js=false keeps this call at 1 credit instead of the 5-credit default.
    response = scrape("https://news.ycombinator.com", render_js="false")

    print("status:", response.status_code)
    print("credits:", response.headers.get("Spb-cost"))
    print("request id:", response.headers.get("Spb-request-id"))
    print(response.text[:500])
```

## Run it

```bash
python scrape.py
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.

### Using the official SDK instead

```bash
pip install scrapingbee
```

```python
from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='YOUR-API-KEY')
response = client.get('https://news.ycombinator.com', params={'render_js': False})
print(response.content)
```

The SDK covers the HTML API and the Google, Amazon, Walmart, YouTube, ChatGPT and Gemini endpoints.

## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
