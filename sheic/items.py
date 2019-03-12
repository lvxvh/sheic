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


# 环评事中事后信息

class ProjBasicInfo(scrapy.Item):
    id = scrapy.Field()
    proj_name = scrapy.Field()  # 项目名称
    build_unit = scrapy.Field()  # 建设单位
    type = scrapy.Field()  # 所属行业
    location = scrapy.Field()  # 建设地点
    proj_detail = scrapy.Field()  # 项目基本信息
    design_unit = scrapy.Field()  # 设计单位
    plan_start_date = scrapy.Field()  # 计划开工日期
    eia_reg_number = scrapy.Field()  # 环评项目登记号
    eia_approv_number = scrapy.Field()  # 环评批文文号
    eia_approv_date = scrapy.Field()  # 环评批文日期
    contact = scrapy.Field()  # 联系人
    tel = scrapy.Field()  # 联系电话
    email = scrapy.Field()  # 电子邮箱


class BuildPeriodInfo(scrapy.Item):
    id = scrapy.Field()
    actual_start_date = scrapy.Field()  # 实际开工日期
    env_measures_paths = scrapy.Field()  # 施工期环保措施落实情况pdf
    env_measures_urls = scrapy.Field()
    env_monitor_result_paths = scrapy.Field()  # 施工期环境监测结果
    env_monitor_result_urls = scrapy.Field()
    files = scrapy.Field()


class AdjustPeriodInfo(scrapy.Item):
    id = scrapy.Field()
    finish_date = scrapy.Field()  # 竣工日期
    adjust_start_date = scrapy.Field()  # 开始调试日期
    adjust_report_paths = scrapy.Field()  # 非重大调整报告
    adjust_report_urls = scrapy.Field()
    env_measures_paths = scrapy.Field()  # 环保措施落实情况
    env_measures_urls = scrapy.Field()
    files = scrapy.Field()


class FinalCheckInfo(scrapy.Item):
    id = scrapy.Field()
    publish_date = scrapy.Field()  # 公示起始日期
    check_report_paths = scrapy.Field()  # 验收报告
    check_report_urls = scrapy.Field()
    files = scrapy.Field()