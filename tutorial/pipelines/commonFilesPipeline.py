import os.path
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request


class SpecialFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        self.item = item

        return [Request(x) for x in item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        media_guid = self.item.get('id_subtitle')  # TODO: the name of the file should be equal to the name of the subtitle + id of the subtitle -> slugify
        media_ext = os.path.splitext(request.url)[1]
        file_name = '%s%s' % (media_guid, media_ext)

        return os.path.join(self.item.get('imdb_id'), file_name)

    def item_completed(self, results, item, info):
        # TODO: save the hash of the file in the DB
        # TODO: Check if the file already exist with the hash and if so delete it from file and DB but before add it's name to the alias(subtitle) table or extrat the file and rename it
        return item
