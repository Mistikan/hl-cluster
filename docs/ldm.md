# Монтирование LDM раздела (WD Blue 1 TB)
## Поиск
```sh
ls /dev/disk/by-uuid/ -lah | grep dm

lrwxrwxrwx 1 root root  10 мар 28 18:21 0513991F235D07B5 -> ../../dm-0
```

## Проверка
```sh
dmsetup info /dev/dm-0

Name:              ldm_vol_MIST-Dg0_Volume1
State:             ACTIVE
Read Ahead:        256
Tables present:    LIVE
Open count:        0
Event number:      0
Major, minor:      252, 0
Number of targets: 2
UUID: LDM-Volume1-118af483-488d-46a0-a83e-14263aad0871
```

## Монтирование
```sh
mkdir /mnt/wd_blue_1tb_ldm
mount -o ro /dev/dm-0 /mnt/wd_blue_1tb_ldm
```

## Копирование данных
```sh
rsync -av --progress --stats /mnt/wd_blue_1tb_ldm/ /var/mnt/zfs/pool_data/wd_blue_1tb/ldm/ 2>/var/mnt/zfs/pool_data/wd_blue_1tb/ldm_rsync_error.txt
```
