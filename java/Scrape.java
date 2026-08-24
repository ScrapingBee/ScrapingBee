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
