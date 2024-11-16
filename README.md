# hl-cluster (homelab-cluster)
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
