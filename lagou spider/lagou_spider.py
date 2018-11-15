#coding:utf-8

import requests
import json
from jsonpath import jsonpath


class LagouSpider(object):
    def __init__(self):
        self.headers = {
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection" : "keep-alive",
            "Content-Length" : "25",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie" : "",
            "Host" : "www.lagou.com",
            "Origin" : "https://www.lagou.com",
            # 反爬点1：检查请求来源是否合理
            "Referer" : "https://www.lagou.com/jobs/list_python?px=default&gj=3%E5%B9%B4%E5%8F%8A%E4%BB%A5%E4%B8%8B&xl=%E6%9C%AC%E7%A7%91&hy=%E7%A7%BB%E5%8A%A8%E4%BA%92%E8%81%94%E7%BD%91&city=%E6%B7%B1%E5%9C%B3",
            # 反爬点2：客户端身份信息
            "User-Agent" : "",
            "X-Anit-Forge-Code" : "0",
            "X-Anit-Forge-Token" : "None",
            "X-Requested-With" : "XMLHttpRequest"
        }
        self.post_url = "https://www.lagou.com/jobs/positionAjax.json?"


        self.query_str = {
            "city": raw_input("请输入需要抓取的城市名:"),
            "needAddtionalResult": "false"
        }

        self.page = 0

        self.form_data = {
            "first": "false",
            "pn": self.page,
            "kd": raw_input("请输入需要抓取的职位:"),
        }

        self.item_list = []

    def send_request(self, url):
        print("[INFO]: 正在发送请求 {}".format(url))
        response = requests.post(url, params=self.query_str, data=self.form_data, headers=self.headers)
        return response


    def parse_page(self, response):
        python_obj = response.json()
        result_list = jsonpath(python_obj, "$..result")[0]
        print(result_list)

        if not result_list:
            return True

        #self.item_list = self.item_list + result_list
        #print(result_list)
        for result in result_list:
            item = {}
            item['salary'] = result['salary']
            item['city'] = result['city']
            item['positionName'] = result['positionName']
            item['district'] = result['district']
            item['createTime'] = result['createTime']
            item['companySize'] = result['companySize']
            item['companyFullName'] = result['companyFullName']
            self.item_list.append(item)

    def save_data(self):
        json.dump(self.item_list, open("lagou.json", "w"))

    def main(self):
        #while True:
        #爬取5页数据
        while self.page <= 5:
            response = self.send_request(self.post_url)
            if self.parse_page(response) == True:
                break
            self.page += 1

        self.save_data()

if __name__ == '__main__':
    spider = LagouSpider()
    spider.main()
