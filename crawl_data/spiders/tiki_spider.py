import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'tiki'

    # start_urls = ['http://www.taisachhay.com/danh-nhan/']

    def start_requests(self):
        urls = [
            'https://tiki.vn/tieu-thuyet-tinh-cam-lang-man/c844?src=tree',

            'https://tiki.vn/sach-van-hoc-viet-nam/c2547?src=tree',
            'https://tiki.vn/truyen-thieu-nhi/c4939?src=tree',
            'https://tiki.vn/phong-su-ky-su/c587?src=tree',
            'https://tiki.vn/tieu-thuyet/c4935?src=tree',
            'https://tiki.vn/truyen-ngan-tan-van/c4938?src=tree',
            'https://tiki.vn/van-hoc-nha-truong/c1528?src=tree',
            'https://tiki.vn/tho/c4934?src=tree',
            'https://tiki.vn/phe-binh-van-hoc/c841?src=tree',
            'https://tiki.vn/truyen-trinh-tham-phieu-luu/c4940?src=tree',
            'https://tiki.vn/truyen-kinh-di/c4942?src=tree',
            'https://tiki.vn/tu-truyen-hoi-ky/c4941?src=tree',

            'https://tiki.vn/tac-pham-kinh-dien/c842?src=tree',
            'https://tiki.vn/truyen-ngan/c845?src=tree',
            'https://tiki.vn/trinh-tham/c664?src=tree',
            'https://tiki.vn/truyen-kinh-di/c665?src=tree',
            'https://tiki.vn/huyen-bi-gia-tuong/c840?src=tree',
            'https://tiki.vn/tieu-su-hoi-ky/c843?src=tree',
            'https://tiki.vn/kiem-hiep-vo-hiep/c639?src=tree',
            'https://tiki.vn/du-ky/c4933?src=tree',
            'https://tiki.vn/phong-su-ky-su/c5245?src=tree',
            'https://tiki.vn/phe-binh-van-hoc/c5244?src=tree',
            'https://tiki.vn/tuy-but-but-ki/c6238?src=tree',
            'https://tiki.vn/truyen-dai/c6750?src=tree',
            'https://tiki.vn/truyen-hai-huoc-truyen-cuoi/c444?src=tree',
            'https://tiki.vn/tho/c446?src=tree',
            'https://tiki.vn/light-novel/c7358?src=tree',
            'https://tiki.vn/truyen-tranh/c8973?src=tree',

            'https://tiki.vn/van-hoc-nuoc-ngoai/c2546?src=tree',
            'https://tiki.vn/tu-truyen-hoi-ky/c4899?src=tree',
            'https://tiki.vn/truyen-ngan/c4895?src=tree',
            'https://tiki.vn/huyen-bi-gia-tuong/c4898?src=tree',
            'https://tiki.vn/phong-su-ky-su/c4892?src=tree',
            'https://tiki.vn/truyen-kinh-di/c4900?src=tree',
            'https://tiki.vn/tieu-thuyet/c4893?src=tree',
            'https://tiki.vn/truyen-thieu-nhi/c4896?src=tree',
            'https://tiki.vn/trinh-tham-phieu-luu/c4897?src=tree',
            'https://tiki.vn/truyen-kiem-hiep-phieu-luu/c4894?src=tree',
            'https://tiki.vn/sach-phe-binh-van-hoc/c4891?src=tree',
            'https://tiki.vn/truyen-co-tich-ngu-ngon/c4890?src=tree',

            'https://tiki.vn/sach-ky-nang-song-dep/c870?src=tree',
            'https://tiki.vn/sach-ba-me-em-be/c2527?src=tree',
            'https://tiki.vn/sach-kinh-te/c846?src=tree',
            'https://tiki.vn/ngoai-ngu-tu-dien/c887?src=tree',
            'https://tiki.vn/truyen-tranh/c1084?src=tree',
            'https://tiki.vn/sach-kien-thuc-tong-hop/c873?src=tree',
            'https://tiki.vn/lich-su-dia-ly/c880?src=tree',
            'https://tiki.vn/khoa-hoc-ky-thuat/c879?src=tree',
            'https://tiki.vn/dien-anh-nhac-hoa/c881?src=tree',
            'https://tiki.vn/ton-giao-tam-linh/c861?src=tree',
            'https://tiki.vn/van-hoa-dia-ly-du-lich/c857?src=tree',
            'https://tiki.vn/chinh-tri-phap-ly/c875?src=tree',
            'https://tiki.vn/nong-lam-ngu-nghiep/c882?src=tree',
            'https://tiki.vn/cong-nghe-thong-tin/c876?src=tree',
            'https://tiki.vn/y-hoc/c885?src=tree',
            'https://tiki.vn/sach-truyen-thieu-nhi/c393?src=tree',
            'https://tiki.vn/sach-thuong-thuc-doi-song/c862?src=tree',
            'https://tiki.vn/tam-ly-gioi-tinh/c868?src=tree'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to author pages
        global category
        category = response.css('ol.breadcrumb li:nth-child(n+3) a::text').extract()
        category = ",".join(category)
        for href in response.css('div.product-box-list div.product-item a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback= self.parse_data)

            # yield {'category': }

        # follow pagination links
        next_page = response.css('div.list-pager a.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_data(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h1#product-name::text'),
            'url': extract_with_css('ol.breadcrumb li:last-child a::attr(href)'),
            'author': extract_with_css('div.item-price div.item-brand p a::text'),
            'description': response.css('div#gioi-thieu > p *::text').extract(),
            'categories': category
        }