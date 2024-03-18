import os
import subprocess
import shutil
import time
import msvcrt
import ctypes
import atexit
from datetime import datetime

# Determine current user
def whoAmI():
    user = subprocess.check_output('whoami')
    user = user.decode("utf-8")
    user = user.replace('<domain>\\', '')
    user = user.replace('\n', '')
    user = user.strip()
    return user

LOCK_FILE_PATH = '\\\\<server path>\\{}\\My Documents\\BookmarkSync\\Bookmarks.lock'
HIDDEN_ATTRIBUTE = 0x02
BACKUP_COUNT = 5
backup_performed = False

def acquireLock(username):
    lockFilePath = LOCK_FILE_PATH.format(username)
    
    # Create 'BookmarkSync' folder if it doesn't exist
    bookmarkSyncPath = os.path.dirname(lockFilePath)
    if not os.path.exists(bookmarkSyncPath):
        os.makedirs(bookmarkSyncPath)

    lockFile = open(lockFilePath, "w")
    msvcrt.locking(lockFile.fileno(), msvcrt.LK_LOCK, 1)
    return lockFile

def releaseLock(lockFile):
    lockFilePath = lockFile.name
    msvcrt.locking(lockFile.fileno(), msvcrt.LK_UNLCK, 1)
    lockFile.close()
    os.remove(lockFilePath)

def waitForUnlock(username):
    lockFilePath = LOCK_FILE_PATH.format(username)
    while os.path.exists(lockFilePath):
        time.sleep(1)

def setHiddenAttribute(folderPath):
    try:
        # Set the 'Hidden' attribute for the folder
        ctypes.windll.kernel32.SetFileAttributesW(folderPath, 0x02)
    except Exception as e:
        print(f"Error setting hidden attribute: {e}")

def backupAndPreSaveActions(username, appDataFile, documentsFile, edgeDataFile):
    global backup_performed

    # Check if backup has already been performed
    if backup_performed:
        print("Backup already performed. Skipping.")
        return

    # Check if the 'BookmarkSync' folder exists in 'My Documents'
    documentsPath = '\\\\<server path>\\{}\\My Documents\\'.format(username)
    bookmarkSyncPath = os.path.join(documentsPath, 'BookmarkSync')

    if not os.path.exists(bookmarkSyncPath):
        os.makedirs(bookmarkSyncPath)

    # Set the 'Hidden' attribute for the 'BookmarkSync' folder
    setHiddenAttribute(bookmarkSyncPath)

    # Create a backup of 'appDataFile' with a timestamp (Chrome)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    appdataBackupFilename = f"Bookmarks-Chrome_{timestamp}.bak"
    appdataBackupPath = os.path.join(bookmarkSyncPath, appdataBackupFilename)

    if os.path.exists(appDataFile):
        shutil.copy(appDataFile, appdataBackupPath)

    # Create a backup of 'documentsFile' with a timestamp (Chrome)
    documentsBackupFilename = f"Documents-Chrome_{timestamp}.bak"
    documentsBackupPath = os.path.join(bookmarkSyncPath, documentsBackupFilename)

    if os.path.exists(documentsFile):
        shutil.copy(documentsFile, documentsBackupPath)

    # Create a backup of 'edgeDataFile' with a timestamp (Edge)
    edgeBackupFilename = f"Bookmarks-Edge_{timestamp}.bak"
    edgeBackupPath = os.path.join(bookmarkSyncPath, edgeBackupFilename)

    if os.path.exists(edgeDataFile):
        shutil.copy(edgeDataFile, edgeBackupPath)

    # Manage the number of backups, keep the most recent 5 for each type
    appdataBackups = sorted(
        [f for f in os.listdir(bookmarkSyncPath) if f.startswith("Bookmarks-Chrome_")],
        key=lambda x: os.path.getctime(os.path.join(bookmarkSyncPath, x)),
        reverse=True
    )

    documentsBackups = sorted(
        [f for f in os.listdir(bookmarkSyncPath) if f.startswith("Documents-Chrome_")],
        key=lambda x: os.path.getctime(os.path.join(bookmarkSyncPath, x)),
        reverse=True
    )

    edgeBackups = sorted(
        [f for f in os.listdir(bookmarkSyncPath) if f.startswith("Bookmarks-Edge_")],
        key=lambda x: os.path.getctime(os.path.join(bookmarkSyncPath, x)),
        reverse=True
    )

    for backups, backupType in zip([appdataBackups, documentsBackups, edgeBackups],
                                    ['Bookmarks-Chrome', 'Documents-Chrome', 'Bookmarks-Edge']):
        if len(backups) > BACKUP_COUNT:
            for oldBackup in backups[BACKUP_COUNT:]:
                oldBackupPath = os.path.join(bookmarkSyncPath, oldBackup)
                os.remove(oldBackupPath)

    # Mark backup as done
    backup_performed = True

