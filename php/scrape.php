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
