import csv, sqlite3
import re
from datetime import datetime

#Function to extract date from Text
def parse_datetime_string(date_string):
    # Use regex to extract the year, month, and day
    match = re.search(r'datetime\.date\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2})\)', date_string)
    
    if match:
        year, month, day = map(int, match.groups())
        # Create a datetime object
        date_obj = datetime(year, month, day).date()
        return date_obj.strftime('%Y-%m-%d')
    else:
        raise ValueError("Invalid datetime.date string format")
    
if __name__ == "__main__":
    #Read CSV
    try:
        with open('5k_borrowers_data.csv', mode ='r')as file:
            list = []
            csvFile = csv.reader(file)
            for lines in csvFile:
                list.append(lines)
    except:
        print("There is some I/O Error!!!!!!! Check if file is there")
    
    listOfLists = []
    n = len(list)
    for i in range(1, n):
        insertPre = f'{i},'
        insertSuf = ""
        for j in range(0, len(list[i])):
            if j in [9, 11, 12,13, 15]:
                insertPre += list[i][j] + ","
            elif j == 19:
                insertSuf += list[i][j] + ","
            elif j == 20: 
                insertSuf += "'"+list[i][j]+"'"
            elif j==18:
                continue
            else:
                insertPre += "'" + list[i][j] + "',"
        #Since I am not reading JSON in SQL, I am creating seprate records for JSON values
        #Not the most Optimal way to go with
        listOfQueries = []
        listTmp = list[i][18][1:-1].split("{")
        for x in listTmp:
            if len(x) == 0:
                continue
            str = "{" + x
            if str.endswith(", "):
                str = str[:-2]
            payment_date = parse_datetime_string(str)
            payment_mode = str.split(":")[2][2:-2]
            listOfQueries.append(insertPre+"'"+payment_date+"','"+payment_mode+"',"+insertSuf)
        
        listOfLists.append(listOfQueries)

    conn = sqlite3.connect("Task.db") 
    cursor = conn.cursor() 
    #Inserting Data to SQLite
    
    for l in listOfLists:
        for l1 in l:
            cursor.execute(" INSERT INTO Repayments VALUES (" + l1 +")")
    print("Loaded Data to DB")
    conn.commit() 
    conn.close()

