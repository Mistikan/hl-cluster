# ZFS Общее
TODO: накидать команды, перенеси из прошлого репозитория.

## Переименование пула
```sh
# Выключить пул
zpool export original_name
# Импортировать пул под новым именем
zpool import original_name new_name
# Проверить статус
zpool status new_name
# Выключить пул, сохранив изменения
zpool export new_name
```

# ZFS Торренты
## Введение
На диске `/dev/sdX` создается zfs раздел для торрентов.
Под него будет выделен отдельный датасет `torrent`, чтобы в случаи необходимости не смешивать данные.
Будет настроено автоматическое монтирование для talos.
Более подробно [см. статью](torrent.md).

## Подготовка
```sh
export ZFS_DISK=/dev/sdX
export ZFS_POOL_NAME=wd_black_1tb_pool
export ZFS_MOUNTPOINT=/var/mnt/zfs/$ZFS_POOL_NAME/torrent
```

## Создание пула
```sh
zpool create \
  -o ashift=12 \
  -O compression=lz4 \
  -O dedup=on \
  -O atime=off \
  -O recordsize=1M \
  $ZFS_POOL_NAME $ZFS_DISK
```

## Создание датасета
```sh
zfs create $ZFS_POOL_NAME/torrent
```

## Установка "только чтения" после копирования данных
```sh
zfs set readonly=on $ZFS_POOL_NAME/torrent
```

## Установка точки монтирования
```sh
zfs set mountpoint=none            $ZFS_POOL_NAME
zfs set mountpoint=$ZFS_MOUNTPOINT $ZFS_POOL_NAME/torrent
```

## Проверка
```sh
zfs list
zpool list
zpool status
```

## Примечание
* Модель: `DeepSeek-V3`;
* Запрос:
    ```
    Привет. Я хочу создать ZFS на моём диске wg green. Требования:
        * игнорировать badblocks
        * основные данные - торренты
        * использовать дедупликацию
        * использовать сжатие
        * раздел после копирования данных всегда будет только в режиме чтения
    Посоветуй, пожалуйста, команды.
    ```
