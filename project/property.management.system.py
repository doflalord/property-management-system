#محمد عبدالقادر هزاع
#محمد بسام شرف 
#محمد اسماعيل محمد
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
request_of_purchase = {} #طلبات شراء من الزبائن
request_of_sell = {}#طلبات عرض عقارات في البرنامج

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
def save_to_file(file  , data): #دالة حفظ المعلومات قبل الخروج
    with open(file,'w') as f :
        for key , value in data.items():
            f.write(f"{key}:\n")
            for k,v in value.items():
                f.write(f"{k}:{v}\n")
            f.write("\n")    

def load_from_file(file): #تحميل المعلومات من الملفات عن البدء
    data = {}
    with open(file,'r') as f :
        lines = f.readlines()
    current_key = None
    for line in lines :
        line = line.strip() #حذف المسافات البيضاء لكل سطر
        if not line :
                continue
        if line.endswith(":") and ":" not in line[:-1] :
                current_key= line[:-1].strip()
                data[current_key] ={}
        elif ":" in line and current_key :
            inner_key , value = line.split(":", 1)
            data[current_key] [inner_key.strip()]  = value.strip()

    return data            

def property_type(): #دالة معرفة نوع العقار
    while True:
        print("\nCHOOSE PROPERTY TYPE:")#اختار نوع العقار
        print("1- Land")#ارض
        print("2- House")#منزل
        print("3- Apartment")#شقة
        print("0- Back")#رجوع
        try:
            prop_type = int(input("Enter your choice: "))
            if 0 <= prop_type <= 3:
                return prop_type
            else:
                print("Invalid number, please enter 0-3")
        except ValueError:
            print("Please enter a valid number")

def input_property_data(property_type_num): #دالة ادخال بيانات العقارات 
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
        data["floors"] = input("Enter number of floors: ").strip() #ادخل عدد الطوابق
        data["number of apartments"] = input("Enter number of apartments: ").strip()
    elif property_type_num == 3:
        data["floor"] = input("Enter floor number: ").strip()
        data["number of rooms"] = input("Enter number of rooms: ").strip()
    return data

def print_property_data(property_dict):#دالة طباعة العقارات 
    if not property_dict:
        print("No properties available.") #لا يوجد عقارات
        return
    for prop_name, prop_data in property_dict.items():
        print(f"\n{prop_name.upper()}:")
        for key, value in prop_data.items():
            print(f"{key.title()}: {value}")

def sort_data(property):#دالة عرض العقارات 
    while True:
        print("SORTING OPTIONS:")
        print("1- Sort by city name") #ترتيب ب اسم المدينة 
        print("2- Sort by price")#ترتيب بالسعر
        print("3- Display without sorting")#بدون الترتيب
        print("0- Back")   #رجوع
        try:
            op = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number")
            continue 
        if op == 0:
            break
        elif op == 1: #الترتيب ب اسم المدينة
            cities = set() #المدن
            for d in property.values():
                cities.add(d.get("city"))#ضيف المدينة الى مجموعه المدن
            for c in sorted(cities):
                print(f"\n{c.upper()}:")
                for name, value in property.items():
                    if value["city"] == c:   
                        print(f"\n{name}:") 
                        for k, v in value.items():
                            print(f"{k.title()}: {v}")
            break
        elif op == 2: #الترتيب ب السعر
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
        elif op == 3: #بدون ترتيب
            print_property_data(property)
            break
        else:
            print("Invalid choice, please enter 1, 2, 3, or 0")

