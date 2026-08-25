# JavaScript web scraping with the ScrapingBee API

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="https://github.com/user-attachments/assets/78927667-6375-4266-bd58-e049208a4922" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

Node 18 and later ship `fetch`, so this example needs no dependencies at all.

## Prerequisites

- [Node.js 18+](https://nodejs.org/en/download/)
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
npm install
```

## The example

```javascript
// Fetch a page through the ScrapingBee web scraping API.
// Auth is the Authorization: Bearer header. The api_key query parameter is deprecated.

const API_URL = "https://app.scrapingbee.com/api/v1";
const API_KEY = process.env.SCRAPINGBEE_API_KEY || "YOUR-API-KEY";

async function scrape(url, params = {}) {
  const query = new URLSearchParams({ url, ...params });
  const response = await fetch(`${API_URL}?${query}`, {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });

  if (!response.ok) {
    throw new Error(`${response.status}: ${await response.text()}`);
  }
  return response;
}

// render_js=false keeps this call at 1 credit instead of the 5-credit default.
scrape("https://news.ycombinator.com", { render_js: "false" })
  .then(async (response) => {
    // HTTP/2 lowercases header names, so read them case-insensitively.
    console.log("status:", response.status);
    console.log("credits:", response.headers.get("spb-cost"));
    console.log("request id:", response.headers.get("spb-request-id"));
    console.log((await response.text()).slice(0, 500));
  })
  .catch((error) => console.error(error.message));
```

## Run it

```bash
node scrape.js
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.

### Using the official SDK instead

```bash
npm install scrapingbee
```

```javascript
const scrapingbee = require('scrapingbee');

const client = new scrapingbee.ScrapingBeeClient('YOUR-API-KEY');
const response = await client.get({ url: 'https://news.ycombinator.com', params: { render_js: false } });
console.log(new TextDecoder().decode(response.data));
```

## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
