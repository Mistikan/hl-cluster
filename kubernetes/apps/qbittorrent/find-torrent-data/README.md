# Наполнение БД
```sh
RUST_LOG=info find-torrent-data search-engine postgresql \
  --input /media/zfs/ \
  --output postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_NAME}?sslmode=prefer \
  --calc-hash none
```
Примечание: повторное заполнение упадёт с ошибкой - надо чистить бд.
Примечание: лучше запускать в screen или аналогичном ПО - чтобы можно было отключиться.
