# hl-cluster (homelab-cluster)
## TODO AUTOASPM - внедрить
```yaml
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: autoaspm
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: autoaspm
  template:
    metadata:
      labels:
        name: autoaspm
    spec:
      initContainers:
      - name: autoaspm
        image: ghcr.io/mistikan/autoaspm:1.0.4
        securityContext:
          privileged: true
        resources:
          limits:
            memory: 100Mi
            cpu: 100m
          requests:
            cpu: 100m
            memory: 100Mi
      containers:
      - name: sleep
        image: ghcr.io/mistikan/autoaspm:1.0.4
        command: ["/bin/sh", "-c", "sleep infinity"]
        resources:
          limits:
            memory: 25Mi
            cpu: 10m
          requests:
            cpu: 10m
            memory: 25M
      terminationGracePeriodSeconds: 30
```

## TODO
* установка ingress-nginx. Как это делается:
  * ставится https://github.com/onedr0p/home-ops/tree/main/kubernetes/main/apps/network/nginx/internal в первозданном виде:
    * нужно сразу IP, который будет обслуживать внутренние запросы отделать от кубера. Будет что-то на уровне плавающего IP
    * при необходимости можно прикрутить external-dns к микроту, чтобы там обновлялись A записи
      * https://github.com/mirceanton/external-dns-provider-mikrotik
    * в микроте настроить все записи с доменом на внутренний хост
  * добавляются ингрессы, им ставится метка с internal - примеров в репозитории достаточно
* прикрутить домен
* пробросить порты для:
    * bitmagnet
    * torrent
* upsmon чей extensions в talos нужен
* подключить ИБП
* kubevirt, local-path - переделать на нормальный деплой, все манифесты уже лежат
* поменять ssh подпись в этом репозитории:
  ```sh
  user@user-Vostro-5502:~/projects/github$ cd Mistikan/
  user@user-Vostro-5502:~/projects/github/Mistikan$ git clone git@github.com:Mistikan/hl-cluster.git
  user@user-Vostro-5502:~/projects/github/Mistikan$ cd hl-cluster/
  user@user-Vostro-5502:~/projects/github/Mistikan/hl-cluster$ git config user.email
  sereja.ermeikin@google.com
  ```
  Настройки перечитаются, если репу переклонировать.
  Надо подумать над github настройками и переклонировать все репы.
* https://github.com/gimlet-io/capacitor
* https://github.com/ahgraber/homelab-gitops-k3s/tree/main/kubernetes/apps/default/homepage
* DNS - внутренние сервисы должны резолвится по внутренним IP как для ethernet, так и для wifi подключений со стороны ноутбука, телефона и т.д..

# ВАЖНО: TALOS KERNEL
Собрал первое ядро.

Директории на ноутбуке:
* /home/user/projects/pkgs
* /home/user/projects/talos/talos

Собранное ядро и образ лежат в проектах (Container registry):
* https://xlab.xlab12.ru/ermeikinsv/kernel
* https://xlab.xlab12.ru/ermeikinsv/imager

Требуется перепулить образ в публичное место и указать его в конфигурации талоса с последующим применением.

# Сборка ядра и образа talos
```sh
# Проверь, что у тебя работает push в ghcr.io/mistikan/

# В репозитории pkgs
# https://www.talos.dev/v1.9/advanced/customizing-the-kernel/
git clone https://github.com/siderolabs/pkgs.git
cd pkgs
git checkout release-1.9
make kernel-menuconfig PLATFORM=linux/amd64
make kernel PUSH=true REGISTRY=ghcr.io USERNAME=mistikan PLATFORM=linux/amd64

# Утилита dive - посмотреть содержимое образа

# В репозитории talos
# Добавить/убрать модуль можно в файле hack/modules-amd64.txt
# https://www.talos.dev/v1.9/advanced/building-images/
git clone https://github.com/siderolabs/talos.git
cd talos
git checkout v1.9.0
make kernel initramfs PKG_KERNEL=ghcr.io/mistikan/kernel:v1.9.0-21-gc1f06e5-dirty PLATFORM=linux/amd64
make imager PKG_KERNEL=ghcr.io/mistikan/kernel:v1.9.0-21-gc1f06e5-dirty PLATFORM=linux/amd64 INSTALLER_ARCH=targetarch IMAGE_REGISTRY=ghcr.io USERNAME=mistikan PUSH=true

# Обновление
talosctl --nodes anaconda upgrade --image="ghcr.io/mistikan/imager:v1.9.2-dirty" --timeout=10m
```

## POWERTOP
### Включение kernel опций
Лучше конечно включить через y, а не модуль.
```
CONFIG_SND_AC97_POWER_SAVE=y
CONFIG_SND_AC97_POWER_SAVE_DEFAULT=0

CONFIG_PM_GENERIC_DOMAINS=y
CONFIG_WQ_POWER_EFFICIENT_DEFAULT=y
CONFIG_PM_GENERIC_DOMAINS_SLEEP=y
CONFIG_ENERGY_MODEL=y

CONFIG_X86_MSR=y
CONFIG_X86_5LEVEL=y

CONFIG_POWERCAP=y
CONFIG_INTEL_RAPL_CORE=m
CONFIG_INTEL_RAPL=m
CONFIG_INTEL_RAPL_TPMI=m
CONFIG_IDLE_INJECT=y
CONFIG_MCB=m
CONFIG_MCB_PCI=m
CONFIG_MCB_LPC=m

CONFIG_DWC_PCIE_PMU=m
```

