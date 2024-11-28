# hl-cluster (homelab-cluster)
## TODO
* прикрутить домен
* пробросить порты для:
    * bitmagnet
    * torrent
* upsmon чей extensions в talos нужен
* подключить ИБП
* kubevirt, local-path - переделать на нормальный деплой, все манифесты уже лежат
* поменять ssh подпись в этом репозитории
* https://github.com/gimlet-io/capacitor

## GUI/X-Server
1. Поставить generic-device-plugin, указав ему доступ к `/dev/dri` в качестве ресурса.
1. Запустить pod `tests/test-dri.yaml`, в котором описан данный ресурс.
1. Провалиться в под.
1. Поставить X сервер. См. репозиторий: https://github.com/bedrin/docker-x-server
1. Запустить X сервер фоном:
  ```sh
  /usr/bin/X :0 -nolisten tcp vt1 &
  ```

1. Запустить xclock или другое графическое приложение:
  ```sh
  DISPLAY=:0 xclock
  ```

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
    * Link: https://mysku.club/blog/aliexpress/100352.html
    * Android APP: Smart Life - Smart Living
    * https://github.com/rkosegi/tuya-smartplug-exporter
    * id, key смотри в keepassxc
* Network:
  * Mikrotik RBD52G-5HacD2HnD
* Etc

## Kubevirt
* https://github.com/siderolabs/talos/pull/9522 - kubevirt

### Get vmi
```sh
kubectl get vmi
```

### Delete vmi
```sh
kubectl delete vmi fedora-vm
```

### Start
```sh
./virtctl start fedora-vm
```

### Console
```sh
./virtctl console fedora-vm
```

### Stop
```sh
./virtctl stop fedora-vm
```

## Заметки
### Энергоэффективность (C-States)
* https://wiki.archlinux.org/title/Powertop
* https://selectel.ru/blog/cpu-power-management/

### Энергоэффективность (E-core/P-core)
На моём железе не поддерживается, т.к. только с [12 поколения intel](https://www.intel.com/content/www/us/en/support/articles/000097881/processors.html).

Но если будет, то:
* [irqbalance app](https://github.com/onedr0p/home-ops/commit/81d32eb2c40307f99941af763e5f51db4a140043#diff-bc63c0dee1b104ef6491529ca31a042283876f17e384dee97b980f8e5feafb6dL13);
* [irqbalance github](https://github.com/Irqbalance/irqbalance/);

## Sops
### Открытие файла для изменения
```sh
EDITOR=nano sops /workspaces/hl-cluster/kubernetes/flux/vars/cluster-secrets.sops.yaml
```

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

### VolumeStatus (партиции)
```sh
talosctl get volumestatus
```

### Найденные партиции
```sh
talosctl get discoveredvolumes
```

## WOL
Включить сервер:
```sh
wakeonlan 18:C0:4D:E0:AB:B5
```

## Links
* https://github.com/onedr0p/home-ops
* https://github.com/buroa/k8s-gitops
* https://kubesearch.dev/
* https://github.com/budimanjojo/talhelper
* https://github.com/wavyland/wavy
