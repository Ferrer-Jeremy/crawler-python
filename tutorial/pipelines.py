# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilePipeline
import mysql.connector
from mysql.connector import errorcode



class YifyPipeline(object):

    def process_item(self, item, spider):
        cursor = self.cnx.cursor()

        query_movie = ("SELECT id FROM movie WHERE imdb_id = %s")
        cursor.execute(query_movie, item.get('imdb_id'))

        row = cursor.fetchone()

        if row is None:  # Add the movie if it doesn't exist
            query_add_movie = ("INSERT INTO movie (imdb_id, title, `year`) VALUES(%s, %s, %s)")
            cursor.execute(query_add_movie, item.get('imdb_id'), item.get('title'), item.get('year'))
            id = cursor.lastrowid
        else:
            id = row

        cursor.close()
        return item

    def open_spider(self, spider):
        config = {
            'user': 'user',
            'password': 'user',
            'host': 'mysql',
            'database': 'crawler',
            'raise_on_warnings': True,
        }

        try:
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cnx.close()

    def close_spider(self, spider):
        self.cnx.close()

class YifyFilePipeline(FilePipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):

        return item