import sqlite3
import datetime
import calendar
import tkinter
import customtkinter

data = sqlite3.connect("ToDo.db")
cursor = data.cursor()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("themes/mono.json")


def add_new():
    global repeating_bool, new_prioirty, recurring, new_priority, new_category, description_entry, title_entry, yesterday, add_new_root

    recurring = "n"
    yesterday = None

    add_new_root = customtkinter.CTk()
    add_new_root.geometry("550x500")
    add_new_root.resizable(width = False, height = False)

    new_entry_frame = customtkinter.CTkFrame(add_new_root)
    heading = customtkinter.CTkFont("Monoton", 25, "bold")

    new_entry_frame.rowconfigure(0, weight = 1)
    new_entry_frame.rowconfigure(1, weight = 1)
    new_entry_frame.rowconfigure(2, weight = 1)
    new_entry_frame.rowconfigure(3, weight = 3)
    new_entry_frame.rowconfigure(4, weight = 1)
    new_entry_frame.rowconfigure(5, weight = 1)

    new_entry_frame.columnconfigure(0, weight = 1)
    new_entry_frame.columnconfigure(1, weight = 1)

    title_label = customtkinter.CTkLabel(new_entry_frame, text = "Title", font = heading)
    title_label.grid(row = 0, column = 0, sticky = "w", padx = 5)

    submit_button = customtkinter.CTkButton(new_entry_frame, text = "Submit", command = submit_new, font = ("Monoton", 25), corner_radius = 0)
    submit_button.grid(row = 0, column = 1, sticky = "e", padx = 5)

    title_entry = customtkinter.CTkEntry(new_entry_frame, corner_radius = 0, font = ("monoton", 20))
    title_entry.grid(row = 1, column = 0, columnspan = 2, sticky = "nesw", padx = 5)

    description_label = customtkinter.CTkLabel(new_entry_frame, text = "Description", font = heading)
    description_label.grid(row = 2, column = 0, sticky = "w", padx = 5)

    description_entry = customtkinter.CTkTextbox(new_entry_frame, corner_radius = 0, font = ("monoton", 20), border_width = 2)
    description_entry.grid(row = 3, column = 0, columnspan = 2, sticky = "nesw", padx = 5)

    repeating_bool = tkinter.IntVar(value = 0)
    repeating_radio_btn_once = customtkinter.CTkRadioButton(new_entry_frame, text = "One Time", command = change_repeating_bool, variable = repeating_bool, value = 1, font = ("Monoton", 30))
    repeating_radio_btn_once.grid(row = 4, column = 0, sticky = "nesw", padx = 5)
    repeating_radio_btn_repeat = customtkinter.CTkRadioButton(new_entry_frame, text = "Repeating", command = change_repeating_bool, variable = repeating_bool, value = 2, font = ("Monoton", 30))
    repeating_radio_btn_repeat.grid(row = 4, column = 1, sticky = "nesw", padx = 5)

    new_priority = customtkinter.StringVar(value = "No Priority")
    priority_menu = customtkinter.CTkOptionMenu(new_entry_frame, values = ["No Priority", "Low Priority", "Medium Priority", "High Priority", "Urgent"], command = set_new_priority, anchor = "center", font = ("Monoton", 20), dropdown_font = ("Monoton", 20), corner_radius = 0,button_color = "#696969", fg_color = "#a8a8a8", text_color = "black")
    priority_menu.grid(row = 5, column = 0, sticky = "nesw", padx = 5)

    new_category = customtkinter.StringVar(value = "Select Category")
    new_category = customtkinter.CTkComboBox(new_entry_frame, values = ["Homework", "Revision", "YouTube", "Programming", "Aviation", "Finance"], command = set_new_category,justify = "center", font = ("Monoton", 20), dropdown_font = ("Monoton", 20), corner_radius = 0,button_color = "#696969", fg_color = "#a8a8a8", text_color = "black", border_width = 0)
    new_category.grid(row = 5, column = 1, sticky = "nesw", padx = 5)


    new_entry_frame.pack(anchor = "center", expand = True, fill = "both",padx = 5, pady = 10)
    add_new_root.mainloop()

    submit_new() # TODO: finish this