И ещё IT87:
```
CONFIG_GPIO_IT87=m
CONFIG_SENSORS_IT87=m
CONFIG_IT87_WDT=m
```

Ссылки:
* https://github.com/fenrus75/powertop/blob/master/README.md#kernel-parameters-and-optional-patches

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

## Быстрое выключение GUI и другого лишнего на ubuntu
```sh
# Console
sudo systemctl isolate multi-user.target

# GPU
echo 1 > /sys/bus/pci/devices/0000\:00\:02.0/remove
# Audio
echo 1 > /sys/bus/pci/devices/0000\:00\:1f.3/remove
# USB
echo 1 > /sys/bus/pci/devices/0000\:00\:14.0/remove

rmmod i915
rmmod xe
rmmod video
```

* [Is there any way to disable GUI from even loading while starting the machine without uninstalling GUI completely ?](https://www.reddit.com/r/Ubuntu/comments/qy1lbj/is_there_any_way_to_disable_gui_from_even_loading/)

## Hardware
TODO:
* Server anaconda
  * Блок питания: MONTECH GAMMA II 650 [GAMMA II 650]
  * Motherboard: Gigabyte Technology Co., Ltd. B560M DS3H
    * [Manual](https://download.gigabyte.com/FileList/Manual/mb_manual_b560m-ds3h-ac_e_v1.pdf)
    * BIOS:
      * Version: F11
      * Date: 12/19/2023
    * FAN control chip: it8689e
      * https://github.com/frankcrawford/it87
      * https://forum.manjaro.org/t/unable-to-control-fan-on-gigabyte-b560m-ds3h-v2-chip-it8689/99930
      * https://github.com/lm-sensors/lm-sensors/issues/154
      * https://gitlab.com/coolercontrol/coolercontrol
      * Загрузка:
        ```sh
        modprobe it87 force_id=0x8628 ignore_resource_conflict=1
        sensors # it8628-isa-0a40
        ```
      * talos:
        ```sh
        talosctl ls /sys/devices/platform/it87.2624
        ```
  * CPU: 11th Gen Intel(R) Core(TM) i5-11400 @ 2.60GHz
  * RAM:
    * KHX2666C16/8G
    * KHX2666C16/8G
  * NVME:
    * KINGSTON SKC3000S512G - 512 GB
      * https://www.kingston.com/datasheets/KC3000_ru.pdf
      * https://smarthdd.com/database/KINGSTON-SKC3000S512G/
  * SATA:
    * SSD - 256GB RUN S9 256 - 256 GB
      * SSD Digma SATA III 256Gb DGSR1256GS93T
      * https://digma.ru/catalog/it-products/components/ssd/ssd-digma-sata-iii-256gb-dgsr1256gs93t-run-s9-m-2-2280-1800620/
      * https://www.nix.ru/autocatalog/ssd/SSD-256-Gb-M2-2280-B-M-6Gb-s-Digma-RUN-S9-DGSR1256GS93T-3D-TLC-1800620_687471.html
    * HDD - WDC WD10EACS-14Z Green - 1TB
    * TODO: ещё диски
  * KVM: KCEVE KVM401A
  * FAN: TODO - охлаждение башня и просто вентиляторы
  * APC:
    * Model: APC BC650-RS
    * Battery: TODO
  * Умная розетка: Atorch S1-B/W/T/H
    * Link: https://mysku.club/blog/aliexpress/100352.html
    * Android APP: Smart Life - Smart Living
    * https://github.com/rkosegi/tuya-smartplug-exporter
    * id, key смотри в keepassxc
    * https://github.com/Mistikan/tuya-web
* Network:
  * Mikrotik RBD52G-5HacD2HnD
* Etc

## Storage links
* https://smarthdd.com/rus/database/ST4000VN006-3CW104/SC60/
* https://smarthdd.com/rus/database/ST2000DM001-1CH164/
* https://smarthdd.com/rus/database/WDC-WD10EACS-14ZJB0/01.01B01/
* https://smarthdd.com/rus/database/WDC-WD10JPVX-22JC3T0/01.01A01/
* https://smarthdd.com/rus/database/DGSR1256GS93T/W0704A0/

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

### Шифрование файла
1. Создаешь файл с именем `.sops\.ya?ml` (см. конфиг `.sops.yaml`). Например, `secret.sops.yaml`.

1. Вписываешь в него обычный манифест как обычно это делаешь:
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: dotfile-secret
    data:
      .secret-file: dmFsdWUtMg0KDQo=
    ```
1. Непосредственно шифруешь (вставь свой путь):
    ```sh
    sops -e -i /workspaces/hl-cluster/kubernetes/$PATH/secret.sops.yaml
    ```

1. Обнови kustomization: https://fluxcd.io/flux/guides/mozilla-sops/#gitops-workflow
    ```yaml
    ...
    decryption:
      provider: sops
      secretRef:
        name: sops-age # Это секрет, с помощью которого дешифруют, а не который требуется расшифровать
    ...
    ```

1. Сохраняешь под гит.

### Ссылки
* https://fluxcd.io/flux/guides/mozilla-sops/

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
* https://budimanjojo.com/2021/10/27/variable-substitution-in-flux-gitops/ - принцип работы SECRET_DOMAIN