def search_property(property_dict, property_type_num):#دالة البحث عن عقار
    found = False
    print("\nSEARCH PROPERTIES:")#اختار طريقة البحث
    print("1- By city name") #البحث ب اسم المدينة
    print("2- By neighborhood name") #البحث ب اسم الحي 
    print("3- By price range")#البحث ب السعر
    print("4- Full search (all details)") #البحث بكامل التفاصيل 
    print("0- Back")#الرجوع
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    if choice == 0:
        return
    results = {} #ديكشنري لتخزين نتائج البحث
    
    if choice == 1: # البحث ب اسم المدينة
        city = input("Enter city name: ").lower().strip() #ادخل اسم المدينة
        for name, data in property_dict.items():
            if data.get("city").lower().strip() == city: #مقارنة بين المدينة التي ادخلها المستخدم والمدينة المسجلة ببيانات العقار
                found = True
                results[name] = data
    
    elif choice == 2: #البحث ب اسم الحي
        neighborhood = input("Enter neighborhood name: ").lower().strip() #ادخل اسم الحي
        for name, data in property_dict.items():
            if data.get("neighborhood",).lower().strip() == neighborhood:
                found = True
                results[name] = data
    elif choice == 3: #البحث بالسعر
        try:
            min_price = float(input("Enter minimum price: ")) #ادخل الحد الادنى من السعر
            max_price = float(input("Enter maximum price: "))#ادخل الحد الاقصى من السعر
        except ValueError:
            print("Invalid price input. Please enter numbers.")
            return   
        for name, data in property_dict.items():
            price = float(data.get("price", 0))
            if min_price <= price <= max_price:
                found = True
                results[name] = data
    
    elif choice == 4: #البحث بكامل التفاصيل
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

def add_property(): #دالة اضافة عقار 
    property_kind = property_type() 
    if property_kind == 0:
        return   
    property_name = input("Enter property name or ID: ").strip()#ادخل اسم العقار
    property_data = input_property_data(property_kind)#يطلب من المستخد ادخال بيانات العقار من الدالة
    target_dict = None #الديكشنري المستهدف
    if property_kind == 1:
        target_dict = lands
        property_type_name = "land"
    elif property_kind == 2:
        target_dict = houses
        property_type_name = "house"
    else:
        target_dict = apartments
        property_type_name = "apartment"
    
    if property_name in target_dict: #اذا كان اسم العقار موجود بالديكشنري المستهدف
        print(f"There is already a {property_type_name} with this name")
    else:
        target_dict[property_name] = property_data
        print(f"The {property_type_name} has been added successfully")

def edit_property():#تعديل عقار معين
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
    
    property_name = input(f"Enter {property_type_name} name: ").strip() #ادخل اسم العقار الذي تود ان تعدل عليه
    
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

def check_property_sold(): #دالة تأكيد بيع عقار 
    property_kind = property_type()
    if property_kind == 0:
        return
    
    target_dict = None #الديكشنري المستهدف لاشي
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
    
    property_name = input(f"Enter {property_type_name} name: ").strip() #ادخل اسم العقار 
    
    if property_name in target_dict:
        sold_dict[property_name] = target_dict[property_name]
        del target_dict[property_name]
        print(f"The {property_type_name} has been marked as sold")
    else:
        print(f"{property_type_name.capitalize()} not found")

def login(): #تسجيل الدخول
    attempts = 3 #ثلاث محاولات لتسجيل الدخول
    while attempts > 0:
        print("="*50)
        print("LOGIN SYSTEM")
        username = input("Username: ").strip() #ادخل اسم المستخدم
        password = input("Password: ").strip()#ادخل كلمة المرور
        
        if username in accounts:#اذا كان اليوزر في الحسابات 
            if accounts[username]["password"] == password:
                print(f"\nWelcome {accounts[username]['name']}!")
                return accounts[username]["role"] #ارجع دور المستخدم
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

