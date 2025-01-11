import sqlite3

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

    cursor.execute("SELECT COUNT(*) FROM ToDo")
    total_items = int(cursor.fetchone()[0])
    ID = total_items + 1

    entry = (ID, name, description, status, category, priority, "", "", "")

    cursor.execute("INSERT INTO ToDo VALUES (?,?,?,?,?,?,?,?,?)", entry)
    data.commit()


    get_items()

def get_items():
    cursor.execute("SELECT COUNT(*) FROM ToDo")
    total_items = int(cursor.fetchone()[0])

    print("0 - Add New")

    for i in range(0,total_items):
        row = i+1
        cursor.execute("SELECT Title FROM ToDo WHERE ID =:c", {"c": row})
        name = cursor.fetchone()[0]
        cursor.execute("SELECT Priority FROM ToDo WHERE ID =:c", {"c": row})
        priority = cursor.fetchone()[0]
        cursor.execute("SELECT Category FROM ToDo WHERE ID =:c", {"c": row})
        category = cursor.fetchone()[0]

        print(row, "-", name, "-", category, "- Priority:", priority)

    print()
    

    item_editing = input()

    if item_editing == "0":
        add_new()
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
            cursor.execute("UPDATE ToDo SET Status = 'Complete' WHERE ID =:c", {"c": item_editing})
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
                cursor.execute("UPDATE ToDo SET Status = 'Complete' WHERE ID =:c", {"c": item_editing})
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