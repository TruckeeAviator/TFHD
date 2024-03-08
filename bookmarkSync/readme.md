## Google bookmark sync agent
---
This agent runs in the background and looks for changes to the Bookmarks JSON file in AppData on Windows. Some variables will need to be updated like the loaction of backup (documentsFile) and the compareBookmarks function could use some work. It starts by checking if a default bookmark files exists. This will be diffrent for other Orgs.


This is ment to run in the background it can be converted to binary with pyinstaller
`pip install pyinstaller`
`pyinstaller -F bookmarkSync.pyw`