def display_menu(user_role): #دالة عرض القائمة للمستخدم
    print("="*50)
    if user_role == "manager": #اذا كان المستخدم مدير
        print("MANAGER DASHBOARD")
        print("1- Search for property") #البحث عن عقار 
        print("2- View all properties available") #عرض العقارات المتاحه
        print("3- List a property for sale")#اضافه عقار 
        print("4- Edit a property information")#تعديل عقار 
        print("5- Confirm a property sale")#تأكيد بيع عقار 
        print("6- Manage employee accounts")#ادارة الموظفين 
        print("7- Manage customers accounts")  #ادارة الزبائن
        print("0- Logout")#الخروج
    elif user_role == "employee": #اذا كان المستخدم موظف
        print("EMPLOYEE DASHBOARD") 
        print("1- Search for properties")#البحث عن عقار 
        print("2- View properties (with filters)")#عرض العقارات 
        print("3- List a property for sale")#اضافه عقار 
        print("4- Edit a property information")#تعديل بيانات عقار
        print("5- Add a new tenant")#اضافه مستأجر
        print("6- Calculate a tenant payment")#حساب الايجار لمستأجر
        print("0- Logout")#الخروج
    elif user_role == "tenant": #اذا كان المستخدم مستأجر
        print("TENANT DASHBOARD")
        print("1- View your property") #عرض العقار الخاص فيه
        print("2- View rent details")#عرض تفاصيل الايجار
        print("3- Auto calculate rent fees")#حساب الرسوم للعقار حقه
        print("4- Request contract renewal")#طلب تجديد عقد الايجار
        print("5- Edit personal info")#تعديل بيانات الخاصه به
        print("6- View payment history")#عرض تاريخ الرسوم
        print("0- Logout")
    elif user_role == "customer":#اذا كان المستخدم زبون
        print("CUSTOMER DASHBOARD")
        print("1- Search for available properties")#البحث عن عقار متاح للشراء
        print("2- Send purchase interest request")#ارسال طلب اهتمام بشراء عقار
        print("3- Request to show property for sale")#طلب عرض عقار للبيع في البرنامج
        print("4- Register or make inquiry")#تسجيل زبون 
        print("0- Logout")#خروج
    print("="*50)

