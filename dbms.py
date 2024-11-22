import file_manager as fm
import os

def create_database():
    """Create a new database by collecting field information and using file manager functions."""
    # Ask the user for the database name
    db_name = input("Enter the name of the new database: ")
    if not db_name:
        print("Database name cannot be empty!")
        return
    
    # Check if the database already exists
    if fm.database_exists(db_name):
        print(f"A database with the name '{db_name}' already exists.")
        return
    
    # Collect field information
    fields = {}
    while True:
        field_name = input("Enter field name (or type 'done' to finish): ")
        if field_name.lower() == 'done':
            break
        if not field_name:
            print("Field name cannot be empty.")
            continue
        
        try:
            max_length = int(input(f"Enter maximum length for field '{field_name}': "))
            fields[field_name] = max_length
        except ValueError:
            print("Please enter a valid integer for field length.")
    
    if not fields:
        print("No fields were added. Database creation aborted.")
        return
    
    # Use file_manager to create the database files
    success = fm.create_database_files(db_name, fields)
    if success:
        print(f"Database '{db_name}' created successfully!")
        print(f"Fields: {fields}")

# Example usage of file_manager functions directly
def main():
    db_name = "my_database"
    fields = {
        "Name": 20,
        "Age": 3,
        "Email": 30
    }

    # Create a new database
    fm.create_database_files(db_name, fields)

    # Load an existing database
    fields, records = fm.load_database_files(db_name)
    if fields:
        print("Fields:", fields)
        print("Records:", records)

    # Save data to the data file
    new_records = [{"Name": "Alice", "Age": "25", "Email": "alice@example.com"}]
    fm.save_data_file(db_name, new_records)

# Run the create_database function to create a database through user input
create_database()
