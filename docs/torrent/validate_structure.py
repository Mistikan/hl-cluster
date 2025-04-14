import os
import stat
import torrent_parser as tp
from pathlib import Path
import binascii
import hashlib
import logging


TORRENT_DIRECTORIES = [
    # "/var/mnt/zfs/wd_green_1tb_pool/torrent",
    # "/var/mnt/zfs/wd_blue_1tb_pool/torrent"
    "/home/user/projects/github/Mistikan/hl-cluster/.venv/torrent"
  ]

def validate_structure(torrent_dir):
  # Путь к директориям data и metadata
  data_dir = Path(torrent_dir, 'data')
  metadata_dir = Path(torrent_dir, 'metadata')

  # Проверка наличия директорий data и metadata
  if not os.path.isdir(data_dir):
      print(f"Директория '{data_dir}' не найдена.")
      return
  if not os.path.isdir(metadata_dir):
      print(f"Директория '{metadata_dir}' не найдена.")
      return

  # Получаем список файлов в директории metadata
  torrent_files = [f for f in metadata_dir.iterdir() if f.is_file()]

  for torrent_file in torrent_files:
      # Filepath
      filepath   = Path(torrent_file)
      logging.info (f"Read {filepath}")
      # Info hash
      data_raw   = tp.parse_torrent_file(filepath, hash_raw=True)
      info_bytes = tp.encode(data_raw["info"])
      info_hash  = binascii.hexlify(hashlib.sha1(info_bytes).digest()).decode()
      # Fields torrent
      data       = tp.parse_torrent_file(filepath)
      if "files" in data["info"]:
        files = data["info"]["files"]
      else:
        files = [
          {
            "length": data["info"]["length"],
            "path": [data["info"]["name"]]
          }
        ]

      # Convert array to dict
      torrent_files = {}
      for file in files:
        path   = file["path"][0]
        length = file["length"]
        torrent_files[path] = length
      files = torrent_files

      # Проверка названия файла на наличие хеша
      filename = info_hash + ".torrent"
      if filename != filepath.name:
        logging.warning(f"Rename file {filepath} => {filename}")
        continue

      # Путь к директории с данными для данного хеша
      hash_data_dir = Path(data_dir, info_hash)

      # Проверка наличия директории с данными
      if not os.path.isdir(hash_data_dir):
          print(f"Dir '{hash_data_dir}' not found.")
          continue

      for file in files:
        print(f"{file}")

      hash_data_files = [f for f in hash_data_dir.iterdir() if f.is_file()]
      r = dict()
      for file in hash_data_files:
        length = file.stat().st_size
        path = file.relative_to(hash_data_dir)
        r [str(path)] = length

      hash_data_files = r

      # Лишние файлы
      extra_files  = set(hash_data_files) - set(files)
      # Недостающие файлы
      need_files = set(files) - set(hash_data_files)

      print (f"Need: {need_files}")
      print (f"Extra: {extra_files}")
      # TODO: здесь может быть ситуация, что файл присутствует, но другого размера

      # Получаем список файлов в директории с данными
      data_files = os.listdir(hash_data_dir)

      # Проверка наличия посторонних файлов
      if len(data_files) == 0:
          print(f"Директория '{hash_data_dir}' пуста.")
          continue

      # Чтение содержимого .torrent файла (здесь можно добавить логику для чтения содержимого)
      # Для примера, предположим, что в torrent файле указаны имена файлов
      # В реальной ситуации нужно использовать библиотеку для работы с .torrent файлами

      # Примерный список файлов из .torrent файла
      # В реальной ситуации нужно извлекать имена файлов из .torrent файла
      expected_files = ['file.mkv', 'file.txt']  # Замените на реальный список

      for expected_file in expected_files:
          expected_file_path = os.path.join(hash_data_dir, expected_file)

          # Проверка наличия файла
          if not os.path.isfile(expected_file_path):
              print(f"Файл '{expected_file_path}' не найден.")
              continue

          # Проверка размера файла
          # Здесь можно добавить логику для проверки размера, если известен ожидаемый размер
          # expected_size = ...  # Замените на реальный размер
          # if os.path.getsize(expected_file_path) != expected_size:
          #     print(f"Размер файла '{expected_file_path}' не соответствует ожидаемому.")

          # Проверка прав доступа
          # TODO: ещё владельца проверять, что root и группа root
          file_stat = os.stat(expected_file_path)
          if file_stat.st_mode & stat.S_IMODE(file_stat.st_mode) != 0o664:
              print(f"Права доступа к файлу '{expected_file_path}' не соответствуют 664.")

          # Проверка, что файл не является ссылкой
          if os.path.islink(expected_file_path):
              print(f"Файл '{expected_file_path}' является символической ссылкой.")

      # Проверка на наличие посторонних файлов
      for file in data_files:
          if file not in expected_files:
              print(f"Посторонний файл '{file}' найден в директории '{hash_data_dir}'.")

def main():
  logging.basicConfig(level=logging.INFO)

  for torrent_dir in TORRENT_DIRECTORIES:
    validate_structure(torrent_dir)

if __name__ == "__main__":
  main()
