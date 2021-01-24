# rss_magnet
rss_magnet

[![GitHub Test Badge][1]][2]

[1]: https://github.com/antonyxu-git/rss_magnet/workflows/Dmhy/badge.svg "GitHub Test Badge"
[2]: https://github.com/antonyxu-git/rss_magnet/actions "GitHub Actions Page"

## Prepare


```bash
pip install -r requarements.txt
```

## Usage

```bash
URL="https://share.dmhy.org/topics/rss/rss.xml"
JSON_PATH="antony@www.xujie-plus.tk:/root/openfiles/json/AnimeDB.json"
CMD_ADD_MAGNET="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no antony@www.xujie-plus.tk qbittorrent-nox"

python main.py --proxy "" --url "$URL" --db_path "$JSON_PATH" --cmd_sshpass "${{ secrets.SSHPASS }}" --cmd_add_magnet "$CMD_ADD_MAGNET"
```
