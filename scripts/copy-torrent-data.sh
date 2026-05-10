#!/usr/bin/env bash
set -euo pipefail

# Requires: TORRENT_DST_FOLDER_DATA, TORRENT_DST_FOLDER_METADATA (destination roots).
# Optional: first argument — directory with *.json manifests (default: current directory).

export TORRENT_DST_FOLDER_DATA="/media/zfs/seagate_barracuda_2tb_pool/data/"
export TORRENT_DST_FOLDER_METADATA="/media/zfs/seagate_barracuda_2tb_pool/metadata/"

JSON_DIR="${1:-.}"

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required" >&2
  exit 1
fi

shopt -s nullglob
for json in "$JSON_DIR"/*.json; do
  if jq -e '(.files // {}) | [.[]] | (length > 0 and all(. == null))' "$json" >/dev/null; then
    continue
  fi

  TORRENT_INFO_HASH="$(jq -r '.torrent_info.hash' "$json")"
  if [[ -z "$TORRENT_INFO_HASH" || "$TORRENT_INFO_HASH" == "null" ]]; then
    echo "skip (no torrent_info.hash): $json" >&2
    continue
  fi

  while IFS=$'\t' read -r key src; do
    [[ -z "$key" ]] && continue
    dst="${TORRENT_DST_FOLDER_DATA}/${TORRENT_INFO_HASH}/${key}"
    dest_dir="$(dirname -- "$dst")"
    install -d -m 755 "$dest_dir"
    cp -- "$src" "$dst"
    chmod 444 "$dst"
  done < <(jq -r '(.files // {}) | to_entries[] | select(.value != null) | "\(.key)\t\(.value)"' "$json")

  torrent_src="$(jq -r '.torrent_info.path' "$json")"
  if [[ -z "$torrent_src" || "$torrent_src" == "null" ]]; then
    echo "skip torrent move (no torrent_info.path): $json" >&2
    continue
  fi

  mv -- "$torrent_src" "${TORRENT_DST_FOLDER_METADATA}/${TORRENT_INFO_HASH}.torrent"
  chmod 444 "${TORRENT_DST_FOLDER_METADATA}/${TORRENT_INFO_HASH}.torrent"

  mv -- "$json" "${json}.completed"
done
