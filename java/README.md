# Java web scraping with the ScrapingBee API

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="https://github.com/user-attachments/assets/78927667-6375-4266-bd58-e049208a4922" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

Built on `java.net.http`, so there is no build tool and no dependency to resolve.

## Prerequisites

- [Java 11+](https://www.oracle.com/java/technologies/downloads/)
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
# No install step. Java 11 and later run a single source file directly.
```

## The example

```java
// Fetch a page through the ScrapingBee web scraping API.
// Auth is the Authorization: Bearer header. The api_key query parameter is deprecated.
//
// Java 11+ runs this file directly, no build tool and no dependencies:
//   java Scrape.java

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;

public class Scrape {

    private static final String API_URL = "https://app.scrapingbee.com/api/v1";

    private static String apiKey() {
        String key = System.getenv("SCRAPINGBEE_API_KEY");
        return (key == null || key.isEmpty()) ? "YOUR-API-KEY" : key;
    }

    private static String encode(String value) {
        return URLEncoder.encode(value, StandardCharsets.UTF_8);
    }

    static HttpResponse<String> scrape(String target, String extraParams) throws Exception {
        String query = "?url=" + encode(target) + extraParams;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL + query))
                .header("Authorization", "Bearer " + apiKey())
                .GET()
                .build();

        return HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
    }

    public static void main(String[] args) throws Exception {
        // render_js=false keeps this call at 1 credit instead of the 5-credit default.
        HttpResponse<String> response = scrape("https://news.ycombinator.com", "&render_js=false");

        System.out.println("status: " + response.statusCode());
        System.out.println("credits: " + response.headers().firstValue("Spb-cost").orElse("n/a"));
        System.out.println("request id: " + response.headers().firstValue("Spb-request-id").orElse("n/a"));

        String body = response.body();
        System.out.println(body.substring(0, Math.min(500, body.length())));
    }
}
```

## Run it

```bash
java Scrape.java
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.

### On the file name

The class is `Scrape`, so the file must be `Scrape.java`. Renaming one without the other
stops the file compiling.

## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
