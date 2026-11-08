
# ==========================================
# 1. INITIAL DATA & ACCOUNTS
# ==========================================
lands = {
    "land1": {
        "city": "Taiz",
        "neighborhood": "Almoshky",
        "size": "1000 hector",
        "price": 10000
    },
    "land2": {
        "city": "Ibb",
        "neighborhood": "Alrodah",
        "size": "1200 hector",
        "price": 12000
    },
    "land3": {
        "city": "Taiz",
        "neighborhood": "alqadi valley",
        "size": "1500 hector",
        "price": 9000
    },
    "land4": {
        "city": "Ibb",
        "neighborhood": "almasbah",
        "size": "1400 hector",
        "price": 12500
    }
}

houses = {
    "house1": {
        "city": "taiz",
        "neighborhood": "almasbah",
        "floors": "3",
        "price": "1000",
        "number of apartments": "6"
    }
}

apartments = {
    "apartment1": {
        "city": "taiz",
        "neighborhood": "alrodah",
        "floor": "2",
        "price": "1000",
        "number of rooms": "6"
    }
}

sold_lands = {}
sold_houses = {}
sold_apartments = {}
request_of_purchase = {}  # Stores customer purchase requests
request_of_sell = {}      # Stores customer property sale offers

accounts = {
    "admin": {
        "name": "Mohammed AL-SHAMERI",
        "password": "moh4321",
        "email": "dofla@gmail.com",
        "phone": "730395069",
        "secretword": "CR7",
        "role": "manager"
    },
    "emp1": {
        "name": "Mohammed Al-sharafi",
        "email": "alsharfi@gmail.com",
        "phone": "778076278",
        "password": "messi10",
        "secretword": "M10",
        "role": "employee"
    },
    "emp2": {
        "name": "Mohammed Isameil",
        "email": "isameil@gmail.com",
        "phone": "734932753",
        "password": "5432167890",
        "secretword": "CR7",
        "role": "employee"
    },
    "emp3": {
        "name": "Mohaned Al-wajeh",
        "email": "mohaned@gmail.com",
        "phone": "735478626",
        "password": "ronaldo4321",
        "secretword": "CR7",
        "role": "employee"
    },
    "ten1": {
        "name": "Qusai",
        "email": "qousai@gmail.com",
        "phone": "770022891",
        "password": "11223344",
        "secretword": "M10",
        "role": "tenant",
        "property": apartments["apartment1"]
    },
    "cus1": {
        "name": "Ahmed",
        "password": "11223344",
        "secretword": "M10",
        "role": "customer"
    }
}


# ==========================================
# 2. FILE HANDLING FUNCTIONS
# ==========================================
# Save dictionary data to a text file before exiting
def save_to_file(file  , data):
    with open(file,'w') as f :
        for key , value in data.items():
            f.write(f"{key}:\n")
            for k,v in value.items():
                f.write(f"{k}:{v}\n")
            f.write("\n")    

# Load dictionary data from a text file at startup
def load_from_file(file):
    data = {}
    with open(file,'r') as f :
        lines = f.readlines()
    current_key = None
    for line in lines :
        line = line.strip()
        if not line :
                continue
        if line.endswith(":") and ":" not in line[:-1] :
                current_key= line[:-1].strip()
                data[current_key] ={}
        elif ":" in line and current_key :
            inner_key , value = line.split(":", 1)
            data[current_key] [inner_key.strip()]  = value.strip()

    return data            


# ==========================================
# 3. PROPERTY OPERATIONS
# ==========================================
# Prompt user to select a property category
def property_type():
    while True:
        print("\nCHOOSE PROPERTY TYPE:")
        print("1- Land")
        print("2- House")
        print("3- Apartment")
        print("0- Back")
        try:
            prop_type = int(input("Enter your choice: "))
            if 0 <= prop_type <= 3:
                return prop_type
            else:
                print("Invalid number, please enter 0-3")
        except ValueError:
            print("Please enter a valid number")

