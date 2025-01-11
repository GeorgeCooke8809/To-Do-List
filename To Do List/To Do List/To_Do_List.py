from pickle import NONE
import sqlite3
import datetime
import calendar

data = sqlite3.connect("ToDo.db")
cursor = data.cursor()

def add_new():
    entry = ()
    name = input("Title: ")
    description = input("Description: ")
    category = input("Category: ")

    status = ""
    while status == "":
        print()
        print("Status:")
        print("1 - Not Started")
        print("2 - In Progress")
        print("3 - On Pause")
        print()

        status = input()

        if status == "1":
            status = "Not Started"
        elif status == "2":
            status = "In Progress"
        elif status == "3":
            status = "On Pause"
        else:
            print("ERROR: Invalid Input")
            status = ""

    priority = ""

    while priority == "":
        print()
        print("Priority:")
        print("1 - Urgent")
        print("2 - High Priority")
        print("3 - Medium Priority")
        print("4 - Low Priority")
        print("5 - No Priority")
        print()

        priority = input()

        if priority == "1":
            priority = "Urgent"
        elif priority == "2":
            priority = "High Priority"
        elif priority == "3":
            priority = "Medium Prioirty"
        elif priority == "4":
            priority = "Low Priority"
        elif priority == "5":
            priority = "No Priority"
        else:
            print("ERROR: Invalid Input")
            priority = ""
    
    print()

    print("Recurring Type:")
    print("1 - None")
    print("2 - Weekly")
    print("3 - Monthly")

    print()

    recurring_type = input()

    if recurring_type == "2":
        print()
        print("Set Weekly Recurring:")
        print("1 - Monday")
        print("2 - Turesday")
        print("3 - Wednesday")
        print("4 - Thursday")
        print("5 - Friday")
        print("6 - Saturday")
        print("7 - Sunday")

        recurring = input()

        if recurring == "1":
            recurring_on = "Monday"
        elif recurring == "2":
            recurring_on = "Tuesday"
        elif recurring == "3":
            recurring_on = "Wednesday"
        elif recurring == "4":
            recurring_on = "Thursday"
        elif recurring == "5":
            recurring_on = "Friday"
        elif recurring == "6":
            recurring_on = "Saturday"
        elif recurring == "7":
            recurring_on = "Sunday"

        recurring = "w"

    elif recurring_type == "3":
        print()
        print("Select Day of Month:")
        recurring_on = int(input())
        recurring = "m"

    else:
        recurring = "n"

    if recurring != "n":
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)

    cursor.execute("SELECT COUNT(*) FROM ToDo")
    total_items = int(cursor.fetchone()[0])
    ID = total_items + 1

    entry = (ID, name, description, category, status, priority, recurring, recurring_on, yesterday)

    cursor.execute("INSERT INTO ToDo VALUES (?,?,?,?,?,?,?,?,?)", entry)
    data.commit()

    print()

    get_items()

