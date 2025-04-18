import os
import stat
import torrent_parser as tp
from pathlib import Path
import binascii
import hashlib
import logging


ST_MODE=0o666

TORRENT_DIRECTORIES = [
    # "/var/mnt/zfs/wd_green_1tb_pool/torrent",
    # "/var/mnt/zfs/wd_blue_1tb_pool/torrent"
    "/home/user/projects/github/Mistikan/hl-cluster/.venv/torrent"
    ]

INFO_HASHS = []

def validate_file(path: Path, length: int, torrent_files: dict, hash_data_dir: Path):
    path_str = str(path.relative_to(hash_data_dir))
    if torrent_files.get(path_str) is not None:
        torrent_length = torrent_files[path_str]
        if length != torrent_length:
            logging.warning(f"File {path} is bad. Expected: {torrent_length}, facted: {length}")
            return False
        else:
            logging.info(f"File {path} is good!")
    else:
        logging.warning(f"Pls, delete file: {path}")
        return False

    # Проверка, что файл не является ссылкой
    if os.path.islink(path):
        logging.warning(f"Файл '{path}' является символической ссылкой.")
        return False

    # Проверка прав доступа
    # TODO: ещё владельца проверять, что root и группа root
    # TODO: а ещё навесить chattr immutable
    file_stat = os.stat(path)
    if file_stat.st_mode & stat.S_IMODE(file_stat.st_mode) != ST_MODE:
        logging.warning(f"Права доступа к файлу '{path}' не соответствуют {ST_MODE}.")
        logging.warning(f"Исправляем в автоматическом режиме")
        os.chmod(path, ST_MODE)

    return True

def validate_structure(torrent_dir):
    global INFO_HASHS

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

    flag_stop = False
    for torrent_file in torrent_files:
        if flag_stop:
            exit(1)

        logging.info("-----")
        # Filepath
        filepath   = Path(torrent_file)
        logging.info (f"Read {filepath}")
        # Info hash
        data_raw   = tp.parse_torrent_file(filepath, hash_raw=True)
        info_bytes = tp.encode(data_raw["info"])
        info_hash  = binascii.hexlify(hashlib.sha1(info_bytes).digest()).decode()
        if info_hash in INFO_HASHS:
            logging.error("Duplicate hashs!")
            exit(1)
        INFO_HASHS.append(info_hash)
        # Fields torrent
        data       = tp.parse_torrent_file(filepath)
        if "files" in data["info"]:
            torrent_files_tmp = data["info"]["files"]
        else:
            torrent_files_tmp = [
                {
                    "length": data["info"]["length"],
                    "path": [data["info"]["name"]]
                }
            ]

        # Ignore_files
        ignore_files_path = Path(metadata_dir / ".ignore_files" / (info_hash + ".txt"))
        if ignore_files_path.is_file():
          logging.info(f"Read ignore file {ignore_files_path}")
          with open(ignore_files_path) as my_file:
            ignore_files = my_file.read().splitlines()
        else:
          ignore_files = []

        # Convert array to dict
        torrent_files = {}
        for file in torrent_files_tmp:
            path   = "/".join(file["path"])
            length = file["length"]
            torrent_files[path] = length

        # Убираю игнорируемые файлы
        for ignore_file in ignore_files:
          torrent_files.pop(ignore_file)

        # Проверка названия торрент файла на наличие хеша
        filename = info_hash + ".torrent"
        if filename != filepath.name:
            logging.warning(f"Rename file {filepath} => {filename}")
            continue

        # Путь к директории с данными для данного хеша
        hash_data_dir = Path(data_dir, info_hash)

        # Проверка наличия директории с данными
        if not os.path.isdir(hash_data_dir):
            logging.warning(f"Dir '{hash_data_dir}' not found.")
            flag_stop = True
            continue

        hash_data_files = [f for f in hash_data_dir.glob('**/*') if f.is_file()]
        r = {}

        for file in hash_data_files:
            # Получение параметров
            length = file.stat().st_size
            r [str(path)] = length
            # Проверка файла
            res = validate_file(file, length, torrent_files, hash_data_dir)
            # Если файл нашли, то удаляем его из файлов для торрента
            if res:
                file_str = str(file.relative_to(hash_data_dir))
                torrent_files.pop(file_str)
            else:
                flag_stop = True



        # Недостающие файлы
        if len(torrent_files) > 0:
            logging.warning (f"Need files:")
            for need_file in torrent_files:
                print(f"{need_file}")
            flag_stop = True


def main():
    logging.basicConfig(level=logging.INFO)

    for torrent_dir in TORRENT_DIRECTORIES:
        validate_structure(torrent_dir)

if __name__ == "__main__":
    main()
