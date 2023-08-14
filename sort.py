import os
import sys
import shutil


def normalize(input_str):
    translit_table = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "д": "d",
        "е": "e",
        "є": "ie",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ю": "iu",
        "я": "ia",
    }

    normalized_str = ""
    for char in input_str:
        if char.isalnum() or char in [".", " "]:
            if char in translit_table:
                normalized_str += translit_table[char]
            else:
                normalized_str += char
        else:
            normalized_str += "_"

    return normalized_str


def sort_folder(folder_path):
    extensions = {
        "images": ("JPEG", "PNG", "JPG", "SVG"),
        "video": ("AVI", "MP4", "MOV", "MKV"),
        "documents": ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"),
        "audio": ("MP3", "OGG", "WAV", "AMR"),
        "archives": ("ZIP", "GZ", "TAR"),
    }

    known_extensions = set()
    unknown_extensions = set()

    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_extension = filename.split(".")[-1].upper()
            if file_extension in extensions["images"]:
                category = "images"
            elif file_extension in extensions["video"]:
                category = "video"
            elif file_extension in extensions["documents"]:
                category = "documents"
            elif file_extension in extensions["audio"]:
                category = "audio"
            elif file_extension in extensions["archives"]:
                category = "archives"
                archive_path = os.path.join(root, filename)
                extract_folder = os.path.join(
                    folder_path, "archives", normalize(filename)
                )
                shutil.unpack_archive(archive_path, extract_folder)
                continue
            else:
                category = "unknown"
                unknown_extensions.add(file_extension)

            known_extensions.add(file_extension)

            src_file_path = os.path.join(root, filename)
            dest_folder = os.path.join(folder_path, category)
            dest_file_path = os.path.join(dest_folder, normalize(filename))

            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            shutil.move(src_file_path, dest_file_path)

    return known_extensions, unknown_extensions


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        known_extensions, unknown_extensions = sort_folder(folder_path)

        print("Known extensions:", known_extensions)
        print("Unknown extensions:", unknown_extensions)
