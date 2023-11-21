import shutil
import logging
import os

logging.basicConfig(level=logging.INFO)
logging.getLogger('pytube').setLevel(logging.INFO)

MUSIC_FOLDER = "./music_folder"


def check_available_disk():
    """
    This function checks for the available disk space,
    if disk space is less than 30 GB, remove the oldest files in the directory
    """

    # Get disk info
    total, used, free = shutil.disk_usage(MUSIC_FOLDER)

    logging.debug("Total: %d GiB" % (total // (2**30)))
    logging.debug("Used: %d GiB" % (used // (2**30)))
    logging.debug("Free: %d GiB" % (free // (2**30)))

    # Get free space available:
    free_space_available = (free // (2**30))

    # Delete Files if there are less than 30 GB available
    if (free_space_available < 30):
        logging.info("Deleting files to free up space")
        delete_old_files(MUSIC_FOLDER)
    else:
        logging.debug("✅ Space check OK")


def delete_old_files(directory_path, num_to_keep=50):
    """
    This function removes the oldest files in the directory,
    and leaves only a maximum of 50 files remaining

    :param directory_path: Directory to check the space
    :type directory_path: str

    :param num_to_keep: Number of files to keep
    :type num_to_keep: int
    """

    # Get a list of all files in the directory
    all_files = os.listdir(directory_path)

    # Sort the files by modification time (oldest first)
    all_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))

    # Get the list of files to delete
    files_to_delete = all_files[:-num_to_keep]

    # Delete the files
    for file_name in files_to_delete:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")


if __name__ == "__main__":
    check_available_disk()
