import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'vnexpress'

    # start_urls = ['http://www.taisachhay.com/danh-nhan/']

    def start_requests(self):
        urls = [
            'http://vnexpress.net/tin-tuc/tam-su'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.title_news a.txt_link::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_data)

        # for href in response.css('#news_home a.txt_link::attr(href)').extract():
        #     yield scrapy.Request(response.urljoin(href),
        #                          callback=self.parse_data)
        # follow pagination links
        # next_page = response.css('div#pagination a.pa_next::attr(href)').extract_first()
        next_page = response.css('div.pagination_news a:last-child::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_data(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        yield {
            'title': extract_with_css('div.title_news h1::text'),
            'intro': extract_with_css('h3.short_intro::text'),
            'content': response.css('div.fck_detail > p *::text').extract()
            # 'comment': response.css('div.comment_item p.full_content::text').extract()
}