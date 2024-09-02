import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = [
        'https://www.brotherhoodbooks.org.au/categories',
    ]

    def parse(self, response):
        # Extract all product links on the page
        product_links = response.css('li.item.product a.product-item-link::attr(href)').getall()

        # Loop through the product links and follow each one
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)
        
        # Go to the next page if available
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract ISBN
        isbn = response.xpath('//table[@id="product-attribute-specs-table"]//tr[th[text()="ISBN"]]/td/text()').get()
        
        # Extract price
        price = response.css('span.price-wrapper span.price::text').get()

         # Extract Condition
        condition = response.xpath('//div[@data-th="Condition"]/strong/text()').get()

        # Extract Cover
        cover = response.xpath('//div[@data-th="Cover"]/strong/text()').get()

        # Extract Year
        year = response.xpath('//div[@data-th="Year"]/strong/text()').get()

        # Yield the extracted data
        yield {
            'ISBN': isbn,
            'Price': price,
            'Condition': condition,
            'Cover': cover,
            'Year': year,
        }



