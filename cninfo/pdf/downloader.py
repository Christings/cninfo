#!/usr/bin/python
# coding = utf-8
# __author__='Lilly'
# description:下载csv中列出的pdf年报

import csv
import os
import time
import requests

MAX_COUNT = 5
DST_DIR = 'D:/workspace/cninfo/report/agriculture/'
LIST_FILE = 'D:/workspace/cninfo/report/agriculture/2018农业上市企业信息_20020206-20180417.csv'

if __name__ == '__main__':
    assert (os.path.exists(DST_DIR)), 'No such destination directory \"' + DST_DIR + '\"!'
    assert (os.path.exists(LIST_FILE)), 'No such list file \"' + LIST_FILE + '\"!'
    if DST_DIR[len(DST_DIR) - 1] != '/':
        DST_DIR += '/'
    # 读取待下载文件列表
    with open(LIST_FILE, 'r') as csv_in:
        reader = csv.reader(csv_in)
        for each in enumerate(reader):
            download_count = 1
            download_token = False
            while download_count <= MAX_COUNT:
                try:
                    download_count += 1
                    r = requests.get(each[1][1])
                    download_token = True
                    break
                except:
                    # 下载失败则报错误
                    print(str(each[0] + 1) + '::' + str(download_count) + ':\"' + each[1][0] + '\" failed!')
                    download_token = False
                    time.sleep(3)
            if download_token:
                # 下载成功则保存
                with open(DST_DIR + each[1][0], 'wb') as file:
                    file.write(r.content)
                    print(str(each[0] + 1) + ': \"' + each[1][0] + '\" downloaded.')
            else:
                # 彻底下载失败则记录日志
                with open(DST_DIR + 'error.log', 'a') as log_file:
                    log_file.write(
                        time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())) + 'Failed to download\"' +
                        each[1][0] + '\"\n')
                    print('...' + str(each[0] + 1) + ':\"' + each[1][0] + '\" finally failed ...')
