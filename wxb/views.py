from django.shortcuts import render,HttpResponse
from .models import Wx_wxb
# Create your views here.
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import os

headers ={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0' }

def get_url(request):
    urls = ['https://data.wxb.com/rankArticle?cate=%E5%9B%BD%E9%99%85&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E4%BD%93%E8%82%B2&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E5%A8%B1%E4%B9%90&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E7%A4%BE%E4%BC%9A&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E8%B4%A2%E7%BB%8F&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%97%B6%E4%BA%8B&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E7%A7%91%E6%8A%80&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%83%85%E6%84%9F&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%B1%BD%E8%BD%A6&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%95%99%E8%82%B2&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%97%B6%E5%B0%9A&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%B8%B8%E6%88%8F&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E5%86%9B%E4%BA%8B&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%97%85%E6%B8%B8&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E7%BE%8E%E9%A3%9F&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%96%87%E5%8C%96&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E5%81%A5%E5%BA%B7%E5%85%BB%E7%94%9F&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%90%9E%E7%AC%91&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E5%AE%B6%E5%B1%85&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E5%8A%A8%E6%BC%AB&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E5%AE%A0%E7%89%A9&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%AF%8D%E5%A9%B4%E8%82%B2%E5%84%BF&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E6%98%9F%E5%BA%A7%E8%BF%90%E5%8A%BF&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E5%8E%86%E5%8F%B2&page=1',
            # 'https://data.wxb.com/rankArticle?cate=%E9%9F%B3%E4%B9%90&page=1',
            ]
    for url in urls:
        items = get_wx_list(url)
        for item in items:
            # print(item)
            # item['url']
            new_item = Wx_wxb()
            new_item.title = item['title']
            new_item.wx_name = item['wx_name']
            new_item.read = item['read']
            new_item.catagory = item['catagory']
            new_item.wx_url = item['url']
            new_item.content = item['content']
            new_item.save()

    return HttpResponse('success')
def parser_wx_page(url,wx_name,read,catagory):
    response = requests.get(url, headers=headers)
    text = response.text
    soup = BeautifulSoup(text, 'lxml')
    title = soup.find('h2',class_="rich_media_title").get_text().strip()
    content = str(soup.find_all('div',id="js_content"))
    content =content.replace('data-src','src')
    imgs = soup.find_all('img')
    for each in imgs:
        if each.get('src'):
            item = each.get('src')
            content = content.replace(item, '')
        if each.get('data-src'):
            item = each.get('data-src')
            if item.endswith(('gif','jpeg','png')):
                if "res.wx.qq.com" in item:
                    content = content.replace(item, '')
                else:
                    new_src = item.split('/')[4] + '.' + item.split('=')[-1]
                    content = content.replace(item, '/wximgs/' + item.split('/')[4] + '.' + item.split('=')[-1])
                    download_img_tool(item, new_src)
            else:
                content = content.replace(item, '')
    position ={
        'title':title,
        'content':content,
        'wx_name':wx_name,
        'catagory':catagory,
        'read':read,
        'url':url,
    }
    return position

def get_wx_list(url):
    positions = []
    response = requests.get(url,headers=headers  )
    text = response.text
    soup = BeautifulSoup(text,'lxml')
    lists = soup.find_all('tr', class_="ant-table-row")
    catagory = unquote(url).split('=')[1].split('&')[0]
    for list in lists:
        wx_url = list.a.attrs['href']
        read = list.find_all('td')[3].get_text()
        wx_name = list.find_all('td')[1].get_text()
        result = parser_wx_page(wx_url, wx_name, read, catagory)
        positions.append(result)
    return positions

def download_img_tool(url,filename):
    # os.chdir('../')
    if not os.path.exists('../media/wximgs'):
        os.makedirs('../media/wximgs')

    r = requests.get(url)
    if "res.wx.qq.com" in filename:
        pass
    with open(os.path.join('../media/wximgs', filename), mode='wb') as f:
        f.write(r.content)

# if __name__ == '__main__':
#     get_url()