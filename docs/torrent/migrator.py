import torrent_parser as tp
from pathlib import Path
import binascii
import hashlib
import shutil


TORRENT_SOURCE_FILEPATH    = "torrents/[Bitsearch.to]04.Grand.Theft.Auto.Vice.City.v1.0.Multi5.EN.Steam-Rip.by.R.G.Origins.torrent"
# TORRENT_SOURCE_FILEPATH    = "torrents/[Bitsearch.to]Blade Runner.1982.720p.BluRay.x264-LEONARDO_[scarabey.org].mkv.torrent"
TORRENT_SOURCE_DATA_FOLDER = "./files"
TORRENT_METADATA_FOLDER    = "./exp/metadata"
TORRENT_DATA_FOLDER        = "./exp/data"
# Данная директория нужна, чтобы после всех работать убедиться что всё ок и вручную удалить файлы через rm -rf
TORRENT_TEMP_FOLDER        = "./exp/temp"

def get_torrent_info(filepath: Path):
    # Info hash
    data_raw   = tp.parse_torrent_file(filepath, hash_raw=True)
    info_bytes = tp.encode(data_raw["info"])
    info_hash  = binascii.hexlify(hashlib.sha1(info_bytes).digest()).decode()

    # Fields torrent
    data  = tp.parse_torrent_file(filepath)
    # Торрент с одним файлом или несколькими
    if "files" in data["info"]:
        files = data["info"]["files"]
    else:
        files = [
            {
                "length": data["info"]["length"],
                "path": [
                    data["info"]["name"]
                ],
            }
        ]

    return info_hash, files

def torrent_file_search(file, data_files):
    # print (file)

    # By size
    data_files_size = [x for x in data_files if x["length"] == file["length"]]
    if len(data_files_size) == 0:
        print (f"Not found file by size {file}")
        return {}

    # By name
    len_filepath = len(file["path"])
    # Сравнение только по имени
    ## data_files_name = [x for x in data_files_size if file["path"][-1] in x["path"].name]
    # Сравнение полного пути
    data_files_name = [x for x in data_files_size if file["path"] == list(x["path"].parts[-len_filepath:])]
    if len(data_files_name) == 0:
        print (f"Not found file by name {file}")
        return {}

    if len(data_files_name) > 1:
        print (f"Multiple file: {file}")
        print (f"Searched files: {data_files_name}")
        exit(1)

    return data_files_name[0]

def torrent_migrator(src_filepath_torrent: str, torrent_source_data_folder: str, data_files):
    # Filepath
    src_filepath_torrent = Path(src_filepath_torrent)
    directory = Path(torrent_source_data_folder)
    info_hash, files = get_torrent_info(src_filepath_torrent)

    # Paths
    dst_filepath_torrent     = Path(f"{TORRENT_METADATA_FOLDER}/{info_hash}.torrent")
    dst_filepath_data        = Path(f"{TORRENT_DATA_FOLDER}/{info_hash}/")
    tmp_dst_filepath_torrent = Path(f"{TORRENT_TEMP_FOLDER}/metadata/{info_hash}.torrent")
    tmp_dst_filepath_data    = Path(f"{TORRENT_TEMP_FOLDER}/data/{info_hash}/")

    # Copy files
    copy_files = [{
        "src": src_filepath_torrent,
        "dst": dst_filepath_torrent,
        "tmp_dst": tmp_dst_filepath_torrent
    }]

    # Search
    for file in files:
        file_src = torrent_file_search(file, data_files)
        if file_src != {}:
            file_dst = Path(str(dst_filepath_data) + "/" + '/'.join(file['path']))
            tmp_file_dst = Path(str(tmp_dst_filepath_data) + "/" + '/'.join(file['path']))
            # print (f"{file_src['path']} -> {file_dst}")
            copy_files.append({
                "src": Path(file_src['path']),
                "dst": Path(file_dst),
                "tmp_dst": Path(tmp_file_dst)
            })
        else:
            print (f"Not found file for file: {file}")

    # print (f"{src_filepath_torrent} -> {dst_filepath_torrent}")
    # print (f"{dst_filepath_data}")

    return copy_files


def get_data_files():
    p = Path(TORRENT_SOURCE_DATA_FOLDER).glob('**/*')
    files = [
        {
          'length': x.stat().st_size,
          'path': x
        }
        for x in p if x.is_file()
    ]
    return files

def main():
    data_files = get_data_files()
    copy_files = torrent_migrator(TORRENT_SOURCE_FILEPATH, TORRENT_SOURCE_DATA_FOLDER, data_files)

    print ("COPY FILES:")
    for file in copy_files:
        print (str(file["src"]) + " → " + str(file["dst"]))

    answer = input("Continue copy?")
    if answer.lower() in ["y","yes"]:
        print ("Copy files")
        for file in copy_files:
            # Создаем директории
            file["dst"].parent.mkdir(parents = True, exist_ok =True)
            # Копируем
            shutil.copy(file["src"], file["dst"])
    elif answer.lower() in ["n","no"]:
        print ("Good bye.")
        exit (0)
    else:
        print ("Error input.")
        exit (1)

    print ("MOVE FILES:")
    for file in copy_files:
        print (str(file["src"]) + " → " + str(file["tmp_dst"]))

    answer = input("Continue move?")
    if answer.lower() in ["y","yes"]:
        print ("Move files")
        for file in copy_files:
            # Создаем директории
            file["tmp_dst"].parent.mkdir(parents = True, exist_ok =True)
            # Перемещаем
            shutil.move(file["src"], file["tmp_dst"])
    elif answer.lower() in ["n","no"]:
        print ("Good bye.")
        exit (0)
    else:
        print ("Error input.")
        exit (1)

if __name__ == "__main__":
    main()
