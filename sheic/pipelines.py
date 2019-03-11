# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

from sheic.items import PreEicBasic, PreEicExtraInfo1, PreEicExtraInfo2, PreEicExtraInfo3, PreEicExtraInfo4


class DuplicatesPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect("47.102.146.137", "greenment_writer", "Greenment2019!", "zone")
        self.cursor = self.connect.cursor()
        print("DuplicatesPipeline Mysql connected.")

    def process_item(self, item, spider):
        if isinstance(item, PreEicBasic):
            sql = "select * from pre_approval_info where eia_id = '%s'" % (item["eia_id"])
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if result is not None:
                    raise DropItem("Duplicate item found: %s" % item["eia_id"])
                else:
                    return item
            except Exception as error:
                print("Error during access mysql: ", error)
                raise DropItem("Duplicate item found: %s" % item["eia_id"])
        elif isinstance(item, PreEicExtraInfo1):
            sql = "select * from pre_approval_extra_info_1 where eia_id = '%s'" % (item["eia_id"])
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if result is not None:
                    raise DropItem("Duplicate item found: %s" % item["eia_id"])
                else:
                    return item
            except Exception as error:
                print("Error during access mysql: ", error)
                raise DropItem("Duplicate item found: %s" % item["eia_id"])
        elif isinstance(item, PreEicExtraInfo2):
            sql = "select * from pre_approval_extra_info_2 where eia_id = '%s'" % (item["eia_id"])
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if result is not None:
                    raise DropItem("Duplicate item found: %s" % item["eia_id"])
                else:
                    return item
            except Exception as error:
                print("Error during access mysql: ", error)
                raise DropItem("Duplicate item found: %s" % item["eia_id"])
        elif isinstance(item, PreEicExtraInfo3):
            sql = "select * from pre_approval_extra_info_3 where eia_id = '%s'" % (item["eia_id"])
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if result is not None:
                    raise DropItem("Duplicate item found: %s" % item["eia_id"])
                else:
                    return item
            except Exception as error:
                print("Error during access mysql: ", error)
                raise DropItem("Duplicate item found: %s" % item["eia_id"])

        elif isinstance(item, PreEicExtraInfo4):
            sql = "select * from pre_approval_extra_info_4 where eia_id = '%s'" % (item["eia_id"])
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if result is not None:
                    raise DropItem("Duplicate item found: %s" % item["eia_id"])
                else:
                    return item
            except Exception as error:
                print("Error during access mysql: ", error)
                raise DropItem("Duplicate item found: %s" % item["eia_id"])


class SaveFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, PreEicExtraInfo1):
            file_url = item['file_urls'][0]
            meta = {'eia_id': item['eia_id'], 'type': 'eia'}
            yield Request(url=file_url, meta=meta)
        elif isinstance(item, PreEicExtraInfo3):
            file_url = item['file_urls'][0]
            meta = {'eia_id': item['eia_id'], 'type': 'rfc'}
            yield Request(url=file_url, meta=meta)
        elif isinstance(item, PreEicExtraInfo4):
            env_report_url = item['file_urls'][0]
            meta = {'eia_id': item['eia_id'], 'type': 'envReport'}
            yield Request(url=env_report_url, meta=meta)
            public_stmt_url = item['file_urls'][1]
            meta = {'eia_id': item['eia_id'], 'type': 'pblcStmt'}
            yield Request(url=public_stmt_url, meta=meta)

    def file_path(self, request, response=None, info=None):
        return '%s/%s' % (request.meta.get('type'), request.meta.get('eia_id') + '.pdf')

    def item_completed(self, results, item, info):
        if isinstance(item, PreEicExtraInfo1):
            file_paths = [x['path'] for ok, x in results if ok]
            if not file_paths:
                raise DropItem("Item contains no files")
            item['file_path'] = file_paths[0]
        elif isinstance(item, PreEicExtraInfo3):
            file_paths = [x['path'] for ok, x in results if ok]
            if not file_paths:
                raise DropItem("Item contains no files")
            item['rfc_path'] = file_paths[0]
        elif isinstance(item, PreEicExtraInfo4):
            file_paths = [x['path'] for ok, x in results if ok]
            if not file_paths:
                raise DropItem("Item contains no files")
            item['env_report_path'] = file_paths[0]
            item['pblc_stmt_path'] = file_paths[1]
        return item


class SaveMetaDataPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect("47.102.146.137", "greenment_writer", "Greenment2019!", "zone")
        self.cursor = self.connect.cursor()
        print("SaveDataPipeline Mysql connected.")

    def process_item(self, item, spider):
        if isinstance(item, PreEicBasic):
            sql = "insert into " \
                  "pre_approval_info(eia_id, proj_name, location, type, " \
                  "proj_detail, build_unit_name, build_unit_addr, " \
                  "build_unit_contact, build_unit_tel, eic_org_name, " \
                  "eic_org_cred_code, eic_org_addr, eic_org_contact, " \
                  "eic_org_tel, email) VALUES " \
                  "('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                  (item['eia_id'], item["proj_name"], item["location"], item["type"],
                   item["proj_detail"], item["build_unit_name"], item["build_unit_addr"],
                   item["build_unit_contact"], item['build_unit_tel'], item['eic_org_name'],
                   item['eic_org_cred_code'], item['eic_org_addr'], item['eic_org_contact'],
                   item['eic_org_tel'], item['email'])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                print("Persisted basic info of %s" % item["eia_id"])
            except Exception as error:
                self.connect.rollback()
                print("Error during access mysql: ", error)

            return item
        elif isinstance(item, PreEicExtraInfo1):
            sql = "insert into " \
                  "pre_approval_extra_info_1(eia_id, file_path, date_from, date_to)" \
                  "VALUES" \
                  "('%s', '%s', '%s', '%s')" % \
                  (item['eia_id'], item['file_path'], item['publish_date_from'], item['publish_date_to'])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                print("Persisted extra info 1 of %s" % item["eia_id"])
            except Exception as error:
                self.connect.rollback()
                print("Error during access mysql: ", error)

        elif isinstance(item, PreEicExtraInfo2):
            sql = "insert into " \
                  "pre_approval_extra_info_2(eia_id, publish_date, opinion_method)" \
                  "VALUES" \
                  "('%s', '%s','%s')" % \
                  (item['eia_id'], item['publish_date'], item['opinion_method'])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                print("Persisted extra info 2 of %s" % item["eia_id"])
            except Exception as error:
                self.connect.rollback()
                print("Error during access mysql: ", error)

        elif isinstance(item, PreEicExtraInfo3):
            sql = "insert into " \
                  "pre_approval_extra_info_3(eia_id, rfc_path, rfc_scpoe, opinion_method, " \
                  "valid_duration, eia_date)" \
                  "VALUES" \
                  "('%s','%s','%s','%s','%s','%s')" % \
                  (item['eia_id'], item['rfc_path'], item['rfc_scope'], item['opinion_method'],
                   item['valid_duration'], item['eia_date'])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                print("Persisted extra info 3 of %s" % item["eia_id"])
            except Exception as error:
                self.connect.rollback()
                print("Error during access mysql: ", error)

        elif isinstance(item, PreEicExtraInfo4):
            sql = "insert into " \
                  "pre_approval_extra_info_4(eia_id, env_report_path, public_stmt_path, pre_approv_date)" \
                  "VALUES" \
                  "('%s','%s','%s','%s')" % \
                  (item['eia_id'], item['env_report_path'], item['pblc_stmt_path'], item['pre_approv_date'])
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                print("Persisted extra info 4 of %s" % item["eia_id"])
            except Exception as error:
                self.connect.rollback()
                print("Error during access mysql: ", error)