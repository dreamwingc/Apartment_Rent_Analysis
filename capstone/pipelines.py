# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb.cursors


class CapstonePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='web_crawler',
                                            user='root', passwd='mypassword', cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        itemDict = {'price': 'varchar(45)',
                    'title': 'varchar(2048)',
                    'floor_plan': 'varchar(45)',
                    'bedrooms': 'varchar(45)',
                    'square_feet': 'varchar(255)',
                    'location': 'varchar(1024)',
                    'related_link': 'varchar(255)'}

        itemName = ()
        itemValue = ()
        for itemKey in itemDict:
            # if itemKey != 'related_link':
            #     tx.execute("alter table web_crawler add column %s %s" % (itemKey, itemDict[itemKey]))
            itemName += (itemKey,)
            itemValue += (item[itemKey],)
        print "---------------------" + str(itemValue) + "--------------------\n"
        print "---------------------" + str(itemName) + "-----------------------"

        tx.execute("insert into web_crawler "
                   "(%s,%s,%s,%s,%s,%s,%s) "
                   "values "
                   "('%s','%s','%s','%s','%s','%s','%s')" % (itemName+itemValue))
