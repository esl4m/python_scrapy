# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import pickle
from scrapy.item import Item, Field


class ArgyleItem(scrapy.Item):
    job_title = 'Not Available'
    job_description = 'Not Available'
    hourly_pay = 'Not Available'
    proposals = 'Not Available'
    country = 'Not Available'

    def serialize(self):
        """
        serialize object and store in pickle file
        """
        with open("./pickles/" + 'upwork_home' + '.pickle', 'wb') as f:
            pickle.dump(self, f)
