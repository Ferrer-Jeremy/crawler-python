import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import YifySubtitles


class YifySpider(scrapy.Spider):
    name = 'yify'
    start_urls = ['http://www.yifysubtitles.com/browse/page-1']

    def parse(self, response):
        for movie_link in response.xpath('/html/body/div/div/div[1]/ul/li'): # For each film
            urljoin = response.urljoin(movie_link.xpath('div[1]/a/@href').extract_first()) # Extract the link
            yield scrapy.Request(urljoin, callback=self.parse_movie) # Follow the link

        # next_page = response.xpath('/html/body/div/div/div/div/ul/li[last()]/a/@href').extract_first()  # Extract the button next
        # if next_page is not None:
        #     urljoin = response.urljoin(next_page)
        #     yield scrapy.Request(urljoin, callback=self.parse)

    def parse_movie(self, response):
        for subtitle_link in response.xpath('/html/body/div/div/div/table/tbody/tr'):
            urljoin = response.urljoin(subtitle_link.xpath('td[last()]/a/@href').extract_first()) # Extract link to download
            yield scrapy.Request(urljoin, callback=self.parse_subtitle)  # Follow the link

    def parse_subtitle(self, response):

        imdb_id = response.xpath('/html/body/div/div/div/a/@href').extract_first().split('/')[-1]  # Get only the id imdb and not the link
        title = response.xpath('//h2/text()').extract_first()
        year = response.xpath('/html/body/div/div/div/div[@class="movie-year"]/text()').extract_first()
        language = response.xpath('/html/body/div/div/div/div/div/ul/li[1]/span[1]/text()').extract_first().strip()
        name = response.xpath('/html/body/div/div/div/div/div[@style="margin-bottom:15px;"]/text()').extract_first().strip()
        file_urls = response.xpath('/html/body/div/div/div/div/div/a/@href').extract_first()

        yifySubtitle = ItemLoader(item=YifySubtitles(), response=response)
        yifySubtitle.add_value('imdb_id', imdb_id)
        yifySubtitle.add_value('title', title)
        yifySubtitle.add_value('year', year)
        yifySubtitle.add_value('language', language)
        yifySubtitle.add_value('name', name)
        yifySubtitle.add_value('file_urls', file_urls)
        yield yifySubtitle.load_item()
