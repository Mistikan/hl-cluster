# Генерация dummy.rom
```bash
sudo mkdir -p /usr/share/vgabios
sudo dd if=/dev/zero of=/usr/share/vgabios/dummy.rom bs=1K count=64
sudo chmod 644 /usr/share/vgabios/dummy.rom
```

# Мой комментарий
https://habr.com/ru/articles/794568/comments/#comment_28550510

# Покдлючение
```xml
<rom bar="on" file="/usr/share/vgabios/nv33.rom"/>
```
