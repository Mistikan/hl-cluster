# Скрипты
```sh
kubectl exec -ti deployment/qbittorrent -c qbt -- /bin/bash
bash /scripts/add-metadata.sh
```

# TODO
* UPNP похоже не заработал - самое оптимальное глянуть [здесь](http://192.168.88.1/cgi-bin/luci/admin/services/upnp)
* надо сделать так, чтобы ты кидал в директорию torrent файл, а он перемещался в metadata/hash.torrent и ставился на закачку правильным способом.