def employee_management(): #دالة ادارة الموظفين
    while True:  
        print("EMPLOYEE MANAGEMENT") #ادارة الموظفين
        print("1- View all employees information")#عرض الموظفين 
        print("2- Add a new employee")#اضاف موظف جديد
        print("3- Edit employee information")#تعديل بيانات موظف
        print("4- Delete an employee account") #حذف حساب موظف
        print("5- Back")#رجوع  
        try:
            cho = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        if cho == 5:
            break   
        if cho == 1:
            print("VIEW EMPLOYEES:")
            print("1- View all employee data") #عرض بيانات الموظفين كامل
            print("2- View a specific employee data")#عرض بيانات موظف فقط
            print("0- Back") #رجوع
            try:
                op = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a valid number")
                continue
            if op == 0:
                continue
            elif op == 1: #عرض بيانات حسابات الموظفين كامل
                print("ALL EMPLOYEES:")
                for id, data in accounts.items():
                    if data["role"] == "employee":#اذا كان الحساب دوره موظف
                        print(f"\n{id}:") #اطبع الايدي حقه
                        for k, v in data.items(): 
                            print(f"{k}: {v}") #اطبع بيانات حسابة
            elif op == 2: #عرض بيانات حساب موظف معين
                ide = input("Enter employee id: ").strip().lower() #ادخل ايدي الموظف المراد طباعة معلوماته
                if ide in accounts and accounts[ide]["role"] == "employee":#اذا كان الايدي موجود في ديكشنري الحسابات ودوره موظف
                    print(f"\n{ide}:")#اطبع الايدي حقه
                    for k, v in accounts[ide].items():
                        print(f"{k}: {v}")#اطبع بياناته
                else: #في حالة عدم وجود ايدي الموظف
                    print("Employee not found" ) #اطبع الموظف غير موجود
            else: 
                print("Invalid choice")
                
        elif cho == 2: #اضافه موظف جديد
            print("ADD NEW EMPLOYEE:") #اضافة موظف جديد
            id = input("Enter employee ID: ").strip() #ادخل ايدي الموظف الجديد
            if id in accounts: #اذا كان الايدي هذا مسجل من قبل
                print("This ID already exists")#اطبع يوجد ايدي مسجل بهذا الاسم
                continue   
            name = input("Enter name of employee: ").strip() #ادخل اسم الموظف
            email = input("Enter email of employee: ").strip().lower()#ادخل ايميل الموظف
            phone = input("Enter phone number of employee: ").strip()#ادخل رقم الموظف 
            password = input("Enter password for employee: ").strip()#ادخل كلمة مرور للموظف
            secretword = input("Enter secret word for employee: ").strip()#ادخل كلمة سر للمستخدم
            
            accounts[id] = {   #ضف معلومات الموظف الجديد الى ديكشنري الحسابات
                "name": name,
                "email": email,
                "phone": phone,
                "password": password,
                "secretword": secretword,
                "role": "employee"
            }
            print("Employee has been added successfully") #الموظف تم اضافته بنجاح

        elif cho == 3: #تعديل بيانات موظف ما
            print("EDIT EMPLOYEE INFORMATION:")
            i = input("Enter id of employee: ").strip().lower() #ادخل ايدي الموظف المراد تعديل بياناته
            if i in accounts and accounts[i]["role"] == "employee": #اذا كان الايدي موجود في الحسابات وكان دوره موظف
                print(f"\nCurrent information for {i}:") #المعلومات الحاليه للموظف
                for k, v in accounts[i].items(): #اعمل لوب لبيانات ايدي الموظف هذا
                    print(f"{k}: {v}") #اطبع بياناته
                
                print("\nEnter new information :")#ادخل المعلومات الجديده للموظف
                new_name = input("Enter new name :") #ادخل الاسم الجديد 
                new_email = input("Enter new email")#ادخل الايميل الجديد
                new_phone = input("Enter new phone :")#ادخل الرقم الجديد 
                new_password = input("Enter new password")#ادخل كلمة السر الجديده له
                new_secretword = input("Enter new secret word")#ادخل كلمة سر مساعده
                
                accounts[i]["name"] = new_name #عدل الاسم الجديد في الحساب
                accounts[i]["email"] = new_email#عدل الايميل الجديد للموظف
                accounts[i]["phone"] = new_phone#ادخل الرقم الجديد
                accounts[i]["password"] = new_password
                accounts[i]["secretword"] = new_secretword
                print("Employee information updated successfully")
            else:
                print("Employee not found")
                
        elif cho == 4: #حذف حساب موظف
            print("DELETE EMPLOYEE ACCOUNT:")
            idd = input("Enter id of employee: ").strip().lower() #ادخل ايدي الموظف المراد حذفه
            if idd in accounts and accounts[idd]["role"] == "employee": #اذا كان الايدي موجود في الحسابات وكان دوره موظف
                del accounts[idd] #احذف الحساب للايدي هذا
                print("Employee account deleted successfully")#تم حذف الحساب
            else:
                print("Employee not found")#لايوجد حساب بهذا الايدي
                
        else: 
            print("Invalid number, enter 1-5")

