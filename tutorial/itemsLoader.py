from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class YifySubtitlesItemLoader(ItemLoader):
    default_output_processor = TakeFirst()