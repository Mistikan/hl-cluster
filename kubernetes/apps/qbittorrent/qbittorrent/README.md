# Скрипты
```sh
kubectl exec -ti deployment/qbittorrent -c qbt -- /bin/bash
bash /scripts/add-metadata.sh
```

# TODO
* Заменить одинаковые файлы хардлинками - вот утилита: https://man7.org/linux/man-pages/man1/hardlink.1.html
* UPNP похоже не заработал - самое оптимальное глянуть [здесь](http://192.168.88.1/cgi-bin/luci/admin/services/upnp)
* надо сделать так, чтобы ты кидал в директорию torrent файл, а он перемещался в metadata/hash.torrent и ставился на закачку правильным способом.
