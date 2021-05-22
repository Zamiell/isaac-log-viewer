# Imports
import os
import sys
import time

# Constants
LOG_FILE_PATH = (
    "C:\\Users\\james\\Documents\\My Games\\Binding of Isaac Repentance\\log.txt"
)

# From: https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Variables
log_file_handle = None
cached_length = 0


def main():
    while True:
        file_size = os.path.getsize(LOG_FILE_PATH)
        if has_log_changed(file_size):
            read_log(file_size)
        time.sleep(0.1)


def has_log_changed(file_size: int):
    return file_size != cached_length


def read_log(file_size: int):
    global log_file_handle
    global cached_length

    if log_file_handle is None or cached_length > file_size:
        # This is a new log file
        log_file_handle = open(LOG_FILE_PATH, "rb")
    elif cached_length < file_size:
        # Append existing content
        log_file_handle.seek(cached_length)

    cached_length = file_size
    new_log_content = log_file_handle.read()
    parse_log(new_log_content)


def parse_log(log_content: str):
    for line in log_content.splitlines():
        parse_log_line(line)


def parse_log_line(line_bytes: str):
    # We read the log in binary form, so we need to convert it to a normal string
    line = line_bytes.decode("utf-8").strip()

    # Don't print empty lines
    if line == "":
        return

    lowercase_line = line.lower()

    # Don't print some specific messages
    if lowercase_line.startswith("[info] - [warn] sound") and lowercase_line.endswith(
        "has no samples."
    ):
        return
    if lowercase_line.startswith("[info] - lua mem usage: "):
        return
    if (
        lowercase_line
        == "[info] - [warn] steamcloud is either not available or disabled in options.ini."
    ):
        return

    # Print all warnings and errors
    if "warn" in lowercase_line or "error" in lowercase_line:
        printf(line)
        return

    # Print lines that have to do with Lua
    if "lua" in lowercase_line:
        printf(line)
        return


def printf(msg: str):
    lowercase_msg = msg.lower()
    if "error" in lowercase_msg or "failed" in lowercase_msg:
        msg = f"{bcolors.FAIL}{msg}{bcolors.ENDC}"
    elif "warn" in lowercase_msg:
        msg = f"{bcolors.WARNING}{msg}{bcolors.ENDC}"

    print(msg, flush=True)


if __name__ == "__main__":
    main()