# Collect property details based on the selected property type
def input_property_data(property_type_num):
    data = {}
    data["city"] = input("Enter city: ").strip()
    data["neighborhood"] = input("Enter neighborhood: ").strip()
    while True:
        try:
            data["price"] = float(input("Enter price: ").strip())
            break
        except ValueError:
            print("Please enter a valid number for price")
    if property_type_num == 1:
        data["size"] = input("Enter size of land: ").strip()
    elif property_type_num == 2:
        data["floors"] = input("Enter number of floors: ").strip()
        data["number of apartments"] = input("Enter number of apartments: ").strip()
    elif property_type_num == 3:
        data["floor"] = input("Enter floor number: ").strip()
        data["number of rooms"] = input("Enter number of rooms: ").strip()
    return data

# Display formatted property records
def print_property_data(property_dict):
    if not property_dict:
        print("No properties available.")
        return
    for prop_name, prop_data in property_dict.items():
        print(f"\n{prop_name.upper()}:")
        for key, value in prop_data.items():
            print(f"{key.title()}: {value}")

# Sort and display properties by city, price, or default order
def sort_data(property):
    while True:
        print("SORTING OPTIONS:")
        print("1- Sort by city name")
        print("2- Sort by price")
        print("3- Display without sorting")
        print("0- Back")
        try:
            op = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number")
            continue 
        if op == 0:
            break
        elif op == 1:  # Sort by city name
            cities = set()
            for d in property.values():
                cities.add(d.get("city"))
            for c in sorted(cities):
                print(f"\n{c.upper()}:")
                for name, value in property.items():
                    if value["city"] == c:   
                        print(f"\n{name}:") 
                        for k, v in value.items():
                            print(f"{k.title()}: {v}")
            break
        elif op == 2:  # Sort by price
            prices ={} 
            for d in property.values() :
                prices.add(float(d.get("price")))
            prices.sort() 
            for p in prices : 
                for name , value in property.items() :
                    if float(value["price"]) == p :
                       print(f"\n{name} :")
                       for k , v in value.items() :
                           print(f"{k.title()}: {v}")
            break                
        elif op == 3:  # Display unsorted
            print_property_data(property)
            break
        else:
            print("Invalid choice, please enter 1, 2, 3, or 0")

# Search properties by city, neighborhood, price range, or full specifications
def search_property(property_dict, property_type_num):
    found = False
    print("\nSEARCH PROPERTIES:")
    print("1- By city name")
    print("2- By neighborhood name")
    print("3- By price range")
    print("4- Full search (all details)")
    print("0- Back")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    if choice == 0:
        return
    results = {}
    
    if choice == 1:  # Filter by city
        city = input("Enter city name: ").lower().strip()
        for name, data in property_dict.items():
            if data.get("city").lower().strip() == city:
                found = True
                results[name] = data
    
    elif choice == 2:  # Filter by neighborhood
        neighborhood = input("Enter neighborhood name: ").lower().strip()
        for name, data in property_dict.items():
            if data.get("neighborhood",).lower().strip() == neighborhood:
                found = True
                results[name] = data
    elif choice == 3:  # Filter by price range
        try:
            min_price = float(input("Enter minimum price: "))
            max_price = float(input("Enter maximum price: "))
        except ValueError:
            print("Invalid price input. Please enter numbers.")
            return   
        for name, data in property_dict.items():
            price = float(data.get("price", 0))
            if min_price <= price <= max_price:
                found = True
                results[name] = data
    
    elif choice == 4:  # Full attribute search
        print("Enter property details to search:")
        user_input = input_property_data(property_type_num)
        for name, data in property_dict.items():
            for key, value in user_input.items():
                if str(data.get(key, "")).lower().strip() != str(value).lower().strip():
                   found = True
                   results[name] = data
    else:
        print("Invalid choice. Please enter 1-4 or 0 to go back.")
        return
    if found:
        print("\nSEARCH RESULTS:")
        print_property_data(results)
    else:
        print("\nNo properties found matching your criteria.")
        return

# Add a new property listing to the corresponding category dictionary
def add_property():
    property_kind = property_type() 
    if property_kind == 0:
        return   
    property_name = input("Enter property name or ID: ").strip()
    property_data = input_property_data(property_kind)
    target_dict = None
    if property_kind == 1:
        target_dict = lands
        property_type_name = "land"
    elif property_kind == 2:
        target_dict = houses
        property_type_name = "house"
    else:
        target_dict = apartments
        property_type_name = "apartment"
    
    if property_name in target_dict:
        print(f"There is already a {property_type_name} with this name")
    else:
        target_dict[property_name] = property_data
        print(f"The {property_type_name} has been added successfully")

