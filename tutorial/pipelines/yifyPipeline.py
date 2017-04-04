import scrapy

class YifyPipeline(object):

    def process_item(self, item, spider):
        if item.get('name') is None or not item.get('name'):
            item['name'] = item.get('title')
        return item