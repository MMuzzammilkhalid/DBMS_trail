import file_manager as fm
import database_operations as db_ops
import os

def main_menu():
    print("\nSimple DBMS Main Menu")
    print("1. Create a new database")
    print("2. Open an existing database")
    print("3. Delete a database")
    print("4. Exit")

def database_menu(db_name):
    print(f"\nDatabase Menu - {db_name}")
    print("1. Add a record")
    print("2. Edit a record")
    print("3. Delete a record")
    print("4. Display all records")
    print("5. Back to Main Menu")






def create_database():
    """
    Allows the user to create a new database by specifying field names and their maximum lengths.
    The function validates input and ensures the database name is unique.
    """
    db_name = input("Enter the name of the new database: ").strip()
    if not db_name:
        print("Database name cannot be empty!")
        return

    if fm.database_exists(db_name):
        print(f"A database with the name '{db_name}' already exists.")
        return

    fields = {}
    while True:
        field_name = input("Enter field name (or type 'done' to finish): ").strip()
        if field_name.lower() == 'done':
            break
        if not field_name:
            print("Field name cannot be empty.")
            continue
        if field_name in fields:
            print(f"Field '{field_name}' already exists. Please enter a unique name.")
            continue

        try:
            max_length = int(input(f"Enter maximum length for field '{field_name}': "))
            fields[field_name] = max_length
        except ValueError:
            print("Please enter a valid integer for field length.")

    if fields:
        # Ensure the message is printed only after the database is created successfully
        success = fm.create_database_files(db_name, fields)
        if success:
            print(f"Database '{db_name}' created successfully with fields: {fields}")
        else:
            print(f"Failed to create database '{db_name}'.")




def display_databases():
    """
    Lists all available databases in the current directory by filtering for system files.
    """
    databases = [file.replace('_system.json', '') for file in os.listdir() if file.endswith('_system.json')]
    if not databases:
        print("No databases found.")
    else:
        print("Available Databases:")
        for i, db in enumerate(databases, start=1):
            print(f"{i}. {db}")






def open_database():
    """
    Opens an existing database by allowing the user to select from available databases.
    If no databases exist, the function informs the user and returns to the main menu.
    """
    # Retrieve a list of available databases by identifying files ending with '_system.json'.
    databases = [file.replace('_system.json', '') for file in os.listdir() if file.endswith('_system.json')]
    
    # Check if there are any databases available.
    if not databases:
        print("No databases found. Returning to the main menu.")
        return

    # Display the list of available databases.
    display_databases()
    
    # Prompt the user to enter the name of the database to open.
    db_name = input("Enter the name of the database to open: ").strip()
    
    # Validate the database name entered by the user.
    if not fm.database_exists(db_name):
        print(f"Database '{db_name}' does not exist.")
        return

    # Load the database records only, as fields are not used.
    records = fm.load_data_file(db_name)

    # Enter the database menu for further operations.
    while True:
        # Display the database menu with options for managing records.
        database_menu(db_name)
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Add a new record to the database.
            db_ops.add_record(db_name)
        elif choice == "2":
            # Edit an existing record.
            if not records:
                print("No records found. Please add a record first.")
                continue
            try:
                record_index = int(input("Enter the index of the record to edit: ")) - 1
                db_ops.edit_record(db_name, record_index)
            except ValueError:
                print("Invalid input. Please enter a valid record index.")
        elif choice == "3":
            # Delete an existing record.
            if not records:
                print("No records found. Please add a record first.")
                continue
            try:
                record_index = int(input("Enter the index of the record to delete: ")) - 1
                db_ops.delete_record(db_name, record_index)
            except ValueError:
                print("Invalid input. Please enter a valid record index.")
        elif choice == "4":
            # Display all records in the database.
            db_ops.view_records(db_name)
        elif choice == "5":
            # Exit the database menu and return to the main menu.
            break
        else:
            # Handle invalid menu options.
            print("Invalid choice. Please try again.")



def delete_database():
    """
    Allows the user to delete an existing database.
    If no databases exist, informs the user and returns to the main menu.
    """
    databases = [file.replace('_system.json', '') for file in os.listdir() if file.endswith('_system.json')]
    if not databases:
        print("No databases found. Returning to the main menu.")
        return

    display_databases()
    db_name = input("Enter the name of the database to delete: ").strip()
    if not fm.database_exists(db_name):
        print(f"Database '{db_name}' does not exist.")
        return

    confirm = input(f"Are you sure you want to delete the database '{db_name}'? (yes/no): ").strip().lower()
    if confirm == 'yes':
        fm.delete_database(db_name)  # This function likely already prints a success message
    else:
        print("Deletion canceled.")








def run_cli():
    while True:
        main_menu()
        option = input("Select an option: ")

        if option == '1':
            create_database()
        elif option == '2':
            open_database()
        elif option == '3':
            delete_database()
        elif option == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    run_cli()