# Modify existing property attributes
def edit_property():
    property_kind = property_type()
    if property_kind == 0:
        return
    target_dict = None
    if property_kind == 1:
        target_dict = lands
        property_type_name = "land"
    elif property_kind == 2:
        target_dict = houses
        property_type_name = "house"
    else:
        target_dict = apartments
        property_type_name = "apartment"
    
    property_name = input(f"Enter {property_type_name} name: ").strip()
    
    if property_name not in target_dict:
        print(f"{property_type_name} not found")
        return
    
    while True:
        print(f"\nEDITING {property_name.upper()}:")
        print(target_dict[property_name])
        
        if property_kind == 1:
            print("\n1- City\n2- Neighborhood\n3- Size\n4- Price\n5- Save and Exit")
        elif property_kind == 2:
            print("\n1- City\n2- Neighborhood\n3- Floors\n4- Price\n5- Number of apartments\n6- Save and Exit")
        else:
            print("\n1- City\n2- Neighborhood\n3- Floor\n4- Price\n5- Number of rooms\n6- Save and Exit")
        
        try:
            op = int(input("Enter field to edit: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        if (property_kind == 1 and op == 5) or ((property_kind == 2 or property_kind == 3) and op == 6):
            break
        if op == 1:
            target_dict[property_name]["city"] = input("Enter new city: ").strip()
        elif op == 2:
            target_dict[property_name]["neighborhood"] = input("Enter new neighborhood: ").strip()
        elif op == 3:
            if property_kind == 1:
                target_dict[property_name]["size"] = input("Enter new size: ").strip()
            elif property_kind == 2:
                target_dict[property_name]["floors"] = input("Enter new number of floors: ").strip()
            else:
                target_dict[property_name]["floor"] = input("Enter new floor number: ").strip()
        elif op == 4:
            while True:
                try:
                    target_dict[property_name]["price"] = float(input("Enter new price: ").strip())
                    break
                except ValueError:
                    print("Please enter a valid number")
        elif op == 5 and property_kind != 1:
            if property_kind == 2:
                target_dict[property_name]["number of apartments"] = input("Enter new number of apartments: ").strip()
            else:
                target_dict[property_name]["number of rooms"] = input("Enter new number of rooms: ").strip()
        else:
            print("Invalid choice")
    
    print("Changes saved successfully")

# Move a property from available inventory to the sold archive
def check_property_sold():
    property_kind = property_type()
    if property_kind == 0:
        return
    
    target_dict = None
    sold_dict = None 
    property_type_name = ""
    
    if property_kind == 1:
        target_dict = lands
        sold_dict = sold_lands
        property_type_name = "land"
    elif property_kind == 2:
        target_dict = houses
        sold_dict = sold_houses
        property_type_name = "house"
    else:
        target_dict = apartments
        sold_dict = sold_apartments
        property_type_name = "apartment"
    
    property_name = input(f"Enter {property_type_name} name: ").strip()
    
    if property_name in target_dict:
        sold_dict[property_name] = target_dict[property_name]
        del target_dict[property_name]
        print(f"The {property_type_name} has been marked as sold")
    else:
        print(f"{property_type_name.capitalize()} not found")


# ==========================================
# 4. AUTHENTICATION & DISPLAY MENUS
# ==========================================
# Authenticate user credentials with a 3-attempt limit and secret word recovery
def login():
    attempts = 3
    while attempts > 0:
        print("="*50)
        print("LOGIN SYSTEM")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username in accounts:
            if accounts[username]["password"] == password:
                print(f"\nWelcome {accounts[username]['name']}!")
                return accounts[username]["role"]
            else:
                attempts -= 1
                print(f"Incorrect password. {attempts} attempts remaining.")
                if attempts > 0:
                    reset = input("Forgot password? (yes/no): ").lower().strip()
                    if reset == "yes":
                        secret = input("Enter your secret word: ").strip()
                        if secret == accounts[username]["secretword"]:
                            print(f"Your password is: {accounts[username]['password']}")
                        else:
                            print("Incorrect secret word.")
        else:
            print("Username not found.")
            attempts -= 1
    
    print("Too many failed attempts. Exiting.")
    return None

# Display role-specific dashboard options
def display_menu(user_role):
    print("="*50)
    if user_role == "manager":
        print("MANAGER DASHBOARD")
        print("1- Search for property")
        print("2- View all properties available")
        print("3- List a property for sale")
        print("4- Edit a property information")
        print("5- Confirm a property sale")
        print("6- Manage employee accounts")
        print("7- Manage customers accounts")
        print("0- Logout")
    elif user_role == "employee":
        print("EMPLOYEE DASHBOARD") 
        print("1- Search for properties")
        print("2- View properties (with filters)")
        print("3- List a property for sale")
        print("4- Edit a property information")
        print("5- Add a new tenant")
        print("6- Calculate a tenant payment")
        print("0- Logout")
    elif user_role == "tenant":
        print("TENANT DASHBOARD")
        print("1- View your property")
        print("2- View rent details")
        print("3- Auto calculate rent fees")
        print("4- Request contract renewal")
        print("5- Edit personal info")
        print("6- View payment history")
        print("0- Logout")
    elif user_role == "customer":
        print("CUSTOMER DASHBOARD")
        print("1- Search for available properties")
        print("2- Send purchase interest request")
        print("3- Request to show property for sale")
        print("4- Register or make inquiry")
        print("0- Logout")
    print("="*50)


# ==========================================
# 5. ACCOUNT & REQUEST MANAGEMENT
# ==========================================
# Manage employee accounts (view, add, edit, delete)
def employee_management():
    while True:  
        print("EMPLOYEE MANAGEMENT")
        print("1- View all employees information")
        print("2- Add a new employee")
        print("3- Edit employee information")
        print("4- Delete an employee account")
        print("5- Back")
        try:
            cho = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        if cho == 5:
            break   
        if cho == 1:
            print("VIEW EMPLOYEES:")
            print("1- View all employee data")
            print("2- View a specific employee data")
            print("0- Back")
            try:
                op = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a valid number")
                continue
            if op == 0:
                continue
            elif op == 1:
                print("ALL EMPLOYEES:")
                for id, data in accounts.items():
                    if data["role"] == "employee":
                        print(f"\n{id}:")
                        for k, v in data.items(): 
                            print(f"{k}: {v}")
            elif op == 2:
                ide = input("Enter employee id: ").strip().lower()
                if ide in accounts and accounts[ide]["role"] == "employee":
                    print(f"\n{ide}:")
                    for k, v in accounts[ide].items():
                        print(f"{k}: {v}")
                else:
                    print("Employee not found" )
            else: 
                print("Invalid choice")
                
        elif cho == 2:  # Add new employee
            print("ADD NEW EMPLOYEE:")
            id = input("Enter employee ID: ").strip()
            if id in accounts:
                print("This ID already exists")
                continue   
            name = input("Enter name of employee: ").strip()
            email = input("Enter email of employee: ").strip().lower()
            phone = input("Enter phone number of employee: ").strip()
            password = input("Enter password for employee: ").strip()
            secretword = input("Enter secret word for employee: ").strip()
            
            accounts[id] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": password,
                "secretword": secretword,
                "role": "employee"
            }
            print("Employee has been added successfully")

        elif cho == 3:  # Edit existing employee
            print("EDIT EMPLOYEE INFORMATION:")
            i = input("Enter id of employee: ").strip().lower()
            if i in accounts and accounts[i]["role"] == "employee":
                print(f"\nCurrent information for {i}:")
                for k, v in accounts[i].items():
                    print(f"{k}: {v}")
                
                print("\nEnter new information :")
                new_name = input("Enter new name :")
                new_email = input("Enter new email")
                new_phone = input("Enter new phone :")
                new_password = input("Enter new password")
                new_secretword = input("Enter new secret word")
                
                accounts[i]["name"] = new_name
                accounts[i]["email"] = new_email
                accounts[i]["phone"] = new_phone
                accounts[i]["password"] = new_password
                accounts[i]["secretword"] = new_secretword
                print("Employee information updated successfully")
            else:
                print("Employee not found")
                
        elif cho == 4:  # Delete employee account
            print("DELETE EMPLOYEE ACCOUNT:")
            idd = input("Enter id of employee: ").strip().lower()
            if idd in accounts and accounts[idd]["role"] == "employee":
                del accounts[idd]
                print("Employee account deleted successfully")
            else:
                print("Employee not found")
                
        else: 
            print("Invalid number, enter 1-5")

# Review customer purchase requests and approve property sale offers
def customer_management():
    while True:
        print("CUSTOMER MANAGEMENT:")
        print("1- View all purchase requests")
        print("2- View property offers")
        print("3- Confirm property offer")
        print("0- Back")
        try:
            t = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number")
            continue  
        if t == 0:
            break    
        if t == 1:  # View purchase requests
            if not request_of_purchase:
                print("No purchase requests available")
            else:
                print("PURCHASE REQUESTS:")
                for k, v in request_of_purchase.items():
                    print(f"\nCustomer: {accounts[k]['name']} (ID: {k})")
                    print("Requested Property:")
                    for i, d in v.items():
                        print(f"{i}: {d}")
        elif t == 2:  # View sale offers
            if not request_of_sell:
                print("No property offers available")
            else:
                print("PROPERTY OFFERS:")
                for k, v in request_of_sell.items():
                    print(f"\nProperty ID: {k}")
                    for i, d in v.items():
                        print(f"{i}: {d}")  
        elif t == 3:  # Approve a customer's sale offer and move it to active listings
            if not request_of_sell:
                print("No property offers available")
                continue   
            print("AVAILABLE OFFERS:")
            for k in request_of_sell.keys():
                print(f"- {k}")
            id = input("\nEnter ID of property to confirm: ").strip().lower()
            if id in request_of_sell:
                pk = property_type()
                if pk == 1:
                    lands[id] = request_of_sell[id]
                    del request_of_sell[id]
                    print("Property added to available lands")
                elif pk == 2:
                    houses[id] = request_of_sell[id]
                    del request_of_sell[id]
                    print("Property added to available houses")
                elif pk == 3:
                    apartments[id] = request_of_sell[id]
                    del request_of_sell[id]
                    print("Property added to available apartments")
                else:
                    print("Operation cancelled")
            else:
                print("Property not found") 
        else:
            print("Invalid choice")


# ==========================================
# 6. ROLE DASHBOARD CONTROLLERS
# ==========================================
# Handle Manager dashboard operations
def manager_menu():
    while True :
        display_menu("manager")
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        if c == 0:
            break    
        if c == 1:
            property_t = property_type()
            if property_t == 0:
                continue
            elif property_t == 1:
                search_property(lands, property_t)
            elif property_t == 2:
                search_property(houses, property_t)
            else:
                search_property(apartments, property_t)  
                      
        elif c == 2:
            property_k = property_type()
            if property_k == 0:
                continue
            elif property_k == 1: 
                sort_data(lands)
            elif property_k == 2:
                sort_data(houses) 
            else:
                sort_data(apartments)
            
        elif c == 3:
            add_property()
        elif c == 4:
            edit_property()
        elif c == 5:
            check_property_sold()
        elif c == 6:
            employee_management()
        elif c == 7:
            customer_management()
        else:
            print("Invalid choice. Please try again.")

# Handle Employee dashboard operations
def employee_menu():
    while True: 
        display_menu("employee")   
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        if c == 0:
            break   
        if c == 1:
            property_t = property_type()
            if property_t == 0:
                continue
            elif property_t == 1:
                search_property(lands, property_t)
            elif property_t == 2:
                search_property(houses, property_t)
            else:
                search_property(apartments, property_t)
                
        elif c == 2:
            property_k = property_type()
            if property_k == 0:
                continue
            elif property_k == 1:
                sort_data(lands)
            elif property_k == 2:
                sort_data(houses) 
            else:
                sort_data(apartments)       
                
        elif c == 3:
            add_property()
            
        elif c == 4:
            edit_property() 
            
        elif c == 5:  # Register a new tenant and link to an existing property
            print("ADD NEW TENANT:")
            id = input("Enter ID for new tenant: ").strip()
            if id in accounts:
                print("This ID already exists")
                continue   
            name = input("Enter name of tenant: ").strip()
            email = input("Enter email of tenant: ").strip().lower()
            phone = input("Enter phone number of tenant: ").strip()
            password = input("Enter password for tenant: ").strip()
            secretword = input("Enter secret word for tenant: ").strip()
            pr = property_type()
            if pr == 0:
                continue  
            property_id = None
            if pr == 1:
                property_id = input("Enter ID of land: ").strip().lower()
                if property_id not in lands:
                    print("Land not found")
                    continue
                property_data = lands[property_id]
            elif pr == 2:
                property_id = input("Enter ID of house: ").strip().lower()
                if property_id not in houses:
                    print("House not found")
                    continue
                property_data = houses[property_id]
            elif pr == 3:
                property_id = input("Enter ID of apartment: ").strip().lower()
                if property_id not in apartments:
                    print("Apartment not found")
                    continue
                property_data = apartments[property_id]
            
            accounts[id] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": password,
                "secretword": secretword,
                "role": "tenant",
                "property": property_data
            }
            print("Tenant added successfully")
            
        elif c == 6:  # Calculate monthly rent (10% of property price)
            print("CALCULATE TENANT PAYMENT:")
            tenant_id = input("Enter tenant ID: ").strip()
            if tenant_id in accounts and accounts[tenant_id]["role"] == "tenant":
                price = float(accounts[tenant_id]["property"].get("price", 0))
                print(f"\nTenant: {accounts[tenant_id]['name']}")
                print(f"Property Price: {price}")
                print(f"Monthly Rent: {price * 0.1}")
            else:
                print("Tenant not found")
        else:
            print("Invalid choice")

