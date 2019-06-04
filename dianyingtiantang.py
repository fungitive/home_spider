import requests
from lxml import etree
BASE_DOMAIN = 'https://www.dytt8.net/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
}
def get_detail_url(url):
    response = requests.get(url,headers=headers)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    detail_urls = html.xpath('//a[@class="ulink"][2]/@href')
    # detail_urls = html.xpath('//table[@class="tbspan"]//a/@href')
    # print(detail_urls)
    # detail_urls = map(lambda url:BASE_DOMAIN+url,detail_urls)
    return  detail_urls
    # for detail_url in detail_urls:
    #     print(BASE_DOMAIN+detail_url)
def detail_page_parse(url):
    movie = {}
    response = requests.get(url, headers=headers)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath('//div[@class="title_all"]/h1/font[@color="#07519a"]/text()')[0]
    movie['title'] = title
    covers = html.xpath('//div[@id="Zoom"][1]//img/@src')[0]
    movie['covers'] = covers
    img2 = html.xpath('//div[@id="Zoom"][1]//img[2]')
    if img2:
        screenshot = html.xpath('//div[@id="Zoom"][1]//img/@src')[1]
        movie['screenshot'] = screenshot
        # print(screenshot)
    if not img2 :
        screenshot = ''
        movie['screenshot'] = screenshot
    zoomE = html.xpath('//div[@id="Zoom"]')[0]
    def parse_info(info,rule):
        return info.replace(rule,"").strip()
    infos  =  zoomE.xpath('.//text()')
    for index,info in enumerate(infos):
        if info.startswith("◎片　　名　"):
            info = parse_info(info,"◎片　　名")
            movie['name'] =info
        if info.startswith("◎年　　代"):
            info = parse_info(info,"◎年　　代")
            movie['year'] =info
        if info.startswith("◎产　　地"):
            info = parse_info(info, "◎产　　地")
            movie['country'] = info
        if info.startswith("◎类　　别"):
            info = parse_info(info,"◎类　　别")
            movie['type'] =info
        if info.startswith("◎语　　言"):
            info = parse_info(info,"◎语　　言")
            movie['language'] =info
        if info.startswith("◎字　　幕"):
            info = parse_info(info,"◎字　　幕")
            movie['caption'] =info
        if info.startswith("◎导　　演"):
            info = parse_info(info,"◎导　　演")
            movie['director'] =info
        if info.startswith("◎豆瓣评分"):
            info = parse_info(info,"◎豆瓣评分")
            movie['douban'] =info
        if info.startswith("◎主　　演"):
            info = parse_info(info,"◎主　　演")
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            movie['actor'] = actors
        if info.startswith("◎简　　介"):
            info = parse_info(info, "◎简　　介")
            summarys =[info]
            for x in range(index + 1, len(infos)):
                summary = infos[x].strip()
                if summary.startswith("◎"):
                    break
                summarys.append(summary)
            movie['summary'] = summarys
    dlink1 = zoomE.xpath('.//a/@href')[0]
    movie['dlink1'] = dlink1
    dlink2 = zoomE.xpath('.//a/@href')[1]
    movie['dlink2'] = dlink2
    return movie

def main():
    url = 'https://www.dytt8.net/html/gndy/rihan/list_6_1.html'
    detail_urls = get_detail_url(url)
    for detail_url in detail_urls:
        movie_url = BASE_DOMAIN+detail_url
        movie_detail = detail_page_parse(movie_url)
        print(movie_detail)
        print('*'*50)

if __name__ == '__main__':
    main()
