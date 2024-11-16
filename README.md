# hl-cluster (homelab-cluster)
## TODO
* пробросить порты для:
    * bitmagnet
    * torrent
* https://github.com/onedr0p/home-ops/commit/81d32eb2c40307f99941af763e5f51db4a140043#diff-bc63c0dee1b104ef6491529ca31a042283876f17e384dee97b980f8e5feafb6dL13
    * для снижения энергопотребления и поиска производительности
* upsmon чей extensions в talos нужен

## Hardware
TODO:
* Server anaconda
  * Motherboard: Gigabyte Technology Co., Ltd. B560M DS3H
    * [Manual](https://download.gigabyte.com/FileList/Manual/mb_manual_b560m-ds3h-ac_e_v1.pdf)
    * BIOS:
      * Version: F11
      * Date: 12/19/2023
  * CPU: 11th Gen Intel(R) Core(TM) i5-11400 @ 2.60GHz
  * RAM:
    * KHX2666C16/8G
    * KHX2666C16/8G
  * NVME:
    * KINGSTON SKC3000S512G - 512 GB
  * SATA:
    * SSD - 256GB RUN S9 256 - 256 GB
    * HDD - WDC WD10EACS-14Z Green - 1TB
    * TODO: ещё диски
  * KVM: KCEVE KVM401A
  * FAN: TODO - охлаждение башня и просто вентиляторы
  * APC:
    * Model: TODO
    * Battery: TODO
  * Умная розетка: Atorch S1-B/W/T/H
* Network:
  * Mikrotik RBD52G-5HacD2HnD
* Etc

## ZFS
### Pool
| Pool name | Disk                             | Size |
|-----------|----------------------------------|------|
| storage   | KINGSTON SKC3000S512G x 1        | 336G |
| TODO      | Seagate IronWolf ST4000NV006 x 2 | 4 TB |

### OpenEBS
* https://openebs.io/docs/4.0.x/user-guides/local-storage-user-guide/local-pv-zfs/zfs-configuration

## Flux
### Обновить состояние git
```sh
flux reconcile source git home-kubernetes
```

### Пересинк (помогает, если снёс релиз и надо заново накатить)
```sh
flux suspend kustomization --all
flux resume kustomization --all
```

### Получить kustomizations
```sh
flux get kustomizations
```

### Получить helmrelease
```sh
flux get helmreleases -A
```

### Получить sources git
```sh
flux get sources git
```

### Получить sources helm
```sh
flux get sources helm
```

### Получить всё
```sh
flux get all
```

## Talos
### Reboot node
```sh
talosctl reboot -m powercycle
```

### Services
```sh
talosctl services
```

# VolumeStatus (партиции)
```sh
talosctl get volumestatus
```

# Найденные партиции
```sh
talosctl get discoveredvolumes
```

## Links
* https://github.com/onedr0p/home-ops
* https://github.com/buroa/k8s-gitops
* https://kubesearch.dev/
* https://github.com/budimanjojo/talhelper
