import scrapy
import time
from selenium import webdriver
from pyvirtualdisplay import Display


class AuthorSpider(scrapy.Spider):
    name = 'auchan'

    start_urls = ['http://www.auchandrive.fr/drive/Marseille-987/Produits-Frais-R3686962/Cremerie-3686963/']

    def __init__(self):
        scrapy.Spider.__init__(self)
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.browser = webdriver.Firefox(executable_path='docker/application/geckodriver')

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
        yield self.browser.find_elements_by_xpath('html')
