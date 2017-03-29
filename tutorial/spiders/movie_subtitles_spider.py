import scrapy
from tutorial.items import YifySubtitlesItem
from tutorial.itemsLoader import YifySubtitlesItemLoader


class MovieSubtitlesSpider(scrapy.Spider):
    name = 'movie_subtitles'
    start_urls = ['http://www.moviesubtitles.org/movies-A.html']

    def parse(self, response):
        for movie_link in response.xpath('//*[@id="content"]/div[3]/div/div[2]/a'): # For each film
            urljoin = response.urljoin(movie_link.xpath('@href').extract_first()) # Extract the link
            yield scrapy.Request(urljoin, callback=self.parse_movie) # Follow the link

        for movie_list in response.xpath('//*[@id="content"]/div[3]/div/a'):  # For each page that list movies
            urljoin = response.urljoin(movie_list.xpath('@href').extract_first()) # Extract the link
            yield scrapy.Request(urljoin, callback=self.parse)

    def parse_movie(self, response):
        for subtitle_link in response.xpath('/html/body/div/div/div[@class="left_articles"]/table/tr'):
            if subtitle_link.xpath('td/a/@href') is None:  # if there no link -> it's not a subtitle so we skip
                continue

            urljoin = response.urljoin(subtitle_link.xpath('td/a/@href').extract_first()) # Extract link to download
            yield scrapy.Request(urljoin, callback=self.parse_subtitle)  # Follow the link

    def parse_subtitle(self, response):

        imdb_id = response.xpath('/html/body/div/div/div/a/@href').extract_first().split('/')[-1]  # Get only the id imdb and not the link
        title = response.xpath('//h2/text()').extract_first().strip()
        year = response.xpath('/html/body/div/div/div/div[@class="movie-year"]/text()').extract_first().strip()
        language = response.xpath('/html/body/div/div/div/div/div/ul/li[1]/span[1]/text()').extract_first().strip()
        name = response.xpath('/html/body/div/div/div/div/div[@style="margin-bottom:15px;"]/text()').extract_first().strip()
        file_urls = response.xpath('/html/body/div/div/div/div/div/a/@href').extract_first()

        yifySubtitle = YifySubtitlesItemLoader(item=YifySubtitlesItem(), response=response)
        yifySubtitle.add_value('imdb_id', imdb_id)
        yifySubtitle.add_value('title', title)
        yifySubtitle.add_value('year', year)
        yifySubtitle.add_value('language', language)
        yifySubtitle.add_value('name', name)
        yifySubtitle.add_value('file_urls', file_urls)
        yield yifySubtitle.load_item()