# Handle Tenant dashboard operations
def tenant_menu():
    tenant_id = None
    for id, data in accounts.items():
        if data["role"] == "tenant":
            tenant_id = id
            break
    
    if not tenant_id:
        print("No tenant account found")
        return
        
    while True: 
        display_menu("tenant")
        
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        
        if c == 0:
            break
            
        if c == 1:  # View leased property details
            print("YOUR PROPERTY:")
            for k, v in accounts[tenant_id]["property"].items():
                print(f"{k}: {v}")     
        elif c == 2:  # View rent breakdown (10% monthly, 20% deposit)
            price = float(accounts[tenant_id]["property"].get("price", 0))
            print("RENT DETAILS:")
            print(f"Monthly Rent: {price * 0.1}")
            print(f"Annual Rent: {price * 0.1 * 12}")
            print(f"Security Deposit: {price * 0.2}")
        elif c == 3:  # Calculate total rent for a custom number of months
            price = float(accounts[tenant_id]["property"].get("price", 0))
            months = int(input("Enter number of months: "))
            print(f"\nTotal rent for {months} months: {price * 0.1 * months}")
        elif c == 4:
            print("Contract renewal request has been sent to management.")   
        elif c == 5:  # Update personal profile information
            print("EDIT PERSONAL INFORMATION:")
            print("\nCurrent information:")
            for k, v in accounts[tenant_id].items():
                if k not in ["property", "role"]:
                    print(f"{k.title()}: {v}")
            
            print("\nEnter new information (leave blank to keep current):")
            new_name = input(f"Enter new name : ")
            new_email = input(f"Enter new email : ")
            new_phone = input(f"Enter new phone :")
            new_password = input("Enter new password:")
            new_secretword = input("Enter new secretword : ")
            
            accounts[tenant_id]["name"] = new_name
            accounts[tenant_id]["email"] = new_email
            accounts[tenant_id]["phone"] = new_phone
            accounts[tenant_id]["password"] = new_password
            accounts[tenant_id]["secretword"] = new_secretword
            print("Information updated successfully")
        elif c == 6:
            print("PAYMENT HISTORY:")
            print("No payment history available")            
        else:
            print("Invalid choice")

