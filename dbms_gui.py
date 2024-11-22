import tkinter as tk
from tkinter import simpledialog, messagebox
import file_manager as fm  # Assuming this contains your file handling functions

class SimpleDBMS:
    def __init__(self, master):
        self.master = master
        master.title("Simple Database Management System")
        master.geometry("400x500")
        master.config(bg="#f0f0f0")

        # Frame for Title
        title_frame = tk.Frame(master, bg="#4CAF50")
        title_frame.pack(fill=tk.X)

        self.label = tk.Label(title_frame, text="Welcome to Simple DBMS", font=("Arial", 16), bg="#4CAF50", fg="white")
        self.label.pack(pady=10)

        # Frame for Buttons
        self.button_frame = tk.Frame(master, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        # Main Menu Buttons
        self.create_db_button = tk.Button(self.button_frame, text="Create Database", command=self.create_database, width=20, bg="#4CAF50", fg="white")
        self.create_db_button.pack(pady=5)

        self.open_db_button = tk.Button(self.button_frame, text="Open Database", command=self.open_database, width=20, bg="#2196F3", fg="white")
        self.open_db_button.pack(pady=5)

        self.delete_db_button = tk.Button(self.button_frame, text="Delete Database", command=self.delete_database, width=20, bg="#F44336", fg="white")
        self.delete_db_button.pack(pady=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=master.quit, width=20, bg="#9E9E9E", fg="white")
        self.exit_button.pack(pady=5)

        # Record Management Buttons
        self.record_buttons = []  # Store the record management buttons
        self.records = []  # Initialize records
        self.current_db_name = None  # Keep track of the current database name

    def create_database(self):
        db_name = simpledialog.askstring("Input", "Enter the name of the new database:")
        if not db_name:
            messagebox.showwarning("Warning", "Database name cannot be empty.")
            return

        if fm.database_exists(db_name):
            messagebox.showwarning("Warning", f"A database named '{db_name}' already exists.")
            return

        fields = {}
        while True:
            field_name = simpledialog.askstring("Field Input", "Enter field name (or type 'done' to finish):")
            if field_name is None or field_name.lower() == 'done':
                break
            if not field_name:
                messagebox.showwarning("Warning", "Field name cannot be empty.")
                continue

            max_length = simpledialog.askinteger("Field Length", f"Enter maximum length for field '{field_name}':")
            if max_length is None or max_length <= 0:
                messagebox.showwarning("Warning", "Please enter a valid positive integer for field length.")
                continue

            fields[field_name] = max_length

        if not fields:
            messagebox.showwarning("Warning", "No fields were added. Database creation aborted.")
            return

        success = fm.create_database_files(db_name, fields)  # Assuming this function exists in file_manager
        if success:
            messagebox.showinfo("Success", f"Database '{db_name}' created successfully!")
            print(f"Database '{db_name}' created with fields: {fields}")  # Optional: Console logging

    def delete_database(self):
        db_name = simpledialog.askstring("Input", "Enter the name of the database to delete:")
        if not db_name:
            messagebox.showwarning("Warning", "Database name cannot be empty.")
            return

        if not fm.database_exists(db_name):
            messagebox.showwarning("Warning", f"Database '{db_name}' does not exist.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the database '{db_name}'?")
        if confirm:
            fm.delete_database(db_name)  # Assuming this function exists in file_manager
            messagebox.showinfo("Success", f"Database '{db_name}' has been deleted successfully.")
        else:
            messagebox.showinfo("Info", "Database deletion canceled.")

    def open_database(self):
        db_name = simpledialog.askstring("Input", "Enter the name of the database to open:")
        if not db_name:
            messagebox.showwarning("Warning", "Database name cannot be empty.")
            return

        if not fm.database_exists(db_name):
            messagebox.showwarning("Warning", f"Database '{db_name}' does not exist.")
            return

        fields, self.records = fm.load_database_files(db_name)  # Assuming this function exists
        self.display_all_records(fields)  # Call to display_all_records

        # Inform the user that they are now working in this database
        messagebox.showinfo("Database Opened", f"You are now working with the database '{db_name}'.")
        self.current_db_name = db_name  # Set the current database name

        self.clear_main_menu()  # Hide main menu buttons
        self.show_record_management_buttons(fields)  # Show record management options

    def clear_main_menu(self):
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()  # Hide main menu buttons

    def show_record_management_buttons(self, fields):
        self.add_record_button = tk.Button(self.master, text="Add Record", command=lambda: self.add_record(self.current_db_name, fields), bg="#FFC107")
        self.add_record_button.pack(pady=5)
        self.record_buttons.append(self.add_record_button)

        self.edit_record_button = tk.Button(self.master, text="Edit Record", command=lambda: self.edit_record(fields), bg="#2196F3")
        self.edit_record_button.pack(pady=5)
        self.record_buttons.append(self.edit_record_button)

        self.delete_record_button = tk.Button(self.master, text="Delete Record", command=self.delete_record, bg="#F44336")
        self.delete_record_button.pack(pady=5)
        self.record_buttons.append(self.delete_record_button)

        self.display_all_button = tk.Button(self.master, text="Display All Records", command=lambda: self.display_all_records(fields), bg="#4CAF50")
        self.display_all_button.pack(pady=5)
        self.record_buttons.append(self.display_all_button)

        self.back_button = tk.Button(self.master, text="Back to Main Menu", command=self.back_to_main_menu, bg="#9E9E9E")
        self.back_button.pack(pady=5)
        self.record_buttons.append(self.back_button)

    def back_to_main_menu(self):
        for button in self.record_buttons:
            button.pack_forget()  # Hide record management buttons
        self.reset_main_menu()  # Show main menu buttons again

    def reset_main_menu(self):
        self.create_db_button.pack(pady=5)
        self.open_db_button.pack(pady=5)
        self.delete_db_button.pack(pady=5)
        self.exit_button.pack(pady=5)

    def add_record(self, db_name, fields):
        """Adds a new record to the opened database."""
        record = {}
        for field, max_length in fields.items():
            value = simpledialog.askstring("Input", f"Enter value for '{field}' (max {max_length} chars):")
            if value and len(value) > max_length:
                messagebox.showwarning("Warning", f"Value for '{field}' exceeds maximum length of {max_length}.")
                return
            record[field] = value

        # Load existing records
        records = fm.load_data_file(db_name) or []
        
        # Append the new record to the list of records
        records.append(record)
        
        # Save the updated records back to the data file
        fm.save_data_file(db_name, records)
        messagebox.showinfo("Success", "Record added successfully.")

    def edit_record(self, fields):
        """Edits an existing record in the opened database."""
        if not self.records:  # Check if records are available
            messagebox.showwarning("Warning", "No records available to edit.")
            return

        # Prompt user to enter the index of the record to edit
        record_index = simpledialog.askinteger("Input", f"Enter the index of the record to edit (0 to {len(self.records) - 1}):")
        if record_index is None or record_index < 0 or record_index >= len(self.records):
            messagebox.showwarning("Warning", "Invalid record index.")
            return

        record = self.records[record_index]  # Get the record to edit

        for field in fields.keys():
            # Prompt user for new value, using the current value as a hint
            new_value = simpledialog.askstring("Edit Value", f"Edit value for '{field}' (current: '{record[field]}'):")
            if new_value is not None:  # If user provided a new value
                # Check if the new value exceeds the maximum length
                if len(new_value) > fields[field]:
                    messagebox.showwarning("Warning", f"Value for '{field}' exceeds maximum length of {fields[field]} characters.")
                    return
                record[field] = new_value  # Update the record with the new value

        # Save the updated records back to the data file
        fm.save_data_file(self.current_db_name, self.records)
        messagebox.showinfo("Success", "Record edited successfully.")

    def delete_record(self):
        """Deletes a record from the opened database."""
        if not self.records:  # Check if records are available
            messagebox.showwarning("Warning", "No records available to delete.")
            return

        record_index = simpledialog.askinteger("Input", f"Enter the index of the record to delete (0 to {len(self.records) - 1}):")
        if record_index is None or record_index < 0 or record_index >= len(self.records):
            messagebox.showwarning("Warning", "Invalid record index.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the record at index {record_index}?")
        if confirm:
            del self.records[record_index]  # Delete the record
            # Save the updated records back to the data file
            fm.save_data_file(self.current_db_name, self.records)
            messagebox.showinfo("Success", "Record deleted successfully.")

    def display_all_records(self, fields):
        """Displays all records in a new window."""
        if not self.records:  # Check if there are records to display
            messagebox.showinfo("Info", "No records available to display.")
            return

        display_window = tk.Toplevel(self.master)
        display_window.title("All Records")

        for idx, record in enumerate(self.records):
            record_str = f"Record {idx}: " + ", ".join(f"{field}: {record[field]}" for field in fields)
            record_label = tk.Label(display_window, text=record_str)
            record_label.pack()

def main():
    root = tk.Tk()
    dbms_app = SimpleDBMS(root)
    root.mainloop()

if __name__ == "__main__":
    main()
