# -*- coding: UTF-8 -*-
from selenium import webdriver
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from webdav4.client import Client
import os
import re
import sys
import json
import logging
import argparse
import tempfile
import feedparser


# ---------------------------------------------------------
# ⚪ 下载解包json文件 - 基于Webdav
# ---------------------------------------------------------
def dav_read_json(file_url, auth):
    url, filename = os.path.split(file_url)
    client = Client(url, auth)
    assert client.exists(filename)
    local_file = tempfile.mkstemp()[1]
    client.download_file(filename, local_file)
    with open(local_file, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    return data


# ---------------------------------------------------------
# ⚪ 打包上传json文件 - 基于Webdav
# ---------------------------------------------------------
def dav_write_json(file_url, auth, data):
    url, filename = os.path.split(file_url)
    client = Client(url, auth)
    local_file = tempfile.mkstemp()[1]
    with open(local_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    client.upload_file(local_file, filename, overwrite=True)
    

# ---------------------------------------------------------
# ⚪ 浏览器驱动
# ---------------------------------------------------------
class ChromeDriver(webdriver.Chrome):
    def __init__(self, proxy=""):
        # wget -q https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip && unzip chromedriver_linux64.zip
        # proxy: e.g. "http://127.0.0.1:1080"
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-gpu')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        if proxy != "":
            chromeOptions.add_argument("--proxy-server={}".format(proxy))
        super(ChromeDriver, self).__init__(options=chromeOptions)
        self.implicitly_wait(10)

    def get_rss(self, url):
        self.get(url)
        rss = feedparser.parse(self.page_source)
        rss_db = {}
        for i in rss['entries']:
            rss_db[i['title']] = {
                "stamp": i["published"],
                "url": i['link']
            }
        assert len(rss_db) > 0
        return rss_db

    def get_magnet(self, url):
        # 找不到怎么办？？
        try:
            self.get(url)
            element = self.find_element_by_id('a_magnet')
            magnet = element.text
        except:
            magnet = None
        return magnet


# ---------------------------------------------------------
# ⚪ 番剧数据集操作
# ---------------------------------------------------------
class DataBase(object):
    def __init__(self, json_url, auth=None):
        self.json_url = json_url
        self.auth = auth
        self.stamp = datetime(1900, 1, 1, 0, 0, 0, 0, timezone(timedelta(0, 28800)))
        self.db = dav_read_json(self.json_url, self.auth)

    def upload(self):
        dav_write_json(self.json_url, self.auth, self.db)

    def update(self, value):
        key = value["key"]
        self.db[key]["stamp"] = value["stamp"]
        for i in self.db[key]["rules"].values():
            if i["type"] == "count":
                i["context"] += 1
                break

    def detect(self, rss_db):
        rss_db_filter = {}
        used_keys = []
        for k, v in rss_db.items():
            key = self.detect_item(k)
            if key is not None and key not in used_keys:
                used_keys.append(key)
                v["key"] = key
                rss_db_filter[k] = v
        return rss_db_filter

    def detect_item(self, string):
        for k1, v1 in self.db.items():  # title
            match = True
            for v2 in v1["rules"].values():  # rules
                if v2["type"] == "find":  # 规则：查找
                    if type(v2["context"]) not in (list, tuple):
                        v2["context"] = [v2["context"]]
                    match &= sum([string.find(i) >= 0 for i in v2["context"]]) > 0
                elif v2["type"] == "count":  # 规则：计数
                    res = re.findall(r'[【\[\ ](\d{2})[】\]\ ]', string)
                    if len(res) > 1:
                        logging.warning("MultiMatch: 'count' in '{}'".format(string))
                    if (v2["context"] + 1 not in [int(r) for r in res]) or len(res) == 0:
                        match = False
            if match:
                return k1
        return None

    def save_magnet(self, url_meta, rss_db):
        for k, v in rss_db.items():
            if v["magnet"] is None:
                continue
            k = k.replace("/", "-")
            url = os.path.join(url_meta, k[:128]+".magnet")
            db = {"magnet": v["magnet"]}
            dav_write_json(url, self.auth, db)
            logging.info("Success Add {} {}".format(k, v["magnet"]))
            self.update(v)


# ---------------------------------------------------------
# ⚪ 主函数
# ---------------------------------------------------------
def main(url_rss, url_meta, url_json, auth, proxy=""):
    try:
        # 获取并解析RSS
        logging.info("Opening Chrome...")
        driver = ChromeDriver(proxy=proxy)
        rss_db = driver.get_rss(url_rss)

        # 对比数据库 - 查找更新
        logging.info("Checking Database...")
        database = DataBase(url_json, auth)
        rss_db = database.detect(rss_db)

        logging.info("Find {} update(s).".format(len(rss_db)))
        if len(rss_db) == 0:
            return

        # 获取磁链
        for k, v in rss_db.items():
            v["magnet"] = driver.get_magnet(v["url"])
            logging.info("Magnet({}): {}".format(k, v["magnet"]))

        # 下载命令
        database.save_magnet(url_meta, rss_db)

        # 更新文件
        logging.info("Upload `{}`...".format(url_json))
        database.upload()

    finally:
        logging.info("Bye!")
        driver.quit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cwd, path = os.getcwd(), os.environ["PATH"]
    if cwd not in path:
        os.environ["PATH"] = "{}:{}".format(cwd, path)

    parser = argparse.ArgumentParser()
    parser.add_argument("--url_rss", type=str)
    parser.add_argument("--url_meta", type=str)
    parser.add_argument("--url_json", type=str)
    parser.add_argument("--username", type=str, default="")
    parser.add_argument("--password", type=str, default="")
    args = parser.parse_args()

    main(args.url_rss, args.url_meta, args.url_json, (args.username, args.password))
