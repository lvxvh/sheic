# -*- coding: utf-8 -*-
import re

import scrapy
from datetime import datetime
from scrapy import Request
from scrapy.shell import inspect_response

from sheic.items import ProjBasicInfo, BuildPeriodInfo, AdjustPeriodInfo, FinalCheckInfo


class PosteiaSpider(scrapy.Spider):
    name = 'postEia'
    allowed_domains = ['xxgk.eic.sh.cn']
    start_urls = ['http://xxgk.eic.sh.cn/jsp/view/jsxmxxgkInfo_main.jsp']

    custom_settings = {
        'ITEM_PIPELINES': {
            'sheic.pipelines.PostDuplicatesPipeline': 100,
            'sheic.pipelines.PostSaveFilesPipeline': 200,
            'sheic.pipelines.PostSaveMetaDataPipeline': 300,
        }
    }

    def parse(self, response):
        # f = open("./test.html", 'w+')
        # f.write(response.text)
        total_page = re.search(r'共(\d+)页', response.text).group(1)
        all_pages = [response.request.url + "?currentPage=" + str(i + 1) for i in range(int(total_page))]
        for page in all_pages:
            yield Request(url=page,
                          callback=self.parse_page)

    def parse_page(self, response):
        current_page = re.search(r'当前第(\d+)页', response.text).group(1)
        total_page = re.search(r'共(\d+)页', response.text).group(1)
        print("爬取进度" ,current_page, " / ", total_page, flush=True)
        eia_id_list = re.findall(r'(?<=openInfo\(\')(.*)(?=\'\))', response.text)

        for idx, id in enumerate(eia_id_list):
            detail_page = 'http://xxgk.eic.sh.cn' \
                          '/jsp/view/jsxmInfo_edit.jsp?from=&id=' \
                          + str(id) + '&type=' + str(type)
            yield Request(url=detail_page,
                          callback=self.parse_detail,
                          meta={'id': id, 'count': (int(current_page)-1)*20 + idx})

    def parse_detail(self, response):
        # with open("./test.html", 'wb') as f:
        #     f.write(response.body)
        id = response.meta.get('id')
        print("current item: ", response.meta.get('count'), flush=True)
        if re.search(r'环评批文日期.*?\s*?<span>(.*?)<', response.text, re.DOTALL).group(1) != "":
            proj_basic_info = ProjBasicInfo()
            proj_basic_info['id'] = id
            proj_basic_info['proj_name'] = re.search(r'项目名称</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['build_unit'] = re.search(r'建设单位</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['type'] = re.search(r'所属行业</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['location'] = re.search(r'建设地点</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['proj_detail'] = re.search(r'项目基本信息</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['design_unit'] = re.search(r'设计单位</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['plan_start_date'] = datetime.strptime(
                re.search(r'计划开工日期</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1) \
                    .replace('\n', '').strip(),
                '%Y-%m-%d')
            proj_basic_info['eia_reg_number'] = re.search(r'环评项目登记号</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['eia_approv_number'] = re.search(r'环评批文文号</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['eia_approv_date'] = datetime.strptime(
                re.search(r'环评批文日期</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1) \
                    .replace('\n', '').strip(),
                '%Y-%m-%d')
            proj_basic_info['contact'] = re.search(r'联系人</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['tel'] = re.search(r'联系电话</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            proj_basic_info['email'] = re.search(r'电子邮箱</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1)\
                                                .replace('\n', '').strip()
            yield proj_basic_info


        if re.search(r'实际开工日期.*?\s*?<span>(.*?)<', response.text, re.DOTALL).group(1) != "":
            build_period_info = BuildPeriodInfo()
            build_period_info['id'] = id
            build_period_info['actual_start_date'] = datetime.strptime(
                re.search(r'实际开工日期</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1) \
                    .replace('\n', '').strip(),
                '%Y-%m-%d')
            env_measures_urls_table = re.search(r'施工期环保措施落实情况（pdf）</div>.*?</div>', response.text, re.DOTALL).group(0)
            file_ids = re.findall(r'filedown\(\'(.*?)\'\)', env_measures_urls_table, re.DOTALL)
            build_period_info['env_measures_urls'] = ['http://xxgk.eic.sh.cn/xhyf/common/filedown1.do?fileId='+ id for id in file_ids]

            env_monitor_result_urls_table = re.search(r'施工期环境监测结果（pdf）</div>.*?</div>', response.text, re.DOTALL).group(0)
            file_ids = re.findall(r'filedown\(\'(.*?)\'\)', env_monitor_result_urls_table, re.DOTALL)
            build_period_info['env_monitor_result_urls'] = ['http://xxgk.eic.sh.cn/xhyf/common/filedown1.do?fileId='+ id for id in file_ids]

            yield build_period_info

        if re.search(r'开始调试日期.*?\s*?<span>(.*?)<', response.text, re.DOTALL).group(1) != "":
            adjust_period_info = AdjustPeriodInfo()
            adjust_period_info['id'] = id
            adjust_period_info['finish_date'] = datetime.strptime(
                re.search(r'竣工日期</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1) \
                    .replace('\n', '').strip(),
                '%Y-%m-%d')
            adjust_period_info['adjust_start_date'] = datetime.strptime(
                re.search(r'开始调试日期</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1) \
                    .replace('\n', '').strip(),
                '%Y-%m-%d')
            adjust_report_urls_table = re.search(r'非重大调整报告（pdf）</div>.*?</div>', response.text, re.DOTALL).group(0)
            file_ids = re.findall(r'filedown\(\'(.*?)\'\)', adjust_report_urls_table, re.DOTALL)
            adjust_period_info['adjust_report_urls'] = ['http://xxgk.eic.sh.cn/xhyf/common/filedown1.do?fileId=' + id for
                                                      id in file_ids]

            env_measures_urls_table = re.search(r'环保措施落实情况（pdf）</div>.*?</div>', response.text, re.DOTALL).group(
                0)
            file_ids = re.findall(r'filedown\(\'(.*?)\'\)', env_measures_urls_table, re.DOTALL)
            adjust_period_info['env_measures_urls'] = [
                'http://xxgk.eic.sh.cn/xhyf/common/filedown1.do?fileId=' + id for id in file_ids]

            yield adjust_period_info

        if re.search(r'公示起始日期.*?\s*?<span>(.*?)<', response.text, re.DOTALL).group(1) != "":
            final_check_info = FinalCheckInfo()
            final_check_info['id'] = id
            final_check_info['publish_date'] = datetime.strptime(
                re.search(r'公示起始日期</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1) \
                    .replace('\n', '').strip(),
                '%Y-%m-%d')
            check_report_urls_table = re.search(r'验收报告</div>.*?</div>', response.text, re.DOTALL).group(
                0)
            file_ids = re.findall(r'filedown\(\'(.*?)\'\)', check_report_urls_table, re.DOTALL)
            final_check_info['check_report_urls'] = [
                'http://xxgk.eic.sh.cn/xhyf/common/filedown1.do?fileId=' + id for id in file_ids]

            yield final_check_info