def change_repeating_bool():
    global recurring, recurring_on, date_select_frame, date_select_window

    repeating = repeating_bool.get()

    if repeating == 1:
        recurring = "n"
        recurring_on = None
    elif repeating == 2:
        date_select_window = customtkinter.CTk()
        date_select_window.geometry("500x350")
        date_select_window.resizable(width = False, height = False)

        date_select_frame = customtkinter.CTkFrame(date_select_window)

        date_select_frame.rowconfigure(0, weight = 1)
        date_select_frame.rowconfigure(1, weight = 1)
        date_select_frame.rowconfigure(2, weight = 1)
        date_select_frame.rowconfigure(3, weight = 1)
        date_select_frame.rowconfigure(4, weight = 1)
        date_select_frame.rowconfigure(5, weight = 1)
        date_select_frame.rowconfigure(6, weight = 1)
        date_select_frame.rowconfigure(7, weight = 1)
        date_select_frame.rowconfigure(8, weight = 1)

        date_select_frame.columnconfigure(0, weight = 1)
        date_select_frame.columnconfigure(1, weight = 1)
        date_select_frame.columnconfigure(2, weight = 1)
        date_select_frame.columnconfigure(3, weight = 1)
        date_select_frame.columnconfigure(4, weight = 1)
        date_select_frame.columnconfigure(5, weight = 1)
        date_select_frame.columnconfigure(6, weight = 1)

        back_button = customtkinter.CTkButton(date_select_frame, text = "Back", command = back_to_new, font = ("Monoton", 25), corner_radius = 0)
        back_button.grid(row = 0, column = 0, columnspan = 2,sticky = "w", padx = 5)

        continue_button = customtkinter.CTkButton(date_select_frame, text = "Continue", command = continue_to_new, font = ("Monoton", 25), corner_radius = 0)
        continue_button.grid(row = 0, column = 5, columnspan = 2, sticky = "e", padx = 5)

        weekly_label = customtkinter.CTkLabel(date_select_frame, text = "Weekly", font = ("Monoton", 25, "bold"))
        weekly_label.grid(row = 1, column = 0, columnspan = 7, sticky = "w", padx = 5, pady = 5)

        monday_button = customtkinter.CTkButton(date_select_frame, text = "M", command = lambda:set_weekly_recurring("1"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
        monday_button.grid(row = 2, column = 0, columnspan = 1,sticky = "nesw", padx = 5)
        tuesday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("2"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
        tuesday_button.grid(row = 2, column = 1, columnspan = 1,sticky = "nesw", padx = 5)
        wednesday_button = customtkinter.CTkButton(date_select_frame, text = "W", command = lambda:set_weekly_recurring("3"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
        wednesday_button.grid(row = 2, column = 2, columnspan = 1,sticky = "nesw", padx = 5)
        thursday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("4"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
        thursday_button.grid(row = 2, column = 3, columnspan = 1,sticky = "nesw", padx = 5)
        friday_button = customtkinter.CTkButton(date_select_frame, text = "F", command = lambda:set_weekly_recurring("5"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
        friday_button.grid(row = 2, column = 4, columnspan = 1,sticky = "nesw", padx = 5)
        saturday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("6"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#545454", text_color = "white")
        saturday_button.grid(row = 2, column = 5, columnspan = 1,sticky = "nesw", padx = 5)
        sunday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("7"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#545454", text_color = "white")
        sunday_button.grid(row = 2, column = 6, columnspan = 1,sticky = "nesw", padx = 5)

        monthly_label = customtkinter.CTkLabel(date_select_frame, text = "Monthly", font = ("Monoton", 25, "bold"),)
        monthly_label.grid(row = 3, column = 0, columnspan = 7, sticky = "w", padx = 5, pady = 5)

        button = {}
        row = 4
        col = 0

        for day in range(1,32):
            action = lambda x = day: set_monthly_recurring(x)
            button[day] = customtkinter.CTkButton(date_select_frame, text = day, command = action, font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black", anchor = "center")
            button[day].grid(row=row, column = col, sticky = "nesw", padx = 5, pady = 5)

            col = col + 1
            if col == 7:
                col = 0
                row = row + 1


        date_select_frame.pack(anchor = "center", expand = True, fill = "both", padx = 5, pady =10)
        date_select_window.mainloop()

def back_to_new():
    date_select_window.destroy()
    recurring = "n"
    recurring_on = None

def continue_to_new():
    date_select_window.destroy()

def set_new_priority():
    pass

def set_new_category():
    pass

def submit_new(): # TODO: do this (submit new)
    global recurring, recurring_on, yesterday, new_priority, new_category, description_entry, title_entry, add_new_root

    name = title_entry.get()
    description = description_entry.get("0.0", "end")
    category = new_category.get()
    priority = new_priority.get()
    status = "Not Started"

    cursor.execute("SELECT COUNT(*) FROM ToDo")
    total_items = int(cursor.fetchone()[0])

    ID = total_items + 1

    entry = (ID, name, description, category, status, priority, recurring, recurring_on, yesterday) # prioirty will be stored as "new_prioiryty" and is in string form

    cursor.execute("INSERT INTO ToDo VALUES (?,?,?,?,?,?,?,?,?)", entry)
    data.commit()

    add_new_root.destroy()

    print()

    update_todo()

def update_todo():
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

    show_details()

def show_details():
    global recurring

    print("000 - Options")

    print()
    

    item_editing = input()

    if item_editing == "0":
        add_new()
    elif item_editing == "000":
        display_options()

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
        print("0 - Cancel")

        print()

        option_in = input()

        print()
        
        if option_in == "0":
            print()
            update_todo()
        elif option_in == "1":
            mark_comlete(item_editing)
           

            print()
            update_todo()
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
                update_todo()
            elif status_to == 2:
                cursor.execute("UPDATE ToDo SET Status = 'In Progress' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                update_todo()
            elif status_to == 3:
                cursor.execute("UPDATE ToDo SET Status = 'On Pause' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                update_todo()
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
                update_todo()
            elif status_to == 0:
                print()
                update_todo()
            else:
                print()
                print("ERROR: Invalid Input")
                print()
                update_todo()

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
                update_todo()
            elif priority_to == "2":
                cursor.execute("UPDATE ToDo SET Priority = 'High Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                update_todo()
            elif priority_to == "3":
                cursor.execute("UPDATE ToDo SET Priority = 'Medium Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                update_todo()
            elif priority_to == "4":
                cursor.execute("UPDATE ToDo SET Priority = 'Low Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                update_todo()
            elif priority_to == "5":
                cursor.execute("UPDATE ToDo SET Priority = 'No Priority' WHERE ID =:c", {"c": item_editing})
                data.commit()
                print()
                update_todo()
            elif priority_to == "0":
                print()
                update_todo()
            else:
                print()
                print("ERROR: Invalid Input")
                print()
                update_todo()
        
        else:
            print()
            print("ERROR: Invalid Input")
            print()
            update_todo()

def view_completed(): # TODO: update
    print()

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
    print()
    update_todo()

def mark_comlete(item_editing):
     if recurring == "n":                
        cursor.execute("UPDATE ToDo SET Status = 'Complete' WHERE ID =:c", {"c": item_editing})
        data.commit()
     else:
        cursor.execute("UPDATE ToDo SET Status = 'Not Started' WHERE ID =:c", {"c": item_editing})
        data.commit()

        cursor.execute("UPDATE ToDo Set LastComplete =:d WHERE ID =:c", {"d": today, "c": item_editing}) # TODO: broken?
        data.commit()

def print_todo():
    pass # TODO: make a pdf then print

def display_options(): # TODO: update
    print()
    print("1 - View Completed")
    print("2 - Print")
    print("0 - Cancel")

    print()

    user_option = input()

    if user_option == "0":
        print()
        update_todo()
    elif user_option == "1":
        view_completed()
    elif user_option == "2:":
        print_todo()
    else:
        print()
        print("ERROR: Invalid Input")
        print()

def save_edits(item_editing): #TODO: where edit presexisting entry will go (save)
    pass

def set_weekly_recurring(weekday):
    global recurring, recurring_on, date_select_frame, date_select_window, yesterday

    monday_button = customtkinter.CTkButton(date_select_frame, text = "M", command = lambda:set_weekly_recurring("1"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    monday_button.grid(row = 2, column = 0, columnspan = 1,sticky = "nesw", padx = 5)
    tuesday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("2"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    tuesday_button.grid(row = 2, column = 1, columnspan = 1,sticky = "nesw", padx = 5)
    wednesday_button = customtkinter.CTkButton(date_select_frame, text = "W", command = lambda:set_weekly_recurring("3"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    wednesday_button.grid(row = 2, column = 2, columnspan = 1,sticky = "nesw", padx = 5)
    thursday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("4"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    thursday_button.grid(row = 2, column = 3, columnspan = 1,sticky = "nesw", padx = 5)
    friday_button = customtkinter.CTkButton(date_select_frame, text = "F", command = lambda:set_weekly_recurring("5"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    friday_button.grid(row = 2, column = 4, columnspan = 1,sticky = "nesw", padx = 5)
    saturday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("6"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#545454", text_color = "white")
    saturday_button.grid(row = 2, column = 5, columnspan = 1,sticky = "nesw", padx = 5)
    sunday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("7"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#545454", text_color = "white")
    sunday_button.grid(row = 2, column = 6, columnspan = 1,sticky = "nesw", padx = 5)

    button = {}
    row = 4
    col = 0

    for day in range(1,32):
        action = lambda x = day: set_monthly_recurring(x)
        button[day] = customtkinter.CTkButton(date_select_frame, text = day, command = action, font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black", anchor = "center")
        button[day].grid(row=row, column = col, sticky = "nesw", padx = 5, pady = 5)

        col = col + 1
        if col == 7:
            col = 0
            row = row + 1

    if weekday == "1":
        recurring_on = "Monday"
        monday_button = customtkinter.CTkButton(date_select_frame, text = "M", command = lambda:set_weekly_recurring("1"), font = ("Monoton", 20), corner_radius = 0, fg_color = "Black", text_color = "White")
        monday_button.grid(row = 2, column = 0, columnspan = 1,sticky = "nesw", padx = 5)
    elif weekday == "2":
        recurring_on = "Tuesday"
        tuesday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("2"), font = ("Monoton", 20), corner_radius = 0, fg_color = "Black", text_color = "White")
        tuesday_button.grid(row = 2, column = 1, columnspan = 1,sticky = "nesw", padx = 5)
    elif weekday == "3":
        recurring_on = "Wednesday"
        wednesday_button = customtkinter.CTkButton(date_select_frame, text = "W", command = lambda:set_weekly_recurring("3"), font = ("Monoton", 20), corner_radius = 0, fg_color = "Black", text_color = "White")
        wednesday_button.grid(row = 2, column = 2, columnspan = 1,sticky = "nesw", padx = 5)
    elif weekday == "4":
        recurring_on = "Thursday"
        thursday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("4"), font = ("Monoton", 20), corner_radius = 0, fg_color = "Black", text_color = "White")
        thursday_button.grid(row = 2, column = 3, columnspan = 1,sticky = "nesw", padx = 5)
    elif weekday == "5":
        recurring_on = "Friday"
        friday_button = customtkinter.CTkButton(date_select_frame, text = "F", command = lambda:set_weekly_recurring("5"), font = ("Monoton", 20), corner_radius = 0, fg_color = "Black", text_color = "White")
        friday_button.grid(row = 2, column = 4, columnspan = 1,sticky = "nesw", padx = 5)
    elif weekday == "6":
        recurring_on = "Saturday"
        saturday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("6"), font = ("Monoton", 20), corner_radius = 0, fg_color = "Black", text_color = "White")
        saturday_button.grid(row = 2, column = 5, columnspan = 1,sticky = "nesw", padx = 5)
    elif weekday == "7":
        recurring_on = "Sunday"
        sunday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("7"), font = ("Monoton", 20), corner_radius = 0, fg_color = "Black", text_color = "White")
        sunday_button.grid(row = 2, column = 6, columnspan = 1,sticky = "nesw", padx = 5)

    recurring = "w"
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)

    date_select_frame.pack(anchor = "center", expand = True, fill = "both", padx = 5, pady =10)
    date_select_window.mainloop()

def set_monthly_recurring(weekday):
    global recurring, recurring_on, date_select_frame, date_select_window, yesterday


    monday_button = customtkinter.CTkButton(date_select_frame, text = "M", command = lambda:set_weekly_recurring("1"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    monday_button.grid(row = 2, column = 0, columnspan = 1,sticky = "nesw", padx = 5)
    tuesday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("2"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    tuesday_button.grid(row = 2, column = 1, columnspan = 1,sticky = "nesw", padx = 5)
    wednesday_button = customtkinter.CTkButton(date_select_frame, text = "W", command = lambda:set_weekly_recurring("3"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    wednesday_button.grid(row = 2, column = 2, columnspan = 1,sticky = "nesw", padx = 5)
    thursday_button = customtkinter.CTkButton(date_select_frame, text = "T", command = lambda:set_weekly_recurring("4"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    thursday_button.grid(row = 2, column = 3, columnspan = 1,sticky = "nesw", padx = 5)
    friday_button = customtkinter.CTkButton(date_select_frame, text = "F", command = lambda:set_weekly_recurring("5"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black")
    friday_button.grid(row = 2, column = 4, columnspan = 1,sticky = "nesw", padx = 5)
    saturday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("6"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#545454", text_color = "white")
    saturday_button.grid(row = 2, column = 5, columnspan = 1,sticky = "nesw", padx = 5)
    sunday_button = customtkinter.CTkButton(date_select_frame, text = "S", command = lambda:set_weekly_recurring("7"), font = ("Monoton", 20), corner_radius = 0, fg_color = "#545454", text_color = "white")
    sunday_button.grid(row = 2, column = 6, columnspan = 1,sticky = "nesw", padx = 5)

    button = {}
    row = 4
    col = 0

    for day in range(1,32):
        action = lambda x = day: set_monthly_recurring(x)
        button[day] = customtkinter.CTkButton(date_select_frame, text = day, command = action, font = ("Monoton", 20), corner_radius = 0, fg_color = "#D9D9D9", text_color = "black", anchor = "center")
        button[day].grid(row=row, column = col, sticky = "nesw", padx = 5, pady = 5)

        col = col + 1
        if col == 7:
            col = 0
            row = row + 1
    
    action = lambda x = weekday: set_monthly_recurring(x)
    button[weekday] = customtkinter.CTkButton(date_select_frame, text = weekday, command = action, font = ("Monoton", 20), corner_radius = 0, fg_color = "black", text_color = "white", anchor = "center")
    col = (weekday % 7)
    if col != 0:
        col = col - 1
    elif col == 0:
        col = 6
    row = (weekday // 7) + 4
    if col == 6:
        row = row - 1
    button[weekday].grid(row=row, column = col, sticky = "nesw", padx = 5, pady = 5)

    recurring_on = weekday
    recurring = "m"
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)

    print(recurring_on)

    date_select_frame.pack(anchor = "center", expand = True, fill = "both", padx = 5, pady =10)
    date_select_window.mainloop()

update_todo()