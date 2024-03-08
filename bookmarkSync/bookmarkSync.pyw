import os, subprocess, shutil, time

#Determine current user
def whoAmI():
    user = subprocess.check_output('whoami')
    user = user.decode("utf-8")
    user = user.replace('<domain>\\', '')
    user = user.replace('\n', '')
    return user

#do the files and folders exist
def testPath(path):

    return os.path.exists(path)

#compare the bookmarkfiles
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


#Set current user
username = whoAmI()

#set paths
appDataPath = os.path.join('C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default'.format(username.strip()))

appDataFile = os.path.join('C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks'.format(username.strip()))
documentsFile = os.path.join('\\\\<server backup location>\\Userstore\\{}\\My Documents\\Bookmarks'.format(username.strip()))


#Logic check - see if this is a first time login to new system, if so sync bookmarks
if testPath(appDataFile) == False and testPath(documentsFile) == True:
    os.makedirs(appDataPath)
    syncBookmarks(src=documentsFile, dst=appDataFile)
    print("creating dir, and copying to appdata")

#If the bookmarks have never been backed up, backup
elif testPath(appDataFile) == True and testPath(documentsFile) == False:
    syncBookmarks(appDataFile, documentsFile)

elif testPath(appDataFile) == True and testPath(documentsFile) == True:
    syncBookmarks(src=documentsFile, dst=appDataFile)
    
while True:
    #if bookmark exsits for user and appdata compare
    if testPath(appDataFile) == True and testPath(documentsFile) == True:

        match compareBookmarks(src=appDataFile, dst=documentsFile):

            #If boookmarks have been updated in appdata, save to documnets
            case 0:
                syncBookmarks(appDataFile, documentsFile)

            #If files are the same, do nothing
            case 1:

            #If the default bookmark exist save users bookmarks
            case 2:
                syncBookmarks(src=appDataFile, dst=documentsFile)

            #If the bookmarks have been updated in documents sync to appdata
            case 3:
                syncBookmarks(src=documentsFile, dst=appDataFile)

    #New user new computer
    elif testPath(appDataFile) == True and testPath(documentsFile) == False:
        syncBookmarks(src=appDataFile, dst=documentsFile)

    time.sleep(5)
