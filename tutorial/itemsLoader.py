from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import Identity


class SubtitlesItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    file_urls_out = Identity()