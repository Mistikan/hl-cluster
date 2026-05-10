#!/usr/bin/env bash
set -euo pipefail

readonly METADATA_DIR="/media/zfs/seagate_barracuda_2tb_pool/metadata-all"
export REPORT_DIR="/media/zfs/seagate_barracuda_2tb_pool/report"
export REPORT_DIR_LOG="/media/zfs/seagate_barracuda_2tb_pool/report-log"

mkdir -p "$REPORT_DIR" "$REPORT_DIR_LOG"

shopt -s nullglob
for TORRENT_FILE in "$METADATA_DIR"/*.torrent; do
  INFO_HASH="$(basename "$TORRENT_FILE" .torrent)"
  export TORRENT_FILE
  export INFO_HASH

  if [[ -f "$REPORT_DIR/$INFO_HASH.json" ]]; then
    echo "skip: report exists — $INFO_HASH"
    continue
  fi

  echo "process: $INFO_HASH"
  RUST_LOG=info find-torrent-data torrent \
    --torrent "${TORRENT_FILE}" \
    --search-engine-type "postgresql" \
    --search-engine-settings "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_NAME}?sslmode=prefer" \
    --output "$REPORT_DIR/$INFO_HASH.json" 2>&1 | tee -a "$REPORT_DIR_LOG/$INFO_HASH.log"
  ec="${PIPESTATUS[0]}"
  if [[ "$ec" -ne 0 ]]; then
    echo "error: find-torrent-data exited $ec — $INFO_HASH" >&2
    exit "$ec"
  fi
done