def customer_management():#دالة ادارة الزبائن
    while True:
        print("CUSTOMER MANAGEMENT:")
        print("1- View all purchase requests")#عرض طلبات الشراء من الزبائن
        print("2- View property offers")#طلبات عرض بيع عقار في البرنامج
        print("3- Confirm property offer")#تأكيد قبول لطلب عرض عقار في البرنامج
        print("0- Back")  #رجوع
        try:
            t = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number")
            continue  
        if t == 0:
            break    
        if t == 1:#عرض طلبات شراء من الزبائن
            if not request_of_purchase:#اذا كان لايوجد طلبات متاحه
                print("No purchase requests available")#لايوجد طلبات
            else: #في حال وجود طلبات
                print("PURCHASE REQUESTS:")
                for k, v in request_of_purchase.items(): #اعمل لوب في الطلبات
                    print(f"\nCustomer: {accounts[k]['name']} (ID: {k})") #اطبع اسم الزبون والايدي حقه
                    print("Requested Property:")
                    for i, d in v.items():
                        print(f"{i}: {d}") #اطبع معلومات العقار المراد شراءه من قبل الزبون
        elif t == 2:
            if not request_of_sell:#اذا كان لايوجد عروض 
                print("No property offers available")#لايوجد عروض
            else:#في حال وجود عروض بيع
                print("PROPERTY OFFERS:")
                for k, v in request_of_sell.items():#اعمل لوب للعروض
                    print(f"\nProperty ID: {k}") #اطبع الايدي حق العقار المراد بيعه
                    for i, d in v.items():
                        print(f"{i}: {d}")  #اطبع معلومات العقار  
        elif t == 3:#تاكيد طلب عرض عقار في البرنامج
            if not request_of_sell:#اذا كان لايوجد عروض
                print("No property offers available")#لايوجد عروض
                continue   
            print("AVAILABLE OFFERS:")#العروض المتاحه
            for k in request_of_sell.keys():
                print(f"- {k}") #اطبع الايديهات حق العقارات المعروضه للبيع 
            id = input("\nEnter ID of property to confirm: ").strip().lower() #ادخل الايدي حق العقار اللي تريد تاكيد عرضه في البرنامج
            if id in request_of_sell:#اذا كان الايدي موجود في العروض
                pk = property_type() #ادخل نوع العقار
                if pk == 1:#اذا كان نوع العقار اراضي 
                    lands[id] = request_of_sell[id] #اضف العقار الى البرنامج
                    del request_of_sell[id] #واحذفه من العروض
                    print("Property added to available lands")#تم اضافه العقار الى البرنامج
                elif pk == 2: #اذا كان نوع العقار منازل
                    houses[id] = request_of_sell[id]#اضف المنزل الى منازل البرنامج
                    del request_of_sell[id]#واحذفه من العروض
                    print("Property added to available houses")
                elif pk == 3:#اذا كان العقار نوعه شقه
                    apartments[id] = request_of_sell[id] #اضف الشقه الى البرنامج
                    del request_of_sell[id]#واحذفه من العروض
                    print("Property added to available apartments")
                else:
                    print("Operation cancelled")
            else:
                print("Property not found") 
        else:
            print("Invalid choice")

def manager_menu():# دالة عمليات المدير
    while True :
        display_menu("manager")  #دالة عرض الخيارات المتاحه للمدير
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        if c == 0:
            break    
        if c == 1: # البحث عن عقار
            property_t = property_type() #دالة معرفة نوع العقار
            if property_t == 0:
                continue
            elif property_t == 1: # نوع العقار ارض
                search_property(lands, property_t) #دالة البحث عن عقار
            elif property_t == 2:
                search_property(houses, property_t)
            else:
                search_property(apartments, property_t)  
                      
        elif c == 2:# عرض العقارات 
            property_k = property_type()
            if property_k == 0:
                continue
            elif property_k == 1: 
                sort_data(lands)#دالة ترتيب العقارات وطباعتها
            elif property_k == 2:
                sort_data(houses) 
            else:
                sort_data(apartments)
            
        elif c == 3: #اضافة عقار 
            add_property() #دالة اضاف عقار
        elif c == 4: #تعديل عقار 
            edit_property()#دالة تعديل عقار
        elif c == 5: #تأكيد بيع عقار 
            check_property_sold()#دالة تأكيد بيع عقار  
        elif c == 6: #ادارة الموظفيين
            employee_management()#دالةادارة الموظفيين
        
        elif c == 7: #ادارة الزبائن
            customer_management()#دالة ادارة الزبائن
            
        else:
            print("Invalid choice. Please try again.")

