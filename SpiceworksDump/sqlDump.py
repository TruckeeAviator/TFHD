import sqlite3, csv

def writeCSV(output):
    with open('SpiceworksDB.csv', 'a', errors='ignore') as f:
        csvWrite = csv.writer(f)
        csvWrite.writerow(output)
      
#Change this path to the SQLite DB file
connection_obj = sqlite3.connect('C:\\spiceworks_prod.db') 

cursor_obj = connection_obj.cursor() 

ticketQuery = '''SELECT 
comments.ticket_id,
comments.body,
tickets.summary AS Subject,
tickets.description AS Description,
tickets.created_at AS Date,
users_created.email AS UserEmail,
users_assigned.email AS AgentEmail,
tickets.status
FROM tickets, comments
LEFT JOIN users as users_created ON tickets.created_by=users_created.id
LEFT JOIN users as users_assigned ON tickets.assigned_to=users_assigned.id
where tickets.id = comments.ticket_id
ORDER BY tickets.id DESC'''
 
cursor_obj.execute(ticketQuery) 

#Change this number to how many lines of output, each comment is a line.
#fetchall() is also an option
output = cursor_obj.fetchmany(250000)
for row in output: 
    writeCSV(row)

print("Done!")

connection_obj.commit()
# Close the connection 
connection_obj.close()
