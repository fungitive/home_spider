import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

ALL_DATA = []
def parse_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
    }
    response = requests.get(url,headers=headers)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text,'html5lib')
    conMidtab = soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds =tr.find_all('td')
            city = tds[0]
            if index == 0:
                city =tds[1]
            city = list(city.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            # print({'city':city,'min_temp':min_temp})
            ALL_DATA.append({'city':city,'min_temp':int(min_temp)})
            # content = '城市：{}  ,最低温度：{}'.format(city,min_temp)
            # f = open('tests.txt', 'a', encoding='utf-8')
            # f.write(content)
            # f.write('\n')
            # f.close()


def main():
    eara = {'hb','db','xb','xn','hd','hn','hz','gat'}
    for i in eara:
        url = 'http://www.weather.com.cn/textFC/{}.shtml'.format(i)
        parse_page(url)
    #分析数据
    # def sort_key(data):
    #     min_temp = data['min_temp']
    #     return min_temp
    # ALL_DATA.sort(key=sort_key)
    ALL_DATA.sort(key=lambda data:data['min_temp'])
    # print(ALL_DATA)
    data = ALL_DATA[-10:-1]
    cities = list(map(lambda x:x['city'],data))
    temps = list(map(lambda x:x['min_temp'], data))

    # print(data)
    chart = Bar("中国天气最低气温排行榜")
    chart.add('',cities,temps)
    chart.render('weather.html')


if __name__ == '__main__':
    main()