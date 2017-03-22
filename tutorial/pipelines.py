# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilesPipeline
import mysql.connector
from mysql.connector import errorcode


class YifyPipeline(object):

    def process_item(self, item, spider):
        try:
            id_movie = self.save_movie_if_it_isnt(item)
            self.save_subtitle(item, id_movie)
        except mysql.connector.Error as err:
            print(err)

        return item

    def save_movie_if_it_isnt(self, item):
        self.cursor.execute(self.query_movie, (item.get('imdb_id'),))
        row = self.cursor.fetchone()

        if row is None:

            return self.save_movie(item)
        else:
            id = row[0]  # Take the id pos 0

            return id

    def save_movie(self, item):
        self.cursor.execute(self.query_add_movie, (item.get('imdb_id'), item.get('title'), item.get('year')))

        return self.cursor.lastrowid

    def save_subtitle(self, item, id_movie):
        self.cursor.execute(self.query_add_subtitle, (id_movie, item.get('name'), item.get('language'), item.get('file_urls')))

    def open_spider(self, spider):
        print('Start Spider')
        self.query_movie = ("SELECT id FROM movie WHERE imdb_id = %s")
        self.query_add_movie = ("INSERT INTO movie (`imdb_id`, `title`, `year`) VALUES(%s, %s, %s)")
        self.query_add_subtitle = ("INSERT INTO subtitle (`id_movie`, `name`, `language`, `path`) VALUES(%s, %s, %s, %s)")

        config = {
            'user': 'user',
            'password': 'user',
            'host': 'mysql',
            'database': 'crawler',
            'raise_on_warnings': True,
        }

        try:
            self.cnx = mysql.connector.connect(**config)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        if self.cnx.is_connected():
            print('Connected to MySQL database')

    def close_spider(self, spider):
        try:
            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
        except mysql.connector.Error as err:
            print(err)

        print('Deconnected of MySQL database')
        print('Close Spider')


class YifyFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item.get('file_urls'):
            yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):
        return item
