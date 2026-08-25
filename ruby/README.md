# Ruby web scraping with the ScrapingBee API

<p align="center">
  <a href="https://www.scrapingbee.com/">
    <img src="https://github.com/user-attachments/assets/78927667-6375-4266-bd58-e049208a4922" alt="ScrapingBee" />
  </a>
</p>

<p align="center"><a href="../README.md">Back to the main repository</a></p>

`net/http` ships with Ruby, so this example installs nothing.

## Prerequisites

- [Ruby 3.0+](https://www.ruby-lang.org/en/downloads/)
- A ScrapingBee API key from the [dashboard](https://app.scrapingbee.com/account/manage/api_key). New accounts get 1,000 free credits.

## Setup

```bash
export SCRAPINGBEE_API_KEY="YOUR-API-KEY"
# No install step. `net/http` is part of the standard library.
```

## The example

```ruby
# Fetch a page through the ScrapingBee web scraping API.
# Auth is the Authorization: Bearer header. The api_key query parameter is deprecated.

require 'net/http'
require 'uri'

API_URL = 'https://app.scrapingbee.com/api/v1'.freeze
API_KEY = ENV.fetch('SCRAPINGBEE_API_KEY', 'YOUR-API-KEY')

def scrape(target, params = {})
  uri = URI(API_URL)
  uri.query = URI.encode_www_form({ url: target }.merge(params))

  request = Net::HTTP::Get.new(uri)
  request['Authorization'] = "Bearer #{API_KEY}"

  Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
    http.request(request)
  end
end

# render_js=false keeps this call at 1 credit instead of the 5-credit default.
response = scrape('https://news.ycombinator.com', render_js: 'false')

puts "status: #{response.code}"
puts "credits: #{response['Spb-cost']}"
puts "request id: #{response['Spb-request-id']}"
puts response.body[0, 500]
```

## Run it

```bash
ruby scrape.rb
```

A successful run prints the status code, the credits charged in the `Spb-cost` header, the
request id, and the first 500 characters of the page.


## Credits used

This example sends `render_js=false`, which costs 1 credit. Leaving JavaScript rendering on,
the default, costs 5. The [full credit table](../README.md#what-a-request-costs) covers every
configuration, and `mode=auto` charges only for whichever one succeeds.

## Help

[Documentation](https://www.scrapingbee.com/documentation/) - [hello@scrapingbee.com](mailto:hello@scrapingbee.com)
