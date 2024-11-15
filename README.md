# hl-cluster (homelab-cluster)
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
