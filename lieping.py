import requests
from lxml import etree
import re

BASE_DOMAIN = 'https://www.liepin.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
}
positions = []
def list_url(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    links = html.xpath('//div[@class="job-info"]/h3/a/@href')
    for link in links:
        if 'http' not  in link:
            link = BASE_DOMAIN+link
        detail_page_paser(link)

def detail_page_paser(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    if html.xpath('//div[@class="title-info"]'):
        title = html.xpath('//div[@class="title-info"]/h1/text()')[0].strip()
        company = html.xpath('//div[@class="title-info"]/h3/a/text()')[0].strip()
    if html.xpath('//div[@class="title-info "]'):
        title = html.xpath('//div[@class="title-info "]/h1/text()')[0].strip()
        company = html.xpath('//div[@class="title-info "]/h3/text()')[0].strip()
    city = ''.join(html.xpath('//p[@class="basic-infor"]/span//text()')).strip()
    if html.xpath('//p[@class="job-main-title"]/text()'):
        salary = html.xpath('//p[@class="job-main-title"]/text()')[0].strip()
        salary = re.sub(r"[\s/]", "", salary)
    if  html.xpath('//p[@class="job-item-title"]/text()'):
        salary =  html.xpath('//p[@class="job-item-title"]/text()')[0].strip()
        salary = re.sub(r"[\s/]", "", salary)
    if html.xpath('//div[@class="job-qualifications"]'):
        job_qualifications_span = html.xpath('//div[@class="job-qualifications"]/span')
        education = job_qualifications_span[0].xpath('.//text()')[0].strip()
        work_year = job_qualifications_span[1].xpath('.//text()')[0].strip()

    if html.xpath('//div[@class="resume clearfix"]'):
        job_qualifications_span = html.xpath('//div[@class="resume clearfix"]/span')
        education = job_qualifications_span[0].xpath('.//text()')[0].strip()
        work_year = job_qualifications_span[1].xpath('.//text()')[0].strip()
    desc = html.xpath('//div[@class="content content-word"]/text()')
    position = {
        'title': title,
        'company': company,
        'salary': salary,
        'city': city,
        'work_year': work_year,
        'education': education,
        'desc': desc,
    }
    positions.append(position)
    # print(title,company,city,salary)
    return positions

def next_page():
    start_url = 'https://www.liepin.com/zhaopin/?init=-1&headckid=cea944f09b0fc0ba&fromSearchBtn=2&ckid=cea944f09b0fc0ba&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=python&siTag=I-7rQ0e90mv8a37po7dV3Q%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=57dfae61aa9de50a8ab5add30be60bec&d_curPage=98&d_pageSize=40&d_headId=57dfae61aa9de50a8ab5add30be60bec&curPage=99'
    urls = [start_url]
    for link in urls:
        response = requests.get(link, headers=headers)
        html = etree.HTML(response.text)
        next2_url = BASE_DOMAIN + html.xpath('//div[@class="pagerbar"]/a[8]/@href')[0].strip()
        last_url = BASE_DOMAIN + html.xpath('//a[@class="last"||[@class="last disabled"]/@href')[0].strip()
        urls.append(next2_url)
        if next2_url == last_url:
             break

    # if html.xpath('//div[@class="pagerbar"]/a[8]/@href'):
    #     next_url = BASE_DOMAIN + html.xpath('//div[@class="pagerbar"]/a[8]/@href')[0].strip()
    #     urls.append(next_url)
    #     response = requests.get(next_url, headers=headers)
    #     html = etree.HTML(response.text)
    #     next1_url = BASE_DOMAIN + html.xpath('//div[@class="pagerbar"]/a[8]/@href')[0].strip()
    #     urls.append(next1_url)
    # last_url = BASE_DOMAIN+html.xpath('//a[@class="last"]/@href')[0].strip()
    #
    #     if next2_url == last_url:
    #         break
    #     break
    #     print(link)

def main():
    next_page()
    # list_url(url)

if __name__ == '__main__':
    main()