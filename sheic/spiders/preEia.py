# -*- coding: utf-8 -*-
import re

from datetime import datetime
import scrapy
from scrapy import Request

from sheic.items import PreEicBasic, PreEicExtraInfo1, PreEicExtraInfo2, PreEicExtraInfo3, PreEicExtraInfo4


class PreeiaSpider(scrapy.Spider):
    name = 'preEia'
    allowed_domains = ['xxgk.eic.sh.cn']
    start_urls = ['http://xxgk.eic.sh.cn/jsp/view/eiaReportList.jsp']
    custom_settings = {
        'ITEM_PIPELINES': {
            'sheic.pipelines.DuplicatesPipeline': 100,
            'sheic.pipelines.SaveFilesPipeline': 200,
            'sheic.pipelines.SaveMetaDataPipeline': 300,
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

        for id in eia_id_list:
            eia_id, type = id.split("','")[0], id.split("','")[1]
            detail_page = 'http://xxgk.eic.sh.cn' \
                          '/jsxmxxgk/eiareport/action/jsxm_eiaReportDetail.do?from=jsxm&stEiaId=' \
                          + str(eia_id) + '&type=' + str(type)
            yield Request(url=detail_page,
                          callback=self.parse_detail,
                          meta={'eia_id': eia_id})

    def parse_detail(self, response):
        basicItem = PreEicBasic()
        eia_id = response.meta.get('eia_id')
        basicItem['eia_id'] = eia_id
        basicItem['proj_name'] = re.search(r'项目名称</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1).replace(
            '\n', '').strip()
        basicItem['location'] = re.search(r'建设地点</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1).replace('\n',
                                                                                                                   '').strip()
        basicItem['type'] = re.search(r'所属行业</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1).replace('\n',
                                                                                                               '').strip()
        basicItem['proj_detail'] = re.search(r'项目内容</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1).replace(
            '\n', '').strip()
        basicItem['build_unit_name'] = re.search(r'建设单位名称</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(
            1).replace('\n', '').strip()
        basicItem['build_unit_addr'] = re.search(r'建设单位地址</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(
            1).replace('\n', '').strip()
        basicItem['build_unit_contact'] = re.search(r'建设单位联系人</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(
            1).replace('\n', '').strip()
        basicItem['build_unit_tel'] = re.findall(r'联系电话</div>.*?>(.*?)</div>', response.text, re.DOTALL)[0].replace(
            '\n', '').strip()
        basicItem['eic_org_name'] = re.search(r'环评机构名称</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(
            1).replace('\n', '').strip()
        basicItem['eic_org_cred_code'] = re.search(r'环评机构证书编码</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(
            1).replace('\n', '').strip()
        basicItem['eic_org_addr'] = re.search(r'环评机构地址</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(
            1).replace('\n', '').strip()
        basicItem['eic_org_contact'] = re.search(r'环评机构联系人</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(
            1).replace('\n', '').strip()
        basicItem['eic_org_tel'] = re.findall(r'联系电话</div>.*?>(.*?)</div>', response.text, re.DOTALL)[1].replace('\n',
                                                                                                                 '').strip()
        basicItem['email'] = re.search(r'电子邮件</div>.*?>(.*?)</div>', response.text, re.DOTALL).group(1).replace('\n',
                                                                                                                '').strip()
        yield basicItem

        if re.search(r'公示日期', response.text) is not None:
            extraItem = PreEicExtraInfo1()
            extraItem['eia_id'] = eia_id
            date_search = re.search(r'公示日期.*?<span>(\d+-\d+-\d+)-(\d+-\d+-\d+)</span>', response.text, re.DOTALL)
            extraItem['publish_date_from'] = datetime.strptime(date_search.group(1), '%Y-%m-%d')
            extraItem['publish_date_to'] = datetime.strptime(date_search.group(2), '%Y-%m-%d')
            extraItem['file_urls'] = ['http://xxgk.eic.sh.cn' \
                                      '/shhjkxw/eiareport/action/download.do?stEiaId=' + extraItem['eia_id']]
            yield extraItem

        if re.search(r'#first', response.text) is not None:
            extraItem = PreEicExtraInfo2()
            extraItem['eia_id'] = eia_id
            extraItem['publish_date'] = datetime.strptime(
                re.search(r'首次公开信息：.*?>(\d+-\d+-\d+)</td>', response.text, re.DOTALL).group(1), '%Y-%m-%d')
            extraItem['opinion_method'] = re.search(r'公众提出意见的主要方式</div>.*?>(.*?)</div>', response.text,
                                                    re.DOTALL).group(1).replace('\n', '').strip()
            yield extraItem

        if re.search(r'#second', response.text) is not None:
            extraItem = PreEicExtraInfo3()
            extraItem['eia_id'] = eia_id
            extraItem['eia_date'] = datetime.strptime(
                re.search(r'环评公示：.*?>(\d+-\d+-\d+)</td>', response.text, re.DOTALL).group(1), '%Y-%m-%d')
            extraItem['rfc_scope'] = re.search(r'征求公众意见的范围</div>.*?>(.*?)</div>', response.text,
                                               re.DOTALL).group(1).replace('\n', '').strip()
            extraItem['opinion_method'] = re.search(r'征求公众意见的范围.*?公众提出意见的主要方式</div>.*?>(.*?)</div>', response.text,
                                                    re.DOTALL).group(1).replace('\n', '').strip()
            extraItem['valid_duration'] = re.search(r'信息发布有效期限</div>.*?>(.*?)</div>', response.text,
                                                    re.DOTALL).group(1).replace('\n', '').strip()
            file_type = re.search(r'环境影响报告书征求意见稿全文.*?filedownBgs\(\'(.*?)\'\)', response.text, re.DOTALL) \
                .group(1).replace('\n', '').strip()
            extraItem['file_urls'] = ['http://xxgk.eic.sh.cn' \
                                      '/shhjkxw/eiareportBgs/action/download.do?stEiaId='
                                      + eia_id + '&fileType=' + file_type]
            yield extraItem

        if re.search(r'#third', response.text) is not None:
            extraItem = PreEicExtraInfo4()
            extraItem['eia_id'] = eia_id
            extraItem['pre_approv_date'] = datetime.strptime(
                re.search(r'报批前公开信息：.*?>(\d+-\d+-\d+)</td>', response.text, re.DOTALL).group(1), '%Y-%m-%d')
            extraItem['file_urls'] = ['http://xxgk.eic.sh.cn' \
                                      '/shhjkxw/eiareportBgs/action/download.do?stEiaId='
                                      + eia_id + '&fileType=' + 'BL_GSWTS',     #报告书
                                      'http://xxgk.eic.sh.cn' \
                                      '/shhjkxw/eiareportBgs/action/download.do?stEiaId='
                                      + eia_id + '&fileType=' + 'BL_THSM',]     #参与说明
            yield extraItem
