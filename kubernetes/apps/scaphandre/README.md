# TODO
Т.к. хелм репозитория нет, то сгенерерировал через helm-template и запушил вот так.

# Инфо
По стандарту POWERCAP выключен:
```sh
talosctl read /proc/config.gz | zcat | grep CONFIG_POWERCAP
```

# Links
* https://hubblo-org.github.io/scaphandre-documentation/tutorials/kubernetes.html
