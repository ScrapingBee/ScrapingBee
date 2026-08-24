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
