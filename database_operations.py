import json
import os
import file_manager as fm  # Ensure to import the file manager
def delete_database(db_name):
    """Deletes the entire database by removing its data and system files."""
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"
    
    # Check if the data file exists
    if os.path.exists(data_file):
        os.remove(data_file)
        print(f"Deleted data file: {data_file}")
    else:
        print(f"Data file '{data_file}' not found.")

    # Check if the system file exists
    if os.path.exists(system_file):
        os.remove(system_file)
        print(f"Deleted system file: {system_file}")
    else:
        print(f"System file '{system_file}' not found.")

    print(f"Database '{db_name}' has been deleted successfully.")

def load_system_file(db_name):
    """Loads the system file for the specified database."""
    system_file = f"{db_name}_system.json"
    if not os.path.exists(system_file):
        print(f"System file for database '{db_name}' not found.")
        return None
    with open(system_file, 'r') as f:
        return json.load(f)

def load_data_file(db_name):
    """Loads the data file for the specified database."""
    data_file = f"{db_name}_data.json"
    if not os.path.exists(data_file):
        print(f"Data file for database '{db_name}' not found.")
        return None
    with open(data_file, 'r') as f:
        return json.load(f)

def save_data_file(db_name, records):
    """Saves the records to the data file for the specified database."""
    data_file = f"{db_name}_data.json"
    with open(data_file, 'w') as f:
        json.dump(records, f, indent=4)

import file_manager as fm

def add_record(db_name):
    fields = fm.load_system_file(db_name)
    record = {}
    
    for field, max_length in fields.items():
        value = input(f"Enter value for '{field}' (max {max_length} chars): ")
        if len(value) > max_length:
            print(f"Value for '{field}' exceeds maximum length of {max_length}.")
            return
        record[field] = value

    # Load existing records
    records = fm.load_data_file(db_name)
    # Append the new record to the records list
    records.append(record)
    # Save the updated records back to the data file
    fm.save_data_file(db_name, records)

    print("Record added successfully.")










def view_records(db_name):
    """
    Displays all records in the specified database in a tabular format with symmetrical alignment.
    """
    # Load records from the database
    records = fm.load_data_file(db_name)
    if not records:
        print("No records found.")
        return

    # Extract field names (headers) and calculate column widths
    headers = list(records[0].keys())
    column_widths = {header: len(header) for header in headers}

    # Update column widths based on the longest value in each column
    for record in records:
        for field, value in record.items():
            column_widths[field] = max(column_widths[field], len(str(value)))

    # Create the header row and separator
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    separator = "+-" + "-+-".join("-" * column_widths[header] for header in headers) + "-+"

    # Print the table
    print(separator)
    print(f"| {header_row} |")
    print(separator)
    for record in records:
        row = " | ".join(str(record[field]).ljust(column_widths[field]) for field in headers)
        print(f"| {row} |")
    print(separator)


def delete_record(db_name, record_index):
    """Deletes a record by its index from the specified database."""
    records = load_data_file(db_name)
    if records is None:
        return

    # Validate the record index
    if record_index < 0 or record_index >= len(records):
        print("Invalid record index.")
        return

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete record {record_index + 1}? (yes/no): ").strip().lower()
    if confirm == 'yes':
        records.pop(record_index)
        save_data_file(db_name, records)
        print(f"Record {record_index + 1} deleted successfully.")
    else:
        print("Deletion canceled.")

def edit_record(db_name, record_index):
    """Edits an existing record in the specified database."""
    fields, records = fm.load_database_files(db_name)

    # Check if the record index is within the range of existing records
    if record_index < 0 or record_index >= len(records):
        print("Invalid record index. Please enter a valid index.")
        return
    
    # Display the current values of the record and prompt for new values
    record = records[record_index]
    print(f"Editing record {record_index + 1}:")
    for field in fields:
        current_value = record.get(field, "")
        
        while True:
            new_value = input(f"{field} [{current_value}]: ") or current_value
            if field == "rollNo":
                if not new_value.isdigit():
                    print("Error: 'rollNo' must be a numeric value.")
                    continue
            
            if len(new_value) <= fields[field]:  # Ensure new value does not exceed max length
                record[field] = new_value
                break
            else:
                print(f"Error: '{field}' value exceeds maximum length of {fields[field]}")
                return
    
    # Save the updated records
    fm.save_data_file(db_name, records)
    print("Record updated successfully.")