def compareBookmarks(src, dst):
    srcSize = os.path.getsize(src)
    dstSize = os.path.getsize(dst)

    if srcSize == 5223:
        return 2
    elif srcSize == dstSize:
        return 1
    elif srcSize != dstSize:
        return 0

def syncBookmarks(src, dst):
    shutil.copy(src, dst)

def main(username):
    # Check if the lock file exists and attempt to acquire the lock
    lockFilePath = LOCK_FILE_PATH.format(username)
    if os.path.exists(lockFilePath):
        print("Lock file exists. Checking for stale lock.")
        try:
            lockFile = acquireLock(username)
        except IOError:
            print("Stale lock detected. Proceeding.")
            os.remove(lockFilePath)
    else:
        # Acquire the lock if it doesn't exist
        lockFile = acquireLock(username)

    # Register the release_lock function to be called on program exit
    atexit.register(releaseLock, lockFile)

    try:
        # Set paths
        chromeAppDataPath = os.path.join('C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default'.format(username))
        chromeAppDataFile = os.path.join(chromeAppDataPath, 'Bookmarks')
        chromeDocumentsFile = '\\\\<server path>\\{}\\My Documents\\Bookmarks'.format(username)

        edgeAppDataPath = os.path.join('C:\\Users\\{}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default'.format(username))
        edgeAppDataFile = os.path.join(edgeAppDataPath, 'Bookmarks')

        backupAndPreSaveActions(username, chromeAppDataFile, chromeDocumentsFile, edgeAppDataFile)

        # Run the program indefinitely
        while True:
            # Logic check for Chrome bookmarks
            if not os.path.exists(chromeAppDataFile) and os.path.exists(chromeDocumentsFile):
                os.makedirs(chromeAppDataPath)
                syncBookmarks(src=chromeDocumentsFile, dst=chromeAppDataFile)
                print("Creating dir and copying to Chrome appdata")

            elif os.path.exists(chromeAppDataFile) and not os.path.exists(chromeDocumentsFile):
                syncBookmarks(chromeAppDataFile, chromeDocumentsFile)

            elif os.path.exists(chromeAppDataFile) and os.path.exists(chromeDocumentsFile):
                syncBookmarks(src=chromeDocumentsFile, dst=chromeAppDataFile)

                result = compareBookmarks(src=chromeAppDataFile, dst=chromeDocumentsFile)
                handleBookmarkSyncResult(result, chromeAppDataFile, chromeDocumentsFile)

            # Logic check for Edge bookmarks
            if not os.path.exists(edgeAppDataFile) and os.path.exists(chromeDocumentsFile) and not os.path.exists(edgeAppDataPath):
                os.makedirs(edgeAppDataPath)
                syncBookmarks(src=chromeDocumentsFile, dst=edgeAppDataFile)
                print("Creating dir and copying to Edge appdata")

            elif not os.path.exists(edgeAppDataFile) and os.path.exists(chromeDocumentsFile) and os.path.exists(edgeAppDataPath):
                syncBookmarks(src=chromeDocumentsFile, dst=edgeAppDataFile)

            elif os.path.exists(edgeAppDataFile) and not os.path.exists(chromeDocumentsFile):
                syncBookmarks(edgeAppDataFile, chromeDocumentsFile)

            elif os.path.exists(edgeAppDataFile) and os.path.exists(chromeDocumentsFile):
                syncBookmarks(src=chromeDocumentsFile, dst=edgeAppDataFile)

                result = compareBookmarks(src=edgeAppDataFile, dst=chromeDocumentsFile)
                handleBookmarkSyncResult(result, edgeAppDataFile, chromeDocumentsFile)

            # Wait for a short time before checking again
            time.sleep(5)

    finally:
        quit()

def handleBookmarkSyncResult(result, src, dst):
    # If bookmarks have been updated in appdata, save to documents
    if result == 0:
        syncBookmarks(src, dst)
        print("Saved to documents")

    # If files are the same, do nothing
    elif result == 1:
        print('Same file, do nothing')

    # If the default bookmark exists, save user's bookmarks
    elif result == 2:
        syncBookmarks(src, dst)
        print("Bookmarks synced to documents")

    # If the bookmarks have been updated in documents sync to appdata
    elif result == 3:
        syncBookmarks(src=dst, dst=src)
        print("Synced to appdata")

if __name__ == "__main__":
    # Set current user
    username = whoAmI()

    # Wait for the lock to be released before continuing
    waitForUnlock(username)

    # Start the main program
    main(username)