# Handle Customer dashboard operations
def customer_menu():
    while True: 
        display_menu("customer")
        
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        
        if c == 0:
            break
            
        if c == 1:
            property_t = property_type()
            if property_t == 0:
                continue
            elif property_t == 1:
                search_property(lands, property_t)
            elif property_t == 2:
                search_property(houses, property_t)
            else:
                search_property(apartments, property_t)
                
        elif c == 2:  # Submit a purchase request for an available property
            customer_id = input("Enter your customer ID: ").strip()
            if customer_id not in accounts or accounts[customer_id]["role"] != "customer":
                print("Customer not found")
                continue
                
            prop = property_type()
            if prop == 0:
                continue
                
            if prop == 1:
                print_property_data(lands)
                id = input("Enter ID of property you're interested in: ").strip()
                if id in lands:
                    request_of_purchase[customer_id] = lands[id]
                    print("Your request has been sent successfully")
                else:
                    print("Property not found")
            elif prop == 2:
                print_property_data(houses)
                id = input("Enter ID of property you're interested in: ").strip()
                if id in houses:
                    request_of_purchase[customer_id] = houses[id]
                    print("Your request has been sent successfully")
                else:
                    print("Property not found")
            elif prop == 3:
                print_property_data(apartments)
                id = input("Enter ID of property you're interested in: ").strip()
                if id in apartments:
                    request_of_purchase[customer_id] = apartments[id]
                    print("Your request has been sent successfully")
                else:
                    print("Property not found")
            
        elif c == 3:  # Submit an offer to list a customer's property for sale
            print("SELL PROPERTY REQUEST")
            pt = property_type()
            if pt == 0:
                continue
                
            id = input("Enter ID for the property: ").strip().lower()
            if (pt == 1 and id in lands) or (pt == 2 and id in houses) or (pt == 3 and id in apartments):
                print("This property already exists in our system")
                continue    
            data = input_property_data(pt)
            request_of_sell[id] = data
            print("Your request has been submitted. We will contact you soon.")   
        elif c == 4:  # Register a new customer account
            print("REGISTER NEW CUSTOMER:")
            id = input("Enter customer ID: ").strip()
            if id in accounts:
                print("This ID already exists")
                continue
                
            name = input("Enter your name: ").strip()
            password = input("Enter password: ").strip()
            secretword = input("Enter secret word for password recovery: ").strip()
            
            accounts[id] = {
                "name": name,
                "password": password,
                "secretword": secretword,
                "role": "customer"
            }
            print("Registration successful. You can now login with your credentials.")       
        else:
            print("Invalid choice")


