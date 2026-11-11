
# Workflow step 1: main.py calls this module to turn the input folder into file metadata records.
import os  # Imports operating-system utilities used by this module.
from pathlib import Path  # Imports path utilities for safe cross-platform filesystem access.
from datetime import datetime  # Imports date/time conversion for file modification timestamps.


def scan_directory(folder_path):  # Returns one metadata dictionary per regular file for the classifier to use.
    folder = Path(folder_path).resolve()  # Converts the supplied directory path to an absolute path.
    files = []  # Accumulates records that will be returned to main.py and passed to classify_files().

    if not folder.is_dir():  # Checks that the resolved path identifies an existing directory.
        raise ValueError("Invalid directory")  # Reports invalid input instead of attempting a scan.

    for item in folder.iterdir():  # Visits each immediate entry in the target directory.

        # Ignore folders and symbolic links
        if item.is_file() and not item.is_symlink():  # Selects regular files and excludes symbolic links.

            metadata = item.stat()  # Reads the selected file's filesystem metadata.

            file_info = {  # Builds the input record used by classification and later planning.
                "name": item.name,  # Stores the file's name without its parent directory.
                "extension": item.suffix.lower(),  # Stores its lowercase extension for classification.
                "size": metadata.st_size,  # Stores the file size in bytes.
                "modified": datetime.fromtimestamp(  # Converts the filesystem modification time to local time.
                    metadata.st_mtime  # Supplies the modification timestamp in seconds.
                ).strftime("%Y-%m-%d %H:%M:%S")  # Formats the timestamp as a readable date and time.
            }  # Finishes the metadata record for this file.

            files.append(file_info)  # Adds the file metadata to the scan results.

    return files  # Hands the discovered file records back to main.py as the first workflow result.


if __name__ == "__main__":  # Checks whether this module is being run as a script.
    result = scan_directory("test_files")  # Scans the test_files directory and saves its file metadata.

    for file in result:  # Iterates through each file found by the scan.
        print(file)  # Prints the metadata for the current file.
