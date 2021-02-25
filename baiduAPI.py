from aip import AipOcr
import os
import sys
import requests
import time
import tkinter as tk
from tkinter import filedialog
import base64
import cv2

APP_ID = '23672431'
API_KEY = 'ebvx2Gy6im6p2ZFin8R6HBec'
SECRET_KEY = 'egEr3r8p16pZxOvPh3YuGYWSO80L1k39'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

fname = 'sample.jpg'


def get_file_content(filePath):
    print(filePath)
    img = cv2.imread(filePath)
    print(img)
    img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))
    newFilePath = filePath + '.small.png'
    cv2.imwrite(newFilePath, img)
    with open(newFilePath, 'rb') as fp:
        return fp.read()


def file_download(url, file_path):
    r = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(r.content)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    data_dir = filedialog.askdirectory(
        title='/Users/huaihaizi/Desktop/Term7/Capstone/Data/image')
    result_dir = filedialog.askdirectory(
        title='/Users/huaihaizi/Desktop/Term7/Capstone/Data/output')
    num = 0
    for name in os.listdir(data_dir):
        if name.endswith('.small.png'):
            continue
        if not name.endswith('.png'):
            continue
        print('{0} : {1} processing'.format(num + 1, name.split('.')[0]))
        image = get_file_content(os.path.join(data_dir, name))
        # image = base64.b64encode(image)
        res = client.tableRecognitionAsync(image)

        # print ("res:", res)
        if 'error_code' in res.keys():
            print('Error! error_code: ', res['error_code'])
            sys.exit()
        req_id = res['result'][0]['request_id']

        for count in range(1, 20):
            res = client.getTableRecognitionResult(req_id)
            print(res['result']['ret_msg'])
            if res['result']['ret_msg'] == '已完成':
                break
            else:
                time.sleep(1)

        url = res['result']['result_data']
        xls_name = name.split('.')[0] + '.xls'
        # xls_name = name.split('.')[0] + '.jpg'
        file_download(url, os.path.join(result_dir, xls_name))
        num += 1
        print('{0} : {1} finished downloaded'.format(num, xls_name))
        time.sleep(1)
