import json
import csv
import os

# Pre-defined denominations
DENOMINATIONS = [10, 20, 50, 100, 200, 500, 1000]

def main():
    notes = {}
    filename = "money_data.json"
    
    # Load previous data
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            notes = data.get('notes', {})
            # Load custom denominations if exists
            if 'denominations' in data:
                global DENOMINATIONS
                DENOMINATIONS = sorted(data['denominations'])
        print("\n> Previous data loaded successfully!")
    
    while True:
        print("\n--- Money Calculator ---")
        print("1: Add Notes")
        print("2: Remove Notes")
        print("3: Show Calculation")
        print("4: Reset Data")
        print("5: Save Data")
        print("6: Export to CSV")
        print("7: Add New Denomination")
        print("8: Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        
        # Add notes
        if choice == '1':
            add_notes(notes)
        
        # Remove notes
        elif choice == '2':
            remove_notes(notes)
        
        # Show calculation
        elif choice == '3':
            show_calculation(notes)
        
        # Reset
        elif choice == '4':
            notes = {}
            print("\n> All data has been reset!")
        
        # Save
        elif choice == '5':
            save_data(notes, filename)
        
        # CSV Export
        elif choice == '6':
            export_to_csv(notes)
        
        # Add new denomination
        elif choice == '7':
            add_new_denomination()
        
        # Exit
        elif choice == '8':
            save_data(notes, filename)
            print("\n> Your data has been saved. Exiting...")
            break
        
        else:
            print("\n> Invalid choice! Please enter a number between 1-8")

def add_notes(notes):
    print("\n--- Add Notes ---")
    print("Available denominations:", ", ".join(map(str, sorted(DENOMINATIONS))))
    
    try:
        denom = int(input("Enter note value: "))
            
        count = int(input("Enter number of notes: "))
        if count < 0:
            print("> Number must be 0 or greater!")
            return
            
        notes[denom] = notes.get(denom, 0) + count
        print(f"> Added: {count} notes of {denom} taka")
    
    except ValueError:
        print("> Please enter valid numbers!")

def remove_notes(notes):
    print("\n--- Remove Notes ---")
    if not notes:
        print("> No notes added yet!")
        return
        
    try:
        # Show available denominations that have notes
        available_denoms = [str(d) for d in sorted(notes.keys())]
        print("Available denominations with notes:", ", ".join(available_denoms))
        
        denom = int(input("Enter note value to remove: "))
        if denom not in notes:
            print(f"> No {denom} taka notes available!")
            return
            
        current_count = notes[denom]
        count = int(input(f"Enter quantity to remove (available: {current_count}): "))
        
        if count > current_count:
            print(f"> Only {current_count} notes available!")
        else:
            notes[denom] -= count
            if notes[denom] == 0:
                del notes[denom]
            print(f"> Removed: {count} notes of {denom} taka")
    
    except ValueError:
        print("> Please enter valid numbers!")

def show_calculation(notes):
    if not notes:
        print("\n> No notes added yet!")
        return
        
    total = 0
    total_notes = 0
    
    print("\n--- Calculation ---")
    for denom, count in sorted(notes.items(), reverse=True):
        amount = denom * count
        total += amount
        total_notes += count
        print(f"{denom} taka notes: {count} pcs = {amount} taka")
    
    print(f"\nTotal Notes: {total_notes} pcs")
    print(f"Total Amount: {total} taka")

def save_data(notes, filename):
    # Save both notes and denominations
    data = {
        'notes': notes,
        'denominations': DENOMINATIONS
    }
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"\n> Data saved to '{filename}'!")

def export_to_csv(notes):
    if not notes:
        print("\n> No notes added yet!")
        return
        
    filename = "money_export.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Note Value", "Quantity", "Total Amount"])
        
        for denom, count in sorted(notes.items(), reverse=True):
            writer.writerow([denom, count, denom * count])
        
        # Total row
        total = sum(denom * count for denom, count in notes.items())
        writer.writerow(["TOTAL", sum(notes.values()), total])
    
    print(f"\n> Data exported to '{filename}'!")

def add_new_denomination():
    print("\n--- Add New Denomination ---")
    print("Current denominations:", ", ".join(map(str, sorted(DENOMINATIONS))))
    
    try:
        new_denom = int(input("Enter new note value: "))
        
        if new_denom <= 0:
            print("> Value must be positive!")
            return
            
        if new_denom in DENOMINATIONS:
            print(f"> {new_denom} taka note already exists!")
            return
            
        DENOMINATIONS.append(new_denom)
        print(f"> Added new denomination: {new_denom} taka")
        print("Updated denominations:", ", ".join(map(str, sorted(DENOMINATIONS))))
    
    except ValueError:
        print("> Please enter a valid number!")

if __name__ == "__main__":
    main()