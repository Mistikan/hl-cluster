# Наполнение БД
```sh
kubectl exec -ti deployment/find-torrent-data -- /bin/bash

RUST_LOG=info find-torrent-data search-engine postgresql \
  --input /media/zfs/ \
  --output postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_NAME}?sslmode=prefer \
  --calc-hash none
```
Примечание: повторное заполнение упадёт с ошибкой - надо чистить бд.
Примечание: лучше запускать в screen или аналогичном ПО - чтобы можно было отключиться.

# Очистка БД
```sh
kubectl -n qbittorrent exec -ti postgresql-qbittorrent-0 -- /bin/bash
su - postgres
psql -d qbittorrent -c "TRUNCATE TABLE file_info;"
```

# Составление отчета
```sh
export REPORT_DIR="/media/zfs/seagate_barracuda_2tb_pool/report"
export REPORT_DIR_LOG="/media/zfs/seagate_barracuda_2tb_pool/report-log"
export TORRENT_FILE="/media/zfs/seagate_barracuda_2tb_pool/metadata-all/00dd21b06b2f8cc615c930e8043e000c0d4424c1.torrent"
export INFO_HASH="00dd21b06b2f8cc615c930e8043e000c0d4424c1"
RUST_LOG=info find-torrent-data torrent \
  --torrent "${TORRENT_FILE}" \
  --search-engine-type "postgresql" \
  --search-engine-settings postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_NAME}?sslmode=prefer \
  --output "$REPORT_DIR/$INFO_HASH.json" 2>&1 | tee -a $REPORT_DIR_LOG/$INFO_HASH.log
```
