from selenium import webdriver
import time
from lxml import etree
import re

class LagouSpider(object):
    driver_path = r"H:\python\home_spider\Scripts\chromedriver.exe"
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        self.url = 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        self.positions = []

    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_list_page(source)
            next_btn = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
            if "page_next_disabled" in next_btn.get_attribute("class"):
                break
            else:
                next_btn.click()

    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//a[@class='position_link']/@href")
        for link in links:
            self.resuqest_detail_page(link)
            time.sleep(2)

    def resuqest_detail_page(self,url):
        # self.driver.get(url)
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = self.driver.page_source
        self.parse_detail_page(source)
        self.driver.close()  #关闭当前详情页
        self.driver.switch_to.window(self.driver.window_handles[1])#切换到列表页

    def parse_detail_page(self,source):
        html = etree.HTML(source)
        title = html.xpath('//span[@class="name"]/text()')[0]
        job_request_span = html.xpath('//dd[@class ="job_request"]//span')
        salary = job_request_span[0].html.xpath('.//text()')[0].strip()
        city = job_request_span[1].html.xpath('.//text()')[0].strip()
        city = re.sub(r"[\s/]","",city)
        work_year = job_request_span[2].html.xpath('.//text()')[0].strip()
        work_year = re.sub(r"[\s/]", "", work_year)
        education = job_request_span[3].html.xpath('.//text()')[0].strip()
        education = re.sub(r"[\s/]", "", education)
        desc = ''.join(html.xpath('//dd[@class="job_bt"]//text()')).strip()
        company = html.xpath('//h2[@class="fl"]/text()')[0].strip()
        positon ={
            'title':title,
            'company':company,
            'salary':salary,
            'city':city,
            'work_year':work_year,
            'education':education,
            'desc':desc,
        }
        self.positions.append(positon)
        print(positon)
if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()