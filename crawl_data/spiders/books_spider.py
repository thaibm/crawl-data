import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'books'

    # start_urls = ['http://www.taisachhay.com/danh-nhan/']

    def start_requests(self):
        urls = [
            'http://www.taisachhay.com/danh-nhan/',
            'http://www.taisachhay.com/kiem-hiep',
            'http://www.taisachhay.com/ky-nang-song',
            'http://www.taisachhay.com/sach-chinh-tri',
            'http://www.taisachhay.com/sach-khoa-hoc',
            'http://www.taisachhay.com/kinh-te',
            'http://www.taisachhay.com/lam-giau',
            'http://www.taisachhay.com/lich-su',
            'http://www.taisachhay.com/sach-nuoi-day-con',
            'http://www.taisachhay.com/sach-phong-thuy',
            'http://www.taisachhay.com/sach-tam-ly',
            'http://www.taisachhay.com/sach-thieu-nhi',
            'http://www.taisachhay.com/sach-tieng-anh',
            'http://www.taisachhay.com/van-hoc',
            'http://www.taisachhay.com/sach-y-hoc',
            'http://www.taisachhay.com/tai-chinh-ngan-hang',
            'http://www.taisachhay.com/tieu-thuyet',
            'http://www.taisachhay.com/trinh-tham-kinh-di',
            'http://www.taisachhay.com/truyen-dai',
            'http://www.taisachhay.com/tuoi-hoc-tro',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to author pages
        for href in response.css('a.featured_image_link::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_book)

        # follow pagination links
        next_page = response.css('div.prev_next span.previous_posts a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_book(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h1.books_title div::text'),
            'url' : extract_with_css('h1.books_title a::attr(href)'),
            'author': extract_with_css('h1.books_title + div a::text'),
            'category': extract_with_css('div.book_info div:nth-child(2) a::text'),
            'description': response.css('div.single_post > p *::text').extract()
}