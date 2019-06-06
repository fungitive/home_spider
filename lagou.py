import json
import requests
import xlwt
import time
import random
from pyecharts import Bar

# 获取存储职位信息的json对象，遍历获得公司名、福利待遇、工作地点、学历要求、工作类型、发布时间、职位名称、薪资、工作年限
def get_json(url, datas):
    my_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Referer": "https://www.lagou.com/jobs/list_Python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=",
        "Content-Type": "application/x-www-form-urlencoded;charset = UTF-8"
    }
    proxies = ['http://163.204.243.184:9999']
    time.sleep(5)
    ses = requests.session()  # 获取session
    print(ses)
    ses.headers.update(my_headers)  # 更新
    ses.get(
        "https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=")
    content = ses.post(url=url, data=datas, )
    # # proxies = random.choice(proxies)
    # print(proxies)
    result = content.json()
    print(result)
    info = result['content']['positionResult']['result']

    info_list = []
    for job in info:
        information = []
        information.append(job['positionId'])  # 岗位对应ID
        information.append(job['city'])  # 岗位对应城市
        information.append(job['companyFullName'])  # 公司全名
        information.append(job['companyLabelList'])  # 福利待遇
        information.append(job['district'])  # 工作地点
        information.append(job['education'])  # 学历要求
        information.append(job['firstType'])  # 工作类型
        information.append(job['formatCreateTime'])  # 发布时间
        information.append(job['positionName'])  # 职位名称
        information.append(job['salary'])  # 薪资
        information.append(job['workYear'])  # 工作年限
        info_list.append(information)
        # 将列表对象进行json格式的编码转换,其中indent参数设置缩进值为2
        # print(json.dumps(info_list, ensure_ascii=False, indent=2))
    print(info_list)
    return info_list


def main():
    page = int(input('请输入你要抓取的页码总数：'))
    # kd = input('请输入你要抓取的职位关键字：')
    # city = input('请输入你要抓取的城市：')

    info_result = []
    title = ['岗位id', '城市', '公司全名', '福利待遇', '工作地点', '学历要求', '工作类型', '发布时间', '职位名称', '薪资', '工作年限']
    info_result.append(title)
    for x in range(1, page + 1):
        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        datas = {
            'first': 'false',
            'pn': x,
            'kd': 'python',
        }
        try:
            info = get_json(url, datas)
            info_result = info_result + info
            print("第%s页正常采集" % x)
        except Exception as msg:
            print("第%s页出现问题" % x)

        # 创建workbook,即excel
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建表,第二参数用于确认同一个cell单元是否可以重设值
        worksheet = workbook.add_sheet('lagouzp', cell_overwrite_ok=True)
        for i, row in enumerate(info_result):
            # print(row)
            for j, col in enumerate(row):
                # print(col)
                worksheet.write(i, j, col)
        workbook.save('lagouzp.xls')
    # print(info_result)
    # info_result = info_result[1:]
    # # print(info_result)
    # ALL_DATA = []
    # for item in info_result:
    #     # for i in item:
    #     city = item[1]
    #     company = item[2]
    #     update = item[7]
    #     work = item[8]
    #     wage= item[9]
    #     # print(item[1],item[2],item[7],item[8],item[9])
    #     # cities = cities.append(''.join(item))
    #     # print(type(city))
    #     ALL_DATA.append({'city': city, 'company':company,'work':work,'wage':wage })
    # print(ALL_DATA)
    # cities = list(map(lambda x: x['city'], ALL_DATA))
    # wage = list(map(lambda x: x['wage'], ALL_DATA))
    # company = list(map(lambda x: x['company'], ALL_DATA))
    # # print(cities)
    # chart = Bar("城市薪资榜")
    # chart.add('', cities, company)
    # chart.render('city_wage.html')
if __name__ == '__main__':
    main()