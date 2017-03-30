import scrapy
from tutorial.items import YifySubtitlesItem
from tutorial.itemsLoader import YifySubtitlesItemLoader


class YifySpider(scrapy.Spider):
    name = 'yify'
    start_urls = ['http://www.yifysubtitles.com/browse/page-153']
    optional_keys = ['name']

    def parse(self, response):
        self.log_response_for_debug(response)
        for movie_link in response.xpath('/html/body/div/div/div[1]/ul/li'):  # For each film
            urljoin = response.urljoin(movie_link.xpath('div[1]/a/@href').extract_first())  # Extract the link
            yield scrapy.Request(urljoin, callback=self.parse_movie)  # Follow the link

        # next_page = response.xpath('/html/body/div/div/div/div/ul/li[last()]/a/@href').extract_first()  # Extract the button next
        # if next_page is not None:
        #     urljoin = response.urljoin(next_page)
        #     yield scrapy.Request(urljoin, callback=self.parse)

    def parse_movie(self, response):
        self.log_response_for_debug(response)
        for subtitle_link in response.xpath('/html/body/div/div/div/table/tbody/tr'):
            urljoin = response.urljoin(subtitle_link.xpath('td[last()]/a/@href').extract_first())  # Extract link to download
            yield scrapy.Request(urljoin, callback=self.parse_subtitle)  # Follow the link

    def parse_subtitle(self, response):
        self.log_response_for_debug(response)
        item = {
            'imdb_id': response.xpath('/html/body/div/div/div/a/@href').extract_first().split('/')[-1],  # Get only the id imdb and not the link
            'title': response.xpath('//h2/text()').extract_first().strip(),
            'year': response.xpath('/html/body/div/div/div/div[@class="movie-year"]/text()').extract_first().strip(),
            'language': response.xpath('/html/body/div/div/div/div/div/ul/li[1]/span[1]/text()').extract_first().strip(),
            'name': response.xpath('/html/body/div/div/div/div/div[@style="margin-bottom:15px;"]/text()').extract_first().strip(),
            'file_urls': response.xpath('/html/body/div/div/div/div/div/a/@href').extract_first()
        }

        self.log_dict_item(item, response)

        yify_subtitle = YifySubtitlesItemLoader(item=YifySubtitlesItem(), response=response)
        yify_subtitle.add_value('imdb_id', item['imdb_id'])
        yify_subtitle.add_value('title', item['title'])
        yify_subtitle.add_value('year', item['year'])
        yify_subtitle.add_value('language', item['language'])
        yify_subtitle.add_value('name', item['name'])
        yify_subtitle.add_value('file_urls', item['file_urls'])
        yield yify_subtitle.load_item()

    def log_dict_item(self, item, response):
        for element in item.items():
            if element[1] is None or not element[1]:
                if element[0] in self.optional_keys:
                    self.logger.warning('Key : {} -- Value : {} -- Url : {}'.format(*element, response.url))
                else:
                    self.logger.error('Key : {} -- Value : {} -- Url : {}'.format(*element, response.url))

    def log_response_for_debug(self, response):
        meta = {
            'url': response.url,
            'status': response.status,
            'header': response.headers
        }

        for element in meta.items():
            self.logger.debug('Key : {} -- Value : {}'.format(*element))
