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
