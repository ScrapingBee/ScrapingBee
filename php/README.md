# PHP web scraping with the ScrapingBee API

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="https://github.com/user-attachments/assets/78927667-6375-4266-bd58-e049208a4922" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

Uses the bundled cURL extension. No Composer packages required.

## Prerequisites

- [PHP 8.0+](https://www.php.net/manual/en/install.php) with the cURL extension enabled
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
# No install step. Confirm cURL is on with `php -m | grep curl`.
```

## The example

```php
<?php
// Fetch a page through the ScrapingBee web scraping API.
// Auth is the Authorization: Bearer header. The api_key query parameter is deprecated.

const API_URL = 'https://app.scrapingbee.com/api/v1';

function scrape(string $target, array $params = []): array
{
    $apiKey = getenv('SCRAPINGBEE_API_KEY') ?: 'YOUR-API-KEY';
    $query = http_build_query(array_merge(['url' => $target], $params));

    $ch = curl_init(API_URL . '?' . $query);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Authorization: Bearer ' . $apiKey]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, true);

    $raw = curl_exec($ch);
    if ($raw === false) {
        throw new RuntimeException('Request failed: ' . curl_error($ch));
    }

    $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return [
        'status' => $status,
        'headers' => substr($raw, 0, $headerSize),
        'body' => substr($raw, $headerSize),
    ];
}

// render_js=false keeps this call at 1 credit instead of the 5-credit default.
$response = scrape('https://news.ycombinator.com', ['render_js' => 'false']);

echo 'status: ' . $response['status'] . PHP_EOL;

// HTTP/2 lowercases header names, so match case-insensitively.
preg_match_all('/^spb-[^:]+:.*$/im', $response['headers'], $matches);
echo implode(PHP_EOL, $matches[0]) . PHP_EOL;

echo substr($response['body'], 0, 500) . PHP_EOL;
```

## Run it

```bash
php scrape.php
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.


## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
