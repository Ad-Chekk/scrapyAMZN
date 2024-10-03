import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    # Replace with the URL of the website you want to scrape
    start_urls = ['https://example.com']

    def parse(self, response):
        # Example: Extract all the <h1> elements
        for heading in response.xpath('//h1'):
            yield {
                'heading': heading.xpath('text()').get(),
            }
        
        # Follow links to other pages, if any (Optional)
        for next_page in response.css('a::attr(href)'):
            next_page = response.urljoin(next_page.get())
            yield scrapy.Request(next_page, callback=self.parse)


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
