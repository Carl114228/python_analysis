from lxml import etree
import requests
import random
import pandas as pd
# 代理池，模拟不同的浏览器对网站发送请求
ua_list = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]
def web_data(page):
    URL = f'https://kaijiang.zhcw.com/zhcw/html/ssq/list_{page}.html'
    headers = {"user-agent": random.choice(ua_list)}
    try:
        response =requests.get(url=URL,headers=headers,timeout=100)
        if response.status_code != 200:
            print(f"{page}页爬取失败,状态码，Status_code:{response.status_code}")
            return []
        print(f"正在爬取第{page}页,并存入列表中*****")
        # print(response.text)#获取网页信息（包含）
        html = etree.HTML(response.text)    #获取整个页面结构
        # 在html代码中寻找table，并且class=wqhgt
        rows = html.xpath("//table[@class='wqhgt']//tr")[2:]    #//tr表示获取-table-标签中所有子标签的tr标签
        # print(rows)
        data_list = []
        for row in rows:
            # print(row)
            # ./表示当前标签下的某个子标签
            tds = row.xpath("./td") #这里开始错写为tr
            # print(tds)
            if len(tds) <=6:
                continue
            date = tds[0].xpath("./text()")[0].strip()
            # print(date)
            issue = tds[1].xpath("./text()")[0].strip()
            # print(issue)
            ems = tds[2].xpath(".//em/text()")
            # print(ems)
            red_balls = ems[0:6]  #得到红球
            blue_ball = ems[-1]  #拿出蓝球
            # print(red_balls,blue_ball)
            sales = tds[3].xpath(".//strong/text()")[0].replace(',','').strip()   #销售额
            # print(sales)
            first = tds[4].xpath(".//strong/text()")[0].strip()     #一等奖
            # print(first)
            second = tds[5].xpath(".//strong/text()")[0].strip()    #二等奖
            # print(second)
            # 输出中奖号码
            winner_ball  = " ".join(red_balls)+" "+blue_ball
            # print(winner_ball)
            #将爬取到的数据存在data_list中
            data_list.append([
                date,issue,
                red_balls[0],red_balls[1],red_balls[2],
                red_balls[3], red_balls[4], red_balls[5],
                blue_ball,winner_ball,
                sales,first,second
            ])
        print(f"第{page}页爬取成功，数据为{data_list}")
        return data_list
    except Exception as e:
        print(f"服务器或网络错误,请重试：{page}页出现异常：{e}")
        return []
def save_data(data):
    colums=["开奖日期","期号","红1","红2","红3","红4","红5","红6","蓝球","中奖号码","销售额","一等奖","二等奖"]
    df = pd.DataFrame(data,columns=colums)
    df.to_csv("TwoColorBall.csv",index=False,encoding = "utf-8")
if __name__ == '__main__':
    # web_data(page=1)
    all_data = []
    for i in range(1,178): #用for循环调用web_data(page)将1~177页的数据extend到all_data中
        page_data = web_data(i)
        all_data.extend(page_data)
    save_data(all_data)
