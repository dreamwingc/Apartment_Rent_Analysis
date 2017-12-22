from twisted.enterprise import adbapi
import MySQLdb.cursors
import mysql.connector
import memcache

class InvertedIndex():
    def __init__(self):
        # self.dbpool = adbapi.ConnectionPool('MySQLdb', db='web_crawler',
        #                                     user='root', passwd='mypassword', cursorclass=MySQLdb.cursors.DictCursor,
        #                                     charset='utf8', use_unicode=True)
        self.mysqlPool = mysql.connector.connect(user='root', password='mypassword', host='127.0.0.1', database='web_crawler')
        self.memcacheClient = memcache.Client(['127.0.0.1:11211'], debug=1)

    def process_data(self, category, query):
        # clear data in memcatch
        # self.memcacheClient.flush_all()

        if category == 'location':
            nQuery = query[1:].replace(' ', '_')
        else:
            nQuery = query

        results = self.memcacheClient.get(nQuery)

        if results:
            for url in results:
                print query + ':'
                print url
        else:
            cursor = self.mysqlPool.cursor(buffered=True)
            if category == 'location':
                # self.dbpool.runInteraction(self._get_location, query)
                cursor.execute("select * from web_crawler where location = '%s'" % query)
            elif category == 'bedroom':
                # self.dbpool.runInteraction(self._get_floor, query)
                cursor.execute("select * from web_crawler where bedrooms = '%s'" % query)

            self.mysqlPool.commit()
            data = cursor.fetchall()

            self.memcacheClient.set(nQuery, data, 3600)

            print "Updated memcached with MySQL data"

            if data:
                for item in data:
                    print item
            else:
                print 'Nothing'

            cursor.close()
            self.mysqlPool.close()

if __name__ == '__main__':
    locations = [' san jose south', ' san jose north', ' san jose west', ' san jose east', ' milpitas', ' santa clara',
                 ' sunnyvale', ' los gatos', ' campbell', ' cupertino', ' mountain view']

    bedrooms = ['1br', '2br', '3br', '4br', '5br']

    for location in locations:
        inverted_index = InvertedIndex()
        inverted_index.process_data('location', location)

    for bedroom in bedrooms:
        inverted_index = InvertedIndex()
        inverted_index.process_data('bedroom', bedroom)