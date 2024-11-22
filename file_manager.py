import json
import os

def delete_database(db_name):
    """
    Deletes the specified database by removing its associated files.
    """
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"

    # Remove the data file if it exists
    if os.path.exists(data_file):
        os.remove(data_file)
        print(f"Deleted data file: {data_file}")
    else:
        print(f"Data file '{data_file}' not found.")

    # Remove the system file if it exists
    if os.path.exists(system_file):
        os.remove(system_file)
        print(f"Deleted system file: {system_file}")
    else:
        print(f"System file '{system_file}' not found.")

    print(f"Database '{db_name}' has been deleted successfully.")

def create_database_files(db_name, fields):
    """
    Creates the necessary files for a new database, including data and system files.
    """
    data_file = f"{db_name}_data.json"
    system_file = f"{db_name}_system.json"

    # Create the data file and system file
    try:
        with open(system_file, 'w') as f:
            json.dump(fields, f, indent=4)  # Save the fields (metadata)
        with open(data_file, 'w') as f:
            json.dump([], f, indent=4)  # Initialize with an empty list of records
        return True  # Indicate success
    except Exception as e:
        print(f"Error creating database files: {e}")
        return False  # Indicate failure

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

def database_exists(db_name):
    """Checks if the database files for the specified database exist."""
    system_file = f"{db_name}_system.json"
    data_file = f"{db_name}_data.json"
    return os.path.exists(system_file) and os.path.exists(data_file)

def load_database_files(db_name):
    """Loads both the system and data files for the specified database."""
    fields = load_system_file(db_name)
    records = load_data_file(db_name)
    return fields, records
