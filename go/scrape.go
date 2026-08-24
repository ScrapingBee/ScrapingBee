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