# ==========================================
# 7. MAIN APPLICATION LOOP
# ==========================================
# Load data from files, run the main login loop, and save data on exit
def main():
    lands = load_from_file("property_l.txt") 
    houses = load_from_file("property_houses.txt")
    apartments = load_from_file("property_apartment.txt")
    sold_lands = load_from_file("sold.property.lands.txt")
    sold_houses= load_from_file("sold.property.houses.txt")
    sold_apartments= load_from_file("sold.property.apartments.txt")
    request_of_purchase = load_from_file("purchase_requsets.txt")
    request_of_sell =  load_from_file("offers_requset.txt")
    accounts= load_from_file("users.account.txt")
    while True:
        print("="*50)
        print("PROPERTY MANAGEMENT SYSTEM")
        print("1- Login")
        print("0- Exit")
        print("="*50)
        
        try:
            option = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        
        if option == 0:
            save_to_file("property_l.txt",lands)
            save_to_file("property_houses.txt",houses)
            save_to_file("property_apartment.txt",apartments)
            save_to_file("users.account.txt",accounts)
            save_to_file("sold.property.lands.txt",sold_lands)
            save_to_file("sold.property.houses.txt",sold_houses)
            save_to_file("sold.property.apartments.txt",sold_apartments)
            save_to_file("purchase_requsets.txt",request_of_purchase)
            save_to_file("offers_requset.txt",request_of_sell)
            print("Thank you for using our system. Goodbye!")
            break
            
        elif option == 1:
            role = login()
            if role == "manager":
                manager_menu()
            elif role == "employee":
                employee_menu()
            elif role == "tenant":
                tenant_menu()
            elif role == "customer":
                customer_menu()
                
        else:
            print("Invalid option. Please try again.")


main()
