import os

css = '''<style>
	body {
		text-align: center;
	}
	
	table {
		margin: 0 auto;
  		border: 1px solid black;
		padding: 2px;
	}

	td, th {
  		border-right: 1px solid black;
		border-left: 1px solid black;
  		border-top: 1px solid black;
  		border-bottom: 1px solid black;
		padding: 5px;
	}
</style>

'''

head = '''
<html>
<body>

<h2>PAF Archive File</h2>
<br>

<table>

<tr>
'''

path = '.\\converted\\'

def findInString(content, startVar, endVar):
    Start = content.find(startVar) + len(startVar)
    End = content.find(endVar)
    outputContent = content[Start:End]
    #Error checks
    outputContent = outputContent.replace('\"', '')
    if len(outputContent) > 1500:
       return None
    return outputContent

def XMLtoHTML(fileNames):
    
    xmlContent = open(fileNames, "r", errors='ignore')

    htmlEdit = xmlContent.read()
    #Removed Full XML Data for internet upload. These two lines would need to be changed anyway
    htmlEdit = htmlEdit.replace('<?xml version="1.0" encoding="UTF-8"?><?mso-infoPathSolution productVersion="15.0.0" PIVersion="1.0.0.0" href="http://127.0.0.1/sites/hr/paf/askdlfjasgnadkkashdfngh/Forms/template.xsn" name="urn:schemas-microsoft-com:office:infopath:PAFNew:-myXSD-2011-03-08T21-31-14" solutionVersion="1.0.0.334" ?><?mso-application progid="InfoPath.Document"?><my:myFields xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dfs="http://schemas.microsoft.com/office/infopath/2003/dataFormSolution" xmlns:my="http://schemas.microsoft.com/office/infopath/2003/myXSD/2011-03-08T21:31:14" xmlns:xd="http://schemas.microsoft.com/office/infopath/2003" xml:lang="en-us">', '')
    htmlEdit = htmlEdit.replace('<?xml version="1.0" encoding="UTF-8"?><?mso-infoPathSolution solutionVersion="1.0.0.344" productVersion="15.0.0" PIVersion="1.0.0.0" href="http://127.0.0.1/sites/hr/paf/askdlfjasgnadkkashdfngh/Forms/template.xsn" name="urn:schemas-microsoft-com:office:infopath:PAFNew:-myXSD-2011-03-08T21-31-14" ?><?mso-application progid="InfoPath.Document"?><my:myFields xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dfs="http://schemas.microsoft.com/office/infopath/2003/dataFormSolution" xmlns:my="http://schemas.microsoft.com/office/infopath/2003/myXSD/2011-03-08T21:31:14" xmlns:xd="http://schemas.microsoft.com/office/infopath/2003" xml:lang="en-us">', '')
    htmlEdit = htmlEdit.replace('my:', '')

    #Move Variables around the XML file, I think this can be a class for OOP
    shiftLFromContent = findInString(htmlEdit, '<ShiftLgthFrom>', '</ShiftLgthFrom>')
    shiftLToContent = findInString(htmlEdit, '<shiftlgthTo>', '</shiftlgthTo>')
    exemptFrmContent = findInString(htmlEdit, '<exemptFrm>', '</exemptFrm>')
    exemptToContent = findInString(htmlEdit, '<exemptTo>', '</exemptTo>')
    reasonForActionNum = findInString(htmlEdit, '<Reason1>', '</Reason1>')
    reasonForActionNumv2 = findInString(htmlEdit, '<reason>', '</reason>')
    submitDateContent = findInString(htmlEdit, '<SubmitDate>', '</SubmitDate>')
    saleryOtherReasonContent = findInString(htmlEdit, '<OtherReason>', '</OtherReason>')
    submittedByContent = findInString(htmlEdit, '<SubmittedBy>', '</SubmittedBy>')
    jobTitleFromContent = findInString(htmlEdit, '<JobTitleFrom>', '</JobTitleFrom>')
    jobTitleToContent = findInString(htmlEdit, '<JobTitleTo>', '</JobTitleTo>')
    deptFromContent = findInString(htmlEdit, '<DeptFrom>', '</DeptFrom>')
    deptToContent = findInString(htmlEdit, '<DeptTo>', '</DeptTo>')
    PCFromContent = findInString(htmlEdit, '<PCFrom>', '</PCFrom>')
    PCToContent = findInString(htmlEdit, '<PCTo>', '</PCTo>')
    rateFromContent = findInString(htmlEdit, '<RateFrom>', '</RateFrom>')
    rateToContent = findInString(htmlEdit, '<RateTo>', '</RateTo>')
    ratePerFromContent = findInString(htmlEdit, '<RatePerFrom>', '</RatePerFrom>')
    ratePerToContent = findInString(htmlEdit, '<RatePerTo>', '</RatePerTo>')
    statusFromContent = findInString(htmlEdit, '<StatusFrom>', '</StatusFrom>')
    statusToContent = findInString(htmlEdit, '<StatusTo>', '</StatusTo>')
    shiftTypeFromContent = findInString(htmlEdit, '<ShiftTypeFrom>', '</ShiftTypeFrom>')
    shiftTypeToContent = findInString(htmlEdit, '<ShiftTypeTo>', '</ShiftTypeTo>')
    benGrpFromContent = findInString(htmlEdit, '<BenGrpFrom>', '</BenGrpFrom>')
    benGrpToContent = findInString(htmlEdit, '<BenGrpTo>', '</BenGrpTo>')
    commentsContent = findInString(htmlEdit, '<comments>', '</comments>')
    termReasonContent = findInString(htmlEdit, '<termReason>', '</termReason>')
    rehireContent = findInString(htmlEdit, '<rehire>', '</rehire>')
    termCommentsContent = findInString(htmlEdit, '<termcomments>', '</termcomments>')
    directorContent = findInString(htmlEdit, '<director>', '</director>')
    ACContent = findInString(htmlEdit, '<AC>', '</AC>')
    directorApprovalContent = findInString(htmlEdit, '<DirectorApproval>', '</DirectorApproval>')
    ACApprovalContent = findInString(htmlEdit, '<ACApproval>', '</ACApproval>')
    rejectCommentsContent = findInString(htmlEdit, '<rejectcomments>', '</rejectcomments>')
    procDateContent = findInString(htmlEdit, '<procDate>', '</procDate>')
    HRStaffContent = findInString(htmlEdit, '<HRStaff>', '</HRStaff>')
    ADPContent = findInString(htmlEdit, '<adp>', '</adp>')
    notifiedContent = findInString(htmlEdit, '<Notified>', '</Notified>')
    volReasonContent = findInString(htmlEdit, '<volReason>', '</volReason>')
    inVolReasonContent = findInString(htmlEdit, '<inVolReason>', '</inVolReason>')

    #Globals for naming file
    global eeLastNameContent
    global eeFirstNameContent
    global effDateContent
    eeLastNameContent = findInString(htmlEdit, '<eeLastName>', '</eeLastName>')
    eeFirstNameContent = findInString(htmlEdit, '<eefirstname>', '</eefirstname>')
    effDateContent = findInString(htmlEdit, '<effdate>', '</effdate>')

    #Reason number to string
    match reasonForActionNum or reasonForActionNumv2:
        case "1":
          reasonForAction = 'New Hire'
        case "2":
          reasonForAction = 'Transfer'
        case "3":
          reasonForAction = 'Promotion'
        case "4":
          reasonForAction = 'Salary Adjustment'
        case "5":
          reasonForAction = 'Termination'
        case "6":
          reasonForAction = 'Other'
        case _:
          if reasonForActionNum == None:
             reasonForAction = 'Unknown ' + reasonForActionNumv2
          else:
             reasonForAction = 'Unknown ' + reasonForActionNum


    #Format the HTML Document
    newhtml = '<td><b>Submitted By:</b> {}</td>\n'.format(submittedByContent)
    newhtml += '<td><b>Submit Date:</b> {}</td>\n'.format(submitDateContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Last Name:</b> {}</td>\n'.format(eeLastNameContent)
    newhtml += '<td><b>First Name:</b> {}</td>\n'.format(eeFirstNameContent)
    newhtml += '</tr>\n</table>'

    #Reason
    newhtml += '<h4>Reason</h4>'
    newhtml += '<table>\n<tr>\n'
    newhtml += '<td><b>Salery Adj Reason:</b> {}</td>\n'.format(reasonForAction)
    newhtml += '<td><b>Other Reason:</b> {}</td>\n'.format(saleryOtherReasonContent)
    newhtml += '<td><b>Effective Date:</b> {}</td>\n'.format(effDateContent)
    newhtml += '</tr>\n</table>\n'

    #To/From
    newhtml += '<table>\n<tr>\n<th>FROM</th>\n<th>TO</th>\n</tr>\n<tr>\n'
    newhtml += '<td><b>Job Title:</b> {}</td>\n'.format(jobTitleFromContent)
    newhtml += '<td><b>Job Title:</b> {}</td>\n'.format(jobTitleToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Department:</b> {}</td>\n'.format(deptFromContent)
    newhtml += '<td><b>Department:</b> {}</td>\n'.format(deptToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>PC:</b> {}</td>\n'.format(PCFromContent)
    newhtml += '<td><b>PC:</b> {}</td>\n'.format(PCToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Pay Rate:</b> {}</td>\n'.format(rateFromContent)
    newhtml += '<td><b>Pay Rate:</b> {}</td>\n'.format(rateToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Pay Type:</b> {}</td>\n'.format(ratePerFromContent)
    newhtml += '<td><b>Pay Type:</b> {}</td>\n'.format(ratePerToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Status:</b> {}</td>\n'.format(statusFromContent)
    newhtml += '<td><b>Status:</b> {}</td>\n'.format(statusToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Shift Type:</b> {}</td>\n'.format(shiftTypeFromContent)
    newhtml += '<td><b>Shift Type:</b> {}</td>\n'.format(shiftTypeToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Shift Length:</b> {}</td>\n'.format(shiftLFromContent)
    newhtml += '<td><b>Shift Length:</b> {}</td>\n'.format(shiftLToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Ex/Non:</b> {}</td>\n'.format(exemptFrmContent)
    newhtml += '<td><b>Ex/Non:</b> {}</td>\n'.format(exemptToContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Benifit Group:</b> {}</td>\n'.format(benGrpFromContent)
    newhtml += '<td><b>Benifit Group:</b> {}</td>\n'.format(benGrpToContent)
    newhtml += '</tr>\n</table>\n'

    #General comments
    newhtml += '<h4>Comments</h4>'
    newhtml += '<table>\n<tr>\n'
    newhtml += '<td>{}</td>\n'.format(commentsContent)
    newhtml += '</tr>\n</table>\n'

    #Termination
    newhtml += '<h4>Termination</h4>'
    newhtml += '<table>\n<tr>\n'
    newhtml += '<td><b>Effective Date:</b> Unknown</td>\n'
    newhtml += '<td><b>Term Reason:</b> {}</td>\n'.format(termReasonContent)
    newhtml += '<td><b>Rehireable:</b> {}</td>\n'.format(rehireContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Voluntary Resaon:</b> {}</td>\n'.format(volReasonContent)
    newhtml += '<td><b>Involuntary Resaon:</b> {}</td>\n'.format(inVolReasonContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Comments:</b> {}</td>\n'.format(termCommentsContent)
    newhtml += '</tr>\n</table>\n'

    #Approvals
    newhtml += '<h4>Approvals</h4>'
    newhtml += '<table>\n<tr>\n'
    newhtml += '<td><b>Approved:</b> {}</td>\n'.format(directorApprovalContent)
    newhtml += '<td><b>Director:</b> {}</td>\n'.format(directorContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Approved:</b> {}</td>\n'.format(ACApprovalContent)
    newhtml += '<td><b>Admin:</b> {}</td>\n'.format(ACContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Reject Comments:</b> {}</td>\n'.format(rejectCommentsContent)
    newhtml += '</tr>\n</table>\n'

    #HR
    newhtml += '<h4>HR Office Use</h4>'
    newhtml += '<table>\n<tr>\n'
    newhtml += '<td><b>Processed Date:</b> {}</td>\n'.format(procDateContent)
    newhtml += '<td><b>HR Staff:</b> {}</td>\n'.format(HRStaffContent)
    newhtml += '<td><b>Entered ADP:</b> {}</td>\n'.format(ADPContent)
    newhtml += '</tr>\n<tr>\n'
    newhtml += '<td><b>Notified:</b> {}</td>\n'.format(notifiedContent)
    newhtml += '</tr>\n</table>\n'

    #End
    newhtml += '</body>\n</html>'

    return newhtml
    

# Get a list of all the files in the current directory.
directoryLS = os.listdir('.')

#Loop through and only edit .xml files
for fileName in directoryLS:
   if ".xml" in fileName:
    #Get the converted content from the file, pass to variable str
    htmlOutput = XMLtoHTML(fileName)
    with open(path + eeLastNameContent + "-" + eeFirstNameContent + "-" + effDateContent + ".html", "w") as fileName:
       #insert css style into each file for portability
       fileName.write(css)
       fileName.write(head)
       fileName.write(htmlOutput)
