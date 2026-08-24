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
