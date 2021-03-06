# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
import MySQLdb.cursors


class OriginIdPipeline(object):
    def process_item(self, item, spider):
        if len(item['origin_id']) > 0:

            return item
        else:
            raise DropItem(item)


class ErrorPipeLine(object):
    def process_item(self, item, spider):
        if 'http://err.taobao.com/' in item['link']:
            DropItem(item)
        return item
        # spider.log(item)


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['origin_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['origin_id'])
            return item


class SQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='core',
                                            host='10.0.2.90',
                                            user='guoku',
                                            passwd='guoku!@#',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_update, item,
                                           spider)
        query.addErrback(self.handle_error, spider)
        return item

    def _conditional_update(self, tx, item, spider):
        try:
            if item['status'] == 0:
                sqls = ["UPDATE core_buy_link SET status = '%s' where"
                        " origin_id = '%s'"
                        % (item['status'], item['origin_id'])]
            elif item['price'] == 0:
                sqls = ["UPDATE core_buy_link SET status = '%s',"
                        " shop_link = '%s', seller='%s' where origin_id = '%s'"
                        % (item['status'], item['shop_link'], item['seller'],
                           item['origin_id'])]
            else:
                sqls = ["UPDATE core_buy_link SET status = '%s',"
                        " shop_link = '%s', seller='%s', price='%s'"
                        " where origin_id = '%s'"
                        % (item['status'], item['shop_link'], item['seller'],
                           item['price'], item['origin_id'])]

            if item['update_selection_status']:
                sqls.append("UPDATE core_selection_entity SET is_published=0"
                            " where entity_id in (SELECT entity_id FROM "
                            "core.core_buy_link where origin_id = '%s');"
                            % item['origin_id'])

                sqls.append("UPDATE core_entity SET status='-1'"
                            " where id in (SELECT entity_id FROM "
                            "core.core_buy_link where origin_id = '%s');"
                            % item['origin_id'])

            for sql in sqls:
                tx.execute(
                    sql
                )
            spider.log(sqls)

        except KeyError, e:
            spider.log(e)
        except BaseException, e:
            spider.log(e)

    def handle_error(self, e, spider):
        spider.log(e)

        # class JsonWriterPipeline(object):
        #
        # def __init__(self):
        # self.file = open('items.jl', 'ab')
        #
        # def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line)
        #         return item
