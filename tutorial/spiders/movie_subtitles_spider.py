import scrapy
from tutorial.items import SubtitlesItem
from tutorial.itemsLoader import SubtitlesItemLoader

import scrapy.utils.reqser


class MovieSubtitlesSpider(scrapy.Spider):
    name = 'movie_subtitles'
    start_urls = ['http://www.moviesubtitles.org/movies-A.html']
    optional_keys = ['imdb_id', 'year']

    def parse(self, response):
        self.log_response_for_debug(response)
        for movie_link in response.xpath('//*[@id="content"]/div[3]/div/div[2]/a'):  # For each film
            urljoin = response.urljoin(movie_link.xpath('@href').extract_first())  # Extract the link
            yield scrapy.Request(urljoin, callback=self.parse_movie)  # Follow the link

        for movie_list_link in response.xpath('//*[@id="content"]/div[3]/div/a'):  # For each page that list movies
            urljoin = response.urljoin(movie_list_link.xpath('@href').extract_first())  # Extract the link
            yield scrapy.Request(urljoin, callback=self.parse)

    def parse_movie(self, response):
        self.log_response_for_debug(response)

        raw_title = response.xpath('//*[@id="content"]/div[3]/div/h2/text()')  # the title contains the original name + the english name if any + the year

        for subtitle_link in response.xpath('/html/body/div/div/div[@class="left_articles"]/table/tr'):
            if subtitle_link.xpath('td/a/@href') is None:  # if there no link -> it's not a subtitle so we skip
                continue

            urljoin = response.urljoin(subtitle_link.xpath('td/a/@href').extract_first())  # Extract link to download
            yield scrapy.Request(urljoin, callback=self.parse_subtitle, meta={'raw_title': raw_title})  # Follow the link

    def parse_subtitle(self, response):
        self.log_response_for_debug(response)
        item = {
            'imdb_id': None,  # to send at OMDBPipeline to get the id
            'title': response.meta.get('raw_title'),  # come from parse_movie // to clean up before insert in db
            'year': None,
            'language': response.xpath('//*[@id="content"]/div[3]/div/p[1]/font/b/text()').extract_first().strip(),
            'name': response.xpath('/html/body/div/div/div/div/div[@style="margin-bottom:15px;"]/text()').extract_first().strip(),
            'file_urls': response.xpath('/html/body/div/div/div/div/div/a/@href').extract_first()
        }

        self.log_dict_item(item, response)

        subtitle = SubtitlesItemLoader(item=SubtitlesItem(), response=response)
        subtitle.add_value('imdb_id', item['imdb_id'])
        subtitle.add_value('title', item['title'])
        subtitle.add_value('year', item['year'])
        subtitle.add_value('language', item['language'])
        subtitle.add_value('name', item['name'])
        subtitle.add_value('file_urls', item['file_urls'])
        yield subtitle.load_item()

    def log_dict_item(self, item, response):
        for element in item.items():
            if element[1] is None or not element[1]:
                if element[0] in self.optional_keys:
                    self.logger.info('Key : {} -- Value : {} -- Url : {}'.format(*element, response.url))
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
