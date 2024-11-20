import scrapy
import csv
from datetime import datetime

import scrapy
import csv

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Follow pagination link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)



class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]

    # Accept the URL from the command line
    def __init__(self, url=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else ['https://www.amazon.com/s?k=smartphones']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'DOWNLOAD_DELAY': 3
    }

    def parse(self, response):
        products = response.css('div.s-main-slot div.s-result-item')

        for product in products:
            name = product.css('span.a-text-normal::text').get()
            price = product.css('span.a-price-whole::text').get()
            price_fraction = product.css('span.a-price-fraction::text').get()
            rating = product.css('span.a-icon-alt::text').get()

            if name and price:
                yield {
                    'name': name.strip(),
                    'price': f'{price}.{price_fraction}',
                    'rating': rating
                }

        # Handle pagination
        next_page = response.css('ul.a-pagination li.a-last a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

################################NETWORKING DATA EXTRACTION FROM HERE R#############

class NetworkingSpider1(scrapy.Spider):
    name = "networking_spider"
    start_urls = ['http://quotes.toscrape.com']

    custom_settings = {
        'FEEDS': {
            'C:\\scrapy_lib\\data\\scrapy_data.csv': {
                'format': 'csv',
                'fields': ['URL', 'Status Code', 'Response Time (s)', 'Depth'],
            },
        }
    }

    def __init__(self):
        # Create/overwrite CSV file and write headers
        with open('C:\\scrapy_lib\\data\\scrapy_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Status Code', 'Response Time (s)', 'Depth'])

    def parse(self, response):
        # Networking data
        url = response.url
        status_code = response.status
        response_time = response.meta.get('download_latency', 'N/A')  # Time taken to get the response
        depth = response.meta.get('depth', 0)  # Depth of the request

        # Write networking data (without any scraped content) to the CSV
        with open('C:\\scrapy_lib\\data\\scrapy_data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([url, status_code, response_time, depth])

        # Follow pagination links or further URLs if needed
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

##############################################################
##complete data spider begins here olahuuber
###############################################################


class NetworkingSpider2(scrapy.Spider):
    name = "complete_net"
    start_urls = ['http://quotes.toscrape.com']

    custom_settings = {
        'FEEDS': {
            'C://EchoSift//data//net_data.csv': {
                'format': 'csv',
                'fields': ['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'],
            },
        }
    }

    def __init__(self):
        # Create/overwrite CSV file and write headers
        with open('C://EchoSift//data//net_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'])

    def parse(self, response):
        # Networking data
        url = response.url
        status_code = response.status
        response_time = response.meta.get('download_latency', 'N/A')  # Time taken to get the response
        depth = response.meta.get('depth', 0)  # Depth of the request
        ip_address = response.ip_address  # IP address of the server
        request_headers = response.request.headers.to_unicode_dict()  # Request headers
        response_headers = response.headers.to_unicode_dict()  # Response headers
        content_length = len(response.body)  # Content length of the response
        user_agent = response.request.headers.get('User-Agent', 'N/A').decode('utf-8')  # User-Agent
        redirected_urls = response.meta.get('redirect_urls', [])  # Any redirected URLs
        encoding = response.encoding if response.encoding else 'N/A'  # Response encoding
        cookies = response.headers.getlist('Set-Cookie')  # Cookies set by the server

        # Extract the actual data here (modify this part as per your scraping logic)
        #data_extracted = response.xpath('//span[@class="text"]/text()').getall()

        # Write networking data and extracted content to the CSV
        with open('C://EchoSift//data//net_data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([url, status_code, response_time, depth, ip_address, request_headers, response_headers, content_length, user_agent, ', '.join(redirected_urls), encoding, cookies])

        # Follow pagination links or further URLs if needed
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

import scrapy
import csv
######################################################################################################
#####ha code below will append the new data on the csv file net data 
###################################################################################################
class NetworkingSpider3(scrapy.Spider):
    name = "complete"
    
    # Default starting URL
    default_url = 'https://www.dmce.ac.in/'  # You can keep this as a default URL if you want

    custom_settings = {
        'FEEDS': {
            'C://EchoSift//data//net_data.csv': {
                'format': 'csv',
                'fields': ['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'],
            },
        }
    }

    def __init__(self, url=None, *args, **kwargs):
        """
        Initialize the spider with a starting URL.
        
        :param url: The URL to scrape, passed as a parameter.
        """
        super().__init__(*args, **kwargs)
        
        # Set the start URL based on the provided URL or use the default
        self.start_urls = [url] if url else [self.default_url]

        # Check if the CSV file exists, if not, create it and write headers
        try:
            with open('C://EchoSift//data//net_data.csv', mode='r', encoding='utf-8') as file:
                pass  # File exists, do nothing
        except FileNotFoundError:
            # If file does not exist, create it and write headers
            with open('C://EchoSift//data//net_data.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'])

    def parse(self, response):
        # Networking data
        url = response.url
        status_code = response.status
        response_time = response.meta.get('download_latency', 'N/A')  # Time taken to get the response
        depth = response.meta.get('depth', 0)  # Depth of the request
        ip_address = response.ip_address  # IP address of the server
        request_headers = response.request.headers.to_unicode_dict()  # Request headers
        response_headers = response.headers.to_unicode_dict()  # Response headers
        content_length = len(response.body)  # Content length of the response
        user_agent = response.request.headers.get('User-Agent', 'N/A').decode('utf-8')  # User-Agent
        redirected_urls = response.meta.get('redirect_urls', [])  # Any redirected URLs
        encoding = response.encoding if response.encoding else 'N/A'  # Response encoding
        cookies = response.headers.getlist('Set-Cookie')  # Cookies set by the server

        # Write networking data and extracted content to the CSV (appending new rows)
        with open('C://EchoSift//data//net_data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([url, status_code, response_time, depth, ip_address, request_headers, response_headers, content_length, user_agent, ', '.join(redirected_urls), encoding, cookies])

        # Follow pagination links or further URLs if needed
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
