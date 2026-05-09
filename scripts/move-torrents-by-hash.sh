#!/usr/bin/env bash
# Сканирует директорию, находит .torrent, вычисляет info-hash (SHA-1),
# перемещает файл в целевую директорию как <hash>.torrent
#
# Использование: move_torrents_by_hash.sh <каталог_сканирования> <каталог_назначения>

set -euo pipefail

usage() {
  echo "Использование: $0 <каталог_сканирования> <каталог_назначения>" >&2
  exit 1
}

[[ $# -eq 2 ]] || usage

SCAN_DIR=$(readlink -f -- "$1")
OUT_DIR=$(readlink -f -- "$2")

if [[ ! -d "$SCAN_DIR" ]]; then
  echo "Ошибка: каталог сканирования не найден: $SCAN_DIR" >&2
  exit 1
fi

mkdir -p -- "$OUT_DIR"

torrent_info_hash() {
  local torfile=$1
  TORRENT_PATH="$torfile" python3 - <<'PY'
import hashlib, os, sys

def bdecode(data, i=0):
    c = data[i : i + 1]
    if c == b"i":
        j = data.index(b"e", i + 1)
        return int(data[i + 1 : j]), j + 1
    if c == b"l":
        i += 1
        out = []
        while data[i : i + 1] != b"e":
            v, i = bdecode(data, i)
            out.append(v)
        return out, i + 1
    if c == b"d":
        i += 1
        out = {}
        while data[i : i + 1] != b"e":
            k, i = bdecode(data, i)
            v, i = bdecode(data, i)
            out[k] = v
        return out, i + 1
    j = data.index(b":", i)
    n = int(data[i:j])
    s = data[j + 1 : j + 1 + n]
    return s, j + 1 + n

def bencode(obj):
    if isinstance(obj, int):
        return b"i" + str(obj).encode() + b"e"
    if isinstance(obj, bytes):
        return str(len(obj)).encode() + b":" + obj
    if isinstance(obj, list):
        return b"l" + b"".join(bencode(x) for x in obj) + b"e"
    if isinstance(obj, dict):
        return b"d" + b"".join(bencode(k) + bencode(obj[k]) for k in obj) + b"e"
    raise TypeError(type(obj))

path = os.environ["TORRENT_PATH"]
with open(path, "rb") as f:
    raw = f.read()
root, _ = bdecode(raw)
info = root.get(b"info")
if info is None:
    print("нет ключа info", file=sys.stderr)
    sys.exit(2)
h = hashlib.sha1(bencode(info)).hexdigest()
print(h)
PY
}

while IFS= read -r -d "" f; do
  if ! hash=$(torrent_info_hash "$f"); then
    echo "Пропуск (ошибка разбора): $f" >&2
    continue
  fi
  dest="$OUT_DIR/$hash.torrent"
  if [[ -e "$dest" && "$(readlink -f -- "$dest")" != "$(readlink -f -- "$f")" ]]; then
    echo "Внимание: уже есть $dest — перезапись файла из $f" >&2
  fi
  mv -f -- "$f" "$dest"
  echo "OK: $f -> $dest"
done < <(find "$SCAN_DIR" -type f -name "*.torrent" -print0)
