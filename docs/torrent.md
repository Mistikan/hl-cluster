# ВАЖНО
**ВАЖНО**: в конце есть issue с поиском похожих файлов на диске.

# О чём документ
Как лучше поддерживать структуру в qbittorrent, основные идеи, что можно улучшить и скрипты.

# Файловая структура
```
torrent
├── data
│   ├── hash1
│   |   └── file.mkv
│   └── hashN
│       └── file.txt
└── metadata
    ├── hash1.torrent
    └── hashN.torrent
```

Директорию torrent рекомендуется создавать, чтобы обозначить характер данных (**ВАЖНО: при условии, что под данные не выделен отдельный датасет. Тогда можно сразу переходить ниже.**).
Требуется сохранять torrent файлы, чтобы при возможности можно их было легко добавить в торрент клиент.
Создавать подпапку не требуется, т.к. данные уже лежат в директории с хешем торрента (дополнительная вложенность не требуется).
Qbittorrent - Настройки - Загрузки - При добавлении торрента - Состав содержимого торрента = Не создавать подпапку.

# Readonly
При возможности на файлы ставить RO, если файлы скачались и не требуют удаления.
Это лишний раз защитит от случайных факторов изменения файлов.

# Существующие хранилища
```sh
zpool list
NAME           SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT # Disk
torrent_pool   928G   715G   213G        -         -     0%    77%  1.02x    ONLINE  -       # WD Green 1 TB
```

# Создание структуры с помощью мигратора
На коленке был накидан скрипт, который:
* по размерам и их именам в метаинформации пытается найти требуемые файлы;
* копирует их в требуемую директорию для формирования будущей структуры;
* перемещает их после копирования (директорию рекомендуется размещать на том же разделе, чтобы было просто перемещение файловой записи, а не данных).

Скрипт не лишён недостатков, но помогает разгребсти завалы.

[migrator.py](./torrent/migrator.py).

# Быстрое добавление торрентов
Требуется стоять в директории с торрентами:
```sh
export HASHS=$(find . -type f -name '*.torrent' -exec basename {} '.torrent' \;)
IFS=$'\n'
for HASH in $HASHS
do
  qbt torrent add file $HASH.torrent \
    --create-root-folder false \
    --paused \
    --folder /media/data/$HASH \
    --url http://localhost:8000
done
```

# Ссылки
* [qbt torrent add file](https://github.com/fedarovich/qbittorrent-cli/wiki/qbt-torrent-add-file)
* [tor cache](https://torrends.to/sites/torrent-storage-caching/)
* [qBittorrent-File-Matcher](https://github.com/xob0t/qBittorrent-File-Matcher)
* [torrent2ipfs](https://github.com/riffcc/torrent2ipfs/)
* [ПОИСК ПОХОЖИХ ФАЙЛОВ](https://github.com/qbittorrent/qBittorrent/issues/6520)
