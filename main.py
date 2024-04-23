import os
import shutil
import re
from eyed3 import id3


def sanitize_string(input_string):
    # Remove invalid characters for folder names
    invalid_characters = r'[\/:*?"<>|.]'
    return re.sub(invalid_characters, '', input_string)


def organize_music_library(source_folder, destination_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                audiofile = id3.Tag()
                audiofile.parse(file_path)

                # Extract artist and album information from metadata
                artist = audiofile.artist
                album = audiofile.album

                # Sanitize artist and album names
                artist = sanitize_string(artist)
                album = sanitize_string(album)

                # Create destination folders if they don't exist
                artist_folder = os.path.join(destination_folder, artist)
                album_folder = os.path.join(artist_folder, album)
                os.makedirs(album_folder, exist_ok=True)

                # Move the file to the organized structure
                destination_path = os.path.join(album_folder, file)
                shutil.move(file_path, destination_path)

                print(f"Moved: {file} -> {destination_path}")


def main():
    source_folder = "_input_music"
    destination_folder = "_local_output_music"

    organize_music_library(source_folder, destination_folder)


if __name__ == "__main__":
    main()
