# -*- coding: UTF-8 -*-
from selenium import webdriver
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import feedparser
import argparse
import sys
import os
import json
import re
import warnings


# sshpass -p * scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ./AnimeDB.json antony@www.xujie-plus.tk:/root/openfiles/json/AnimeDB.json
# sshpass -p * scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no antony@www.xujie-plus.tk:/root/openfiles/json/AnimeDB.json ./AnimeDB.json
# sshpass -p * ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no antony@www.xujie-plus.tk qbittorrent-nox
# datetime.strptime(i["published"], '%a, %d %b %Y %X %z')


class ChromeDriver(webdriver.Chrome):
    def __init__(self, proxy=None):
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


class DataBase(object):
    def __init__(self, path):
        self.path = path
        self.stamp = datetime(1900, 1, 1, 0, 0, 0, 0, timezone(timedelta(0, 28800)))
        self.load()

    def load(self):
        assert self.path.endswith(".json")
        if not os.path.exists(self.path):
            print("[Info] Cannot open {}, download from `www.xujie-plus.tk`.".format(self.path))
            assert os.system("curl https://www.xujie-plus.tk/openfiles/json/AnimeDB.json -o {}".format(self.path)) == 0
        with open(self.path, "r") as f:
            self.db = json.load(f)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

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
                        warnings.warn("MultiMatch: 'count' in '{}'".format(string))
                    elif len(res) == 0:
                        match = False
                    else:
                        match &= int(res[0]) > v2["context"]
            if match:
                return k1
        return None


def update_anime(args):
    try:
        # 获取并解析RSS
        print("[Info] Opening Chrome...")
        driver = ChromeDriver(proxy=args.proxy)
        rss_db = driver.get_rss(args.url)

        # 对比数据库
        print("[Info] Checking Database...")
        database = DataBase(args.db_path)
        rss_db = database.detect(rss_db)

        print("[Info] Find {} update(s).".format(len(rss_db)))
        print(tuple(rss_db.keys()))
        if len(rss_db) == 0:
            return

        # 获取磁链
        for k, v in rss_db.items():
            v["magnet"] = driver.get_magnet(v["url"])
            print("[Info] Magnet({}): {}".format(k, v["magnet"]))

        # 添加到服务器
        for k, v in rss_db.items():
            if v["magnet"] is None:
                continue
            cmd = "{} ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no antony@www.xujie-plus.tk qbittorrent-nox {}".format(args.sshpass, v["magnet"])
            if os.system(cmd) == 0:
                print("[Info] Success Add {} {}".format(k, v["magnet"]))
                database.update(v)
        database.save()

        # 更新文件
        print("[Info] Upload `{}` by scp...".format(args.db_path))
        cmd = "{} scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {} antony@www.xujie-plus.tk:/root/openfiles/json/".format(args.sshpass, args.db_path)
        assert os.system(cmd) == 0
        
    finally:
        driver.quit()


if __name__ == "__main__":
    cwd, path = os.getcwd(), os.environ["PATH"]
    if cwd not in path:
        os.environ["PATH"] = "{}:{}".format(cwd, path)

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="https://share.dmhy.org/topics/rss/rss.xml")
    parser.add_argument("--proxy", type=str, default="")
    parser.add_argument("--db_path", type=str, default="./AnimeDB.json")
    parser.add_argument("--sshpass", type=str, default="")
    args = parser.parse_args()

    # --proxy http://127.0.0.1:1080 --sshpass "sshpass -p ******"
    update_anime(args)
