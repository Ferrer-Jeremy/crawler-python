# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilesPipeline
import mysql.connector
from mysql.connector import errorcode


class YifyPipeline(object):

    def process_item(self, item, spider):
        query_movie = ("SELECT id FROM movie WHERE imdb_id = %s")
        query_add_movie = ("INSERT INTO movie (`imdb_id`, `title`, `year`) VALUES(%s, %s, %s)")
        query_add_subtitle = ("INSERT INTO subtitle (`movie_id`, `name`, `language`) VALUES(%s, %s, %s)")

        cursor = cnx.cursor()

        save_movie_if_it_isnt(item, cursor)

        return item

    def save_movie_if_it_isnt(self, item, cursor):
        try:
            cursor.execute(query_movie, (item.get('imdb_id'),))
        except mysql.connector.Error as err:
            print(err)

        row = cursor.fetchone()
        if row is None:
            save_movie(item, cursor)
        else:
            pass

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

        if cnx.is_connected():
            print('Connected to MySQL database')

    def close_spider(self, spider):
        self.cnx.close()


class YifyFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item.get('file_urls'):
            yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):
        return item
