contacts = []

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email address: ")
    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact)
    print("Contact added successfully!\n")

def view_contacts():
    if not contacts:
        print("No contacts found.\n")
        return
    print("\nContact List:")
    for idx, contact in enumerate(contacts, start=1):
        print(f"{idx}. Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}")
    print()

def update_contact():
    view_contacts()
    if not contacts:
        return
    try:
        choice = int(input("Enter the number of the contact to update: "))
        if 1 <= choice <= len(contacts):
            contact = contacts[choice - 1]
            contact['name'] = input(f"Enter new name (current: {contact['name']}): ") or contact['name']
            contact['phone'] = input(f"Enter new phone (current: {contact['phone']}): ") or contact['phone']
            contact['email'] = input(f"Enter new email (current: {contact['email']}): ") or contact['email']
            print("Contact updated successfully!\n")
        else:
            print("Invalid contact number.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def delete_contact():
    view_contacts()
    if not contacts:
        return
    try:
        choice = int(input("Enter the number of the contact to delete: "))
        if 1 <= choice <= len(contacts):
            deleted = contacts.pop(choice - 1)
            print(f"Deleted contact: {deleted['name']}\n")
        else:
            print("Invalid contact number.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def main():
    while True:
        print("Contact Management System")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_contact()
        elif choice == '2':
            view_contacts()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "_main_":
    main()