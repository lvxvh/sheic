# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PreEicBasic(scrapy.Item):
    eia_id = scrapy.Field()  # id
    proj_name = scrapy.Field()  # 项目名称
    location = scrapy.Field()  # 建设地点
    type = scrapy.Field()  # 所属行业
    proj_detail = scrapy.Field()  # 项目内容
    build_unit_name = scrapy.Field()  # 建设单位名称
    build_unit_addr = scrapy.Field()  # 建设单位地址
    build_unit_contact = scrapy.Field()  # 建设单位联系人
    build_unit_tel = scrapy.Field()  # 建设单位联系电话
    eic_org_name = scrapy.Field()  # 环评机构名称
    eic_org_cred_code = scrapy.Field()  # 环评机构证书编码
    eic_org_addr = scrapy.Field()  # 环评机构地址
    eic_org_contact = scrapy.Field()  # 环评机构联系人
    eic_org_tel = scrapy.Field()  # 环评机构电话
    email = scrapy.Field()  # 电子邮件


# 环评文件
class PreEicExtraInfo1(scrapy.Item):
    eia_id = scrapy.Field()  # id
    publish_date_from = scrapy.Field()
    publish_date_to = scrapy.Field()
    file_urls = scrapy.Field()
    file_path = scrapy.Field()
    files = scrapy.Field()


# 首次公开信息
class PreEicExtraInfo2(scrapy.Item):
    eia_id = scrapy.Field()  # id
    publish_date = scrapy.Field()
    opinion_method = scrapy.Field()


# 环评公示信息
class PreEicExtraInfo3(scrapy.Item):
    eia_id = scrapy.Field()  # id
    eia_date = scrapy.Field()
    rfc_path = scrapy.Field()
    rfc_scope = scrapy.Field()
    opinion_method = scrapy.Field()
    valid_duration = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


# 报批前公开信息
class PreEicExtraInfo4(scrapy.Item):
    eia_id = scrapy.Field()  # id
    pre_approv_date = scrapy.Field()
    env_report_path = scrapy.Field()
    pblc_stmt_path = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
