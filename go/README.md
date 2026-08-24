# Go web scraping with the ScrapingBee API

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="REPLACE_WITH_SCREENSHOT_URL" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

Standard library only. `net/http` and `net/url` cover everything the API needs.

## Prerequisites

- [Go 1.21+](https://golang.org/dl/)
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
go mod tidy
```

## The example

```go
// Fetch a page through the ScrapingBee web scraping API.
// Auth is the Authorization: Bearer header. The api_key query parameter is deprecated.
package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
)

const apiURL = "https://app.scrapingbee.com/api/v1"

func scrape(target string, params map[string]string) (*http.Response, error) {
	apiKey := os.Getenv("SCRAPINGBEE_API_KEY")
	if apiKey == "" {
		apiKey = "YOUR-API-KEY"
	}

	query := url.Values{}
	query.Set("url", target)
	for key, value := range params {
		query.Set(key, value)
	}

	req, err := http.NewRequest("GET", apiURL+"?"+query.Encode(), nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+apiKey)

	return (&http.Client{}).Do(req)
}

func main() {
	// render_js=false keeps this call at 1 credit instead of the 5-credit default.
	resp, err := scrape("https://news.ycombinator.com", map[string]string{"render_js": "false"})
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("status:", resp.Status)
	fmt.Println("credits:", resp.Header.Get("Spb-cost"))
	fmt.Println("request id:", resp.Header.Get("Spb-request-id"))
	fmt.Println(string(body[:min(500, len(body))]))
}
```

## Run it

```bash
go run scrape.go
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.


## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
