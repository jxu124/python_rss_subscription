# rss_magnet
rss_magnet

[![GitHub Test Badge][1]][2]

[1]: https://github.com/jxu124/rss_magnet/workflows/DMHY_UPDATE/badge.svg "GitHub Test Badge"
[2]: https://github.com/jxu124/rss_magnet/actions "GitHub Actions Page"

## Prepare

```bash
pip install -r requarements.txt
```

## Usage

```bash
URL_RSS="https://share.dmhy.org/topics/rss/rss.xml"
URL_META="https://a.jxu124.ml/webdav/configure/anime_query"
URL_JSON="https://a.jxu124.ml/webdav/configure/AnimeDB.json"
python main.py --url_rss "$URL_RSS" --url_meta "$URL_META" --url_json "$URL_JSON" --username admin --password 123456
```
