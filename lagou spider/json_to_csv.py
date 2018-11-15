#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import csv

def json_to_csv():
    json_file = open("lagou.json", "r")
    csv_file = open("lagou.csv", "w")

    item_list = json.load(json_file)

    #[]
    sheet_data = item_list[0].keys()
    #[[], [], []]
    value_data = [item.values() for item in item_list]

    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(sheet_data)
    csv_writer.writerows(value_data)

    csv_file.close()
    json_file.close()




if __name__ == "__main__":
    json_to_csv()
