# hl-cluster (homelab-cluster)
## Hardware
TODO:
* Server anaconda
  * CPU: 11th Gen Intel(R) Core(TM) i5-11400 @ 2.60GHz
  * NVME:
    * KINGSTON SKC3000S512G - 512 GB
  * SATA:
    * SSD - 256GB RUN S9 256 - 256 GB
    * HDD - WDC WD10EACS-14Z Green - 1TB
    * TODO: ещё диски
* Network:
  * Mikrotik RBD52G-5HacD2HnD
* Etc

## ZFS
### Pool
| Pool name | Disk     | Size |
|-----------|----------|------|
| storage   | kingston | 336G |

### OpenEBS
* https://openebs.io/docs/4.0.x/user-guides/local-storage-user-guide/local-pv-zfs/zfs-configuration

## Flux
### Обновить состояние git
```sh
flux reconcile source git home-kubernetes
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
* https://github.com/buroa/k8s-gitops
* https://kubesearch.dev/