def employee_menu(): #قائمة الموظف
    while True: 
        display_menu("employee")   
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        if c == 0:
            break   
        if c == 1: #البحث عن عقار
            property_t = property_type()
            if property_t == 0:
                continue
            elif property_t == 1:
                search_property(lands, property_t)
            elif property_t == 2:
                search_property(houses, property_t)
            else:
                search_property(apartments, property_t)
                
        elif c == 2:#عرض العقارات
            property_k = property_type()
            if property_k == 0:
                continue
            elif property_k == 1:
                sort_data(lands)
            elif property_k == 2:
                sort_data(houses) 
            else:
                sort_data(apartments)       
                
        elif c == 3:#اضافه عقار
            add_property()
            
        elif c == 4:#تعديل عقار معين
            edit_property() 
            
        elif c == 5: #اضافة مستأجر
            print("ADD NEW TENANT:")
            id = input("Enter ID for new tenant: ").strip() #ادخل الايدي حق  المستأجر الذي تريد اضافته
            if id in accounts:#اذا يوجد ايدي بنفس هذا الايدي
                print("This ID already exists")#اطبع يوجد ايدي مسجل بهذا
                continue   
            name = input("Enter name of tenant: ").strip()#اسم المستأجر
            email = input("Enter email of tenant: ").strip().lower()#الايميل
            phone = input("Enter phone number of tenant: ").strip()#الرقم
            password = input("Enter password for tenant: ").strip()#كلمة المرور
            secretword = input("Enter secret word for tenant: ").strip()    #كلمة مرور احتياطيه
            pr = property_type()
            if pr == 0:
                continue  
            property_id = None
            if pr == 1: #اذا كان نوع العقار ارض
                property_id = input("Enter ID of land: ").strip().lower()#ادخل ايدي الارض المستأجره
                if property_id not in lands: #اذا كان ايدي العقار لايوجد في الاراضي
                    print("Land not found")#لا يوجد ارض بهذا الايدي
                    continue
                property_data = lands[property_id]#خذ بيانات الارض 
            elif pr == 2:#اذا كان نوع العقار منزل
                property_id = input("Enter ID of house: ").strip().lower()#ادخل ايدي المنزل
                if property_id not in houses:
                    print("House not found")
                    continue
                property_data = houses[property_id]#خذ بيانات المنزل
            elif pr == 3:    #اذا كان نوع العقار شقه
                property_id = input("Enter ID of apartment: ").strip().lower()#ادخل ايدي الشقه
                if property_id not in apartments:
                    print("Apartment not found")
                    continue
                property_data = apartments[property_id]#خذ معلومات الشقه
            
            accounts[id] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": password,
                "secretword": secretword,
                "role": "tenant",
                "property": property_data #معلومات عقار المستأجر
            }
            print("Tenant added successfully")#تم اضافه المستأجر
            
        elif c == 6:#حساب رسوم المستأجر
            print("CALCULATE TENANT PAYMENT:")
            tenant_id = input("Enter tenant ID: ").strip()#ادخل ايدي المستأجر
            if tenant_id in accounts and accounts[tenant_id]["role"] == "tenant":#اذا كان الايدي موجود بالحسابات وكان دوره مستأجر
                price = float(accounts[tenant_id]["property"].get("price", 0))#خذ سعر العقار من حسابه
                print(f"\nTenant: {accounts[tenant_id]['name']}")#اطبع اسمه 
                print(f"Property Price: {price}")#سعر العقار
                print(f"Monthly Rent: {price * 0.1}")  #الرسوم الشهريه
            else:#في حال عدم وجود ايدي المستأجر
                print("Tenant not found")  #المستأجر لا يوجد
        else:
            print("Invalid choice")

def tenant_menu(): # دالة قائمه المستأجر
    tenant_id = None
    for id, data in accounts.items():#يشوف اذا في حسابات مسـتاجرين
        if data["role"] == "tenant": #اذا كان دورة مستاجر
            tenant_id = id
            break
    
    if not tenant_id:
        print("No tenant account found")#لايوجد مستأجر
        return
        
    while True: 
        display_menu("tenant")# عرض خيارات المستأجر
        
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        
        if c == 0:
            break
            
        if c == 1: #عرض العقار الخاص بالمستأجر
            print("YOUR PROPERTY:")
            for k, v in accounts[tenant_id]["property"].items():
                print(f"{k}: {v}")     
        elif c == 2:#عرض تفاصيل الايجار
            price = float(accounts[tenant_id]["property"].get("price", 0))#خذ سعر عقار المستاجر
            print("RENT DETAILS:")
            print(f"Monthly Rent: {price * 0.1}")#الرسوم الشهريه
            print(f"Annual Rent: {price * 0.1 * 12}")#الرسوم السنويه
            print(f"Security Deposit: {price * 0.2}")     #التأمين
        elif c == 3: #حساب الرسوم
            price = float(accounts[tenant_id]["property"].get("price", 0))#خذ سعر عقار المستخدم
            months = int(input("Enter number of months: ")) #ادخل عدد الشهور 
            print(f"\nTotal rent for {months} months: {price * 0.1 * months}") #احسب رسوم     
        elif c == 4:#طلب تجديد عقد ايجار
            print("Contract renewal request has been sent to management.")   
        elif c == 5:#تعديل بيانات المستاجر الخاصه
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