def get_items():
    cursor.execute("SELECT COUNT(*) FROM ToDo")
    total_items = int(cursor.fetchone()[0])

    print("0 - Add New")

    for i in range(0,total_items):
        row = i+1
        cursor.execute("SELECT Recurring FROM ToDo WHERE ID =:c", {"c": row})
        recurring = cursor.fetchone()
        if recurring != None:
            recurring = recurring[0]
        if recurring == "n":
            cursor.execute("SELECT Title FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
            name = cursor.fetchone()
            if name != None:
                name = name[0]
            cursor.execute("SELECT Priority FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
            priority = cursor.fetchone()
            if priority != None:
                priority = priority[0]
            cursor.execute("SELECT Status FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
            status = cursor.fetchone()
            if status != None:
                status = status[0]
       
        elif recurring == "w":
            today = datetime.date.today()
            day_of_week = calendar.day_name[today.weekday()]
            
            cursor.execute("SELECT RecurringOn FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
            recurring_on = cursor.fetchone()
            if recurring_on != None:
                recurring_on = recurring_on[0]

            if day_of_week == recurring_on:
                cursor.execute("SELECT LastComplete FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
                last_complete = cursor.fetchone()
                if last_complete != None:
                    last_complete = last_complete[0]

                last_complete = datetime.datetime.strptime(last_complete, '%Y-%m-%d').date()
                if last_complete != today:
                    cursor.execute("SELECT Title FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
                    name = cursor.fetchone()
                    if name != None:
                        name = name[0]
                    cursor.execute("SELECT Priority FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
                    priority = cursor.fetchone()
                    if priority != None:
                        priority = priority[0]
                    cursor.execute("SELECT Status FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
                    status = cursor.fetchone()
                    if status != None:
                        status = status[0]
                else:
                    name = None
            else:
                name = None
        elif recurring == "m":
            today = datetime.date.today()
            day_of_month = str(today.day)
            
            cursor.execute("SELECT RecurringOn FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
            recurring_on = cursor.fetchone()
            if recurring_on != None:
                recurring_on = recurring_on[0]

            if recurring_on == day_of_month:
                cursor.execute("SELECT LastComplete FROM ToDo WHERE ID =:c AND STATUS != 'Complete'", {"c": row})
                last_complete = cursor.fetchone()
                if last_complete != None:
                    last_complete = last_complete[0]
                last_complete = datetime.datetime.strptime(last_complete, '%Y-%m-%d').date()


                if last_complete != today:
                    cursor.execute("SELECT Title FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
                    name = cursor.fetchone()
                    if name != None:
                        name = name[0]
                    cursor.execute("SELECT Priority FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
                    priority = cursor.fetchone()
                    if priority != None:
                        priority = priority[0]
                    cursor.execute("SELECT Status FROM ToDo WHERE ID =:c AND Status != 'Complete'", {"c": row})
                    status = cursor.fetchone()
                    if status != None:
                        status = status[0]
                else:
                    name = None
            else:
                name = None
        else:
            name = None

        if name != None:
            print(row, "-", name, "-", status, "- Priority:", priority)


    print("000 - Options")

    print()
    

    item_editing = input()

    if item_editing == "0":
        add_new()
    elif item_editing == "000":
        print()
        print("1 - View Completed")
        print("0 - Cancel")

        print()

        user_option = input()

        if user_option == "0":
            print()
            get_items()
        elif user_option == "1":
            print("0 - Go Back")
            cursor.execute("SELECT ID FROM ToDo WHERE Status = 'Complete'")
            complete_ID = cursor.fetchall()
            if complete_ID != None:
                complete_ID = complete_ID[0]
                for ID in complete_ID:
                    cursor.execute("SELECT Title FROM ToDo WHERE ID =:c", {"c": ID})
                    name = cursor.fetchone()[0]
                    cursor.execute("SELECT Category FROM ToDo WHERE ID =:c", {"c": ID})
                    category = cursor.fetchone()[0]
                    cursor.execute("SELECT Priority FROM ToDo WHERE ID =:c", {"c": ID})
                    priority = cursor.fetchone()[0]

                    print(name, "-", category, "-", priority)
            else:
                print("There Are No Complete Entries")
            user_input = input()
            get_items()

        else:
            print()
            print("ERROR: Invalid Input")
            print()

    else:
        cursor.execute("SELECT Title FROM ToDo WHERE ID =:c", {"c": item_editing})
        name = cursor.fetchone()[0]
        cursor.execute("SELECT Description FROM ToDo WHERE ID =:c", {"c": item_editing})
        description = cursor.fetchone()[0]
        cursor.execute("SELECT Category FROM ToDo WHERE ID =:c", {"c": item_editing})
        category = cursor.fetchone()[0]
        cursor.execute("SELECT Status FROM ToDo WHERE ID =:c", {"c": item_editing})
        status = cursor.fetchone()[0]

        if description == "":
            description = "No Description"

        print()

        print(name)
        print(description)
        print(category)
        print(status)

        print()

        print("1 - Mark Complete")
        print("2 - Change Status")
        print("3 - Change Priority")
        print("4 - Delete")
        print("0 - Cancel")

        print()

        option_in = input()

        print()
        
        if option_in == "0":
            print()
            get_items()
        elif option_in == "1":
            if recurring == "n":                
                cursor.execute("UPDATE ToDo SET Status = 'Complete' WHERE ID =:c", {"c": item_editing})
                data.commit()
            else:
                cursor.execute("UPDATE ToDo SET Status = 'Not Started' WHERE ID =:c", {"c": item_editing})
                data.commit()

                cursor.execute("UPDATE ToDo Set LastComplete =:d WHERE ID =:c", {"d": today, "c": item_editing})
                data.commit()

            print()
            get_items()
        elif option_in == "2":
            print()

            print("Change Status:")
            print("1 - Not Started")
            print("2 - In Progress")
            print("3 - On Pause")
            print("4 - Complete")
            print("0 - Cancel")

            print()

            status_to = int(input())

            if status_to == 1:
                cursor.execute("UPDATE ToDo SET Status = 'Not Started' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif status_to == 2:
                cursor.execute("UPDATE ToDo SET Status = 'In Progress' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif status_to == 3:
                cursor.execute("UPDATE ToDo SET Status = 'On Pause' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif status_to == 4:
                if recurring == "n":                
                    cursor.execute("UPDATE ToDo SET Status = 'Complete' WHERE ID =:c", {"c": item_editing})
                    data.commit()
                else:
                    cursor.execute("UPDATE ToDo SET Status = 'Not Started' WHERE ID =:c", {"c": item_editing})
                    data.commit()

                    cursor.execute("UPDATE ToDo Set LastComplete =:d WHERE ID =:c", {"d": today, "c": item_editing})
                    data.commit()

                print()
                get_items()
            elif status_to == 0:
                print()
                get_items()
            else:
                print()
                print("ERROR: Invalid Input")
                print()
                get_items()

        elif option_in == "3":
            print("1 - Urgent")
            print("2 - High Priority")
            print("3 - Medium Priority")
            print("4 - Low Priority")
            print("5 - No Priority")
            print("0 - Cancel")

            priority_to = input()

            if priority_to == "1":
                cursor.execute("UPDATE ToDo SET Priority = 'Urgent' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif priority_to == "2":
                cursor.execute("UPDATE ToDo SET Priority = 'High Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif priority_to == "3":
                cursor.execute("UPDATE ToDo SET Priority = 'Medium Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif priority_to == "4":
                cursor.execute("UPDATE ToDo SET Priority = 'Low Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif priority_to == "5":
                cursor.execute("UPDATE ToDo SET Priority = 'No Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
            elif priority_to == "0":
                print()
                get_items()
            else:
                print()
                print("ERROR: Invalid Input")
                print()
                get_items()


        elif option_in == "4":
            print("Are You Sure You Want To Delete? (Y/N)")
            confirm = input().upper()
            print(confirm)
            if confirm == "Y":
                cursor.execute("DELETE FROM ToDo WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                get_items()
        
        else:
            print()
            print("ERROR: Invalid Input")
            print()
            get_items()


get_items()