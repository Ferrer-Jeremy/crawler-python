# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilesPipeline
import mysql.connector
from mysql.connector import errorcode

import os
import os.path
from scrapy.http import Request


class YifyPipeline(object):
    query_movie = ("SELECT id FROM movie WHERE imdb_id = %s")
    query_add_movie = ("INSERT INTO movie (`imdb_id`, `title`, `year`) VALUES(%s, %s, %s)")
    query_add_subtitle = ("INSERT INTO subtitle (`id_movie`, `name`, `language`, `path`) VALUES(%s, %s, %s, %s)")

    def process_item(self, item, spider):
        try:
            id_movie = self.save_movie_if_it_isnt(item)
            item['id_subtitle'] = self.save_subtitle(item, id_movie)
        except mysql.connector.Error as err:
            print(err)

        return item

    def save_movie_if_it_isnt(self, item):
        self.cursor.execute(self.query_movie, (item.get('imdb_id'),))
        row = self.cursor.fetchone()

        if row is None:

            return self.save_movie(item)
        else:
            id_movie = row[0]  # Take the id pos 0

            return id_movie

    def save_movie(self, item):
        self.cursor.execute(self.query_add_movie, (item.get('imdb_id'), item.get('title'), item.get('year')))

        # Make a direcoty for this movie if it doesn't exist
        movie_dir = os.path.join('subtitles', item.get('imdb_id')) # TODO: REPLACE SUBTITLE BY THE VARIABLE IN THE SETTINGS
        # TODO: Log if we create a dir?
        if not os.path.exists(movie_dir):
            os.makedir(movie_dir)

        return self.cursor.lastrowid

    def save_subtitle(self, item, id_movie):
        file_url = item.get('file_urls')[0] # there is only one
        self.cursor.execute(self.query_add_subtitle, (id_movie, item.get('name'), item.get('language'), file_url))

        return self.cursor.lastrowid

    def open_spider(self, spider):
        print('Start Spider')

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
        self.item = item

        return [Request(x) for x in item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        media_guid = self.item.get('id_subtitle') # TODO: the name of the file should be equal to the name of the subtitle + id of the subtitle -> slugify
        media_ext = os.path.splitext(request.url)[1]
        file_name = '%s%s' % (media_guid, media_ext)

        return os.path.join(self.item.get('imdb_id'), file_name)

    def item_completed(self, results, item, info):
        # TODO: save the hash of the file in the DB
        # TODO: Check if the file already exist with the hash and if so delete it from file and DB but before add it's name to the alias(subtitle) table
        return item