def customer_menu(): #دالة قائمة الزبون
    while True: 
        display_menu("customer")
        
        try:
            c = int(input("Enter number of operation: "))
        except ValueError:
            print("Please enter a valid number")
            continue
        
        if c == 0:
            break
            
        if c == 1:#البحث عن عقار
            property_t = property_type()
            if property_t == 0:
                continue
            elif property_t == 1:
                search_property(lands, property_t)
            elif property_t == 2:
                search_property(houses, property_t)
            else:
                search_property(apartments, property_t)
                
        elif c == 2:#ارسال طلب اهتمام بشراء عقار
            customer_id = input("Enter your customer ID: ").strip() # ادخل الادي 
            if customer_id not in accounts or accounts[customer_id]["role"] != "customer":
                print("Customer not found")
                continue
                
            prop = property_type()
            if prop == 0:
                continue
                
            if prop == 1:#اذا كان نوع العقار اراضي
                print_property_data(lands) #اطبع كل العقارات المتاحه للبيع
                id = input("Enter ID of property you're interested in: ").strip() #اطلب من الزبون ادخال ايدي العقار الذي ريد شراءه
                if id in lands:
                    request_of_purchase[customer_id] = lands[id] #ارسل الطلب 
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
            
        elif c == 3: #طلب عرض عقار للبيع في البرنامج
            print("SELL PROPERTY REQUEST")
            pt = property_type()
            if pt == 0:
                continue
                
            id = input("Enter ID for the property: ").strip().lower() #ادخل ايدي لعقارك
            if (pt == 1 and id in lands) or (pt == 2 and id in houses) or (pt == 3 and id in apartments): #اذا يوجد ايدي مسجل مسبق بهذا الاسم 
                print("This property already exists in our system") #يوجد ايدي مسجل بهذا
                continue    
            data = input_property_data(pt) #ادخل معلومات عقارك الذي تريد بيعه
            request_of_sell[id] = data #اضف الطلب هذا
            print("Your request has been submitted. We will contact you soon.")   
        elif c == 4: #تسجيل زبون
            print("REGISTER NEW CUSTOMER:")
            id = input("Enter customer ID: ").strip() #ادخل الايدي
            if id in accounts:
                print("This ID already exists")
                continue
                
            name = input("Enter your name: ").strip() #ادخل الاسم
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

def main():#الداله الرئيسيه     
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
        print("PROPERTY MANAGEMENT SYSTEM") #نظام ادارة عقارات
        print("1- Login") #تسجيل الدخول
        print("0- Exit") #الخروخ
        print("="*50)
        
        try: #عشان م يوقف البرنامج عند ادخال المستخدم نص
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
            print("Thank you for using our system. Goodbye!")#شكرا لاستخدامك برنامجنا 
            break
            
        elif option == 1:
            role = login() #دالة تسجيل الدخول
            if role == "manager": #اذا كان المستخدم مدير
                manager_menu() #دالة قائمة المدير
            elif role == "employee":#اذا كان المستخدم موظف
                employee_menu() #دالة قائمه الموظف
            elif role == "tenant": #اذا كان المستخدم مستأجر
                tenant_menu() #دالة قائمة المستاجر
            elif role == "customer":
                customer_menu()
                
        else:
            print("Invalid option. Please try again.")



main()


