def _get_container_by_type(self, prop_or_type):
        # إذا تلقيت كائن أو نوع string
        if isinstance(prop_or_type, Property):
            if isinstance(prop_or_type, Land):
                return self.lands
            if isinstance(prop_or_type, House):
                return self.houses
            if isinstance(prop_or_type, Apartment):
                return self.apartments
        else:
            t = prop_or_type.lower()
            if t == "land" or t == "lands":
                return self.lands
            if t == "house" or t == "houses":
                return self.houses
            if t == "apartment" or t == "apartments":
                return self.apartments
        raise ValueError("Unknown type")

    # حذف/بيع
    def mark_as_sold(self, prop_type: str, prop_id: str) -> bool:
        cont = self._get_container_by_type(prop_type)
        if prop_id in cont:
            prop = cont[prop_id]
            if prop_type.lower() == "land":
                self.sold_lands[prop_id] = prop.to_dict()
            elif prop_type.lower() == "house":
                self.sold_houses[prop_id] = prop.to_dict()
            else:
                self.sold_apartments[prop_id] = prop.to_dict()
            del cont[prop_id]
            return True
        return False

    # تحرير بيانات عقار (بسيط عبر استبدال الحقول)
    def edit_property(self, prop_type: str, prop_id: str, updates: Dict[str, Any]) -> bool:
        cont = self._get_container_by_type(prop_type)
        if prop_id not in cont:
            return False
        prop = cont[prop_id]
        for k, v in updates.items():
            if hasattr(prop, k):
                try:
                    # استبدال النوع إن كان price
                    if k == "price":
                        setattr(prop, k, float(v))
                    else:
                        setattr(prop, k, v)
                except Exception:
                    setattr(prop, k, v)
        return True

    # طباعة/عرض
    def list_properties(self, prop_type: str) -> None:
        cont = self._get_container_by_type(prop_type)
        if not cont:
            print("No properties available.")
            return
        for pid, prop in cont.items():
            print("-" * 30)
            prop.display()

    # بحث متقدم (city/neighborhood/price_range/full match)
    def search_by_city(self, city: str) -> List[Property]:
        city = city.strip().lower()
        results = []
        for d in (self.lands, self.houses, self.apartments):
            for p in d.values():
                if p.city.strip().lower() == city:
                    results.append(p)
        return results

    def search_by_neighborhood(self, neighborhood: str) -> List[Property]:
        neighborhood = neighborhood.strip().lower()
        results = []
        for d in (self.lands, self.houses, self.apartments):
            for p in d.values():
                if p.neighborhood.strip().lower() == neighborhood:
                    results.append(p)
        return results

    def search_by_price_range(self, min_price: float, max_price: float) -> List[Property]:
        results = []
        for d in (self.lands, self.houses, self.apartments):
            for p in d.values():
                if min_price <= float(p.price) <= max_price:
                    results.append(p)
        return results

    def search_full(self, prop_type_num: int, criteria: Dict[str, Any]) -> List[Property]:
        # prop_type_num: 1 land, 2 house, 3 apartment
        container = {1: self.lands, 2: self.houses, 3: self.apartments}.get(prop_type_num, {})
        results = []
        for p in container.values():
            match = True
            for k, v in criteria.items():
                pv = str(getattr(p, k, "")).strip().lower()
                if pv != str(v).strip().lower():
                    match = False
                    break
            if match:
                results.append(p)
        return results


# -----------------------
# Accounts و Users
# -----------------------
class User:
    def __init__(self, user_id: str, name: str, password: str, role: str, email: Optional[str] = None,
                 phone: Optional[str] = None, secretword: Optional[str] = None, property_data: Optional[Dict] = None):
        self.id = user_id
        self.name = name
        self.password = password
        self.role = role
        self.email = email
        self.phone = phone
        self.secretword = secretword
        self.property = property_data  # للاحتفاظ بمعلومات العقار إذا كان مستأجرًا

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "role": self.role,
            "email": self.email,
            "phone": self.phone,
            "secretword": self.secretword,
            "property": self.property
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data["id"], data.get("name", ""), data.get("password", ""), data.get("role", ""),
                   data.get("email"), data.get("phone"), data.get("secretword"), data.get("property"))


class AccountManager:
    def __init__(self):
        self.accounts: Dict[str, User] = {}

    def load(self):
        raw = load_json(ACCOUNTS_FILE)
        if not raw:
            self.accounts = {}
            return
        self.accounts = {uid: User.from_dict(d) for uid, d in raw.items()}

    def save(self):
        save_json(ACCOUNTS_FILE, {uid: u.to_dict() for uid, u in self.accounts.items()})

    def add_user(self, user: User) -> bool:
        if user.id in self.accounts:
            return False
        self.accounts[user.id] = user
        return True

    def remove_user(self, user_id: str) -> bool:
        if user_id in self.accounts:
            del self.accounts[user_id]
            return True
        return False

    def edit_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        if user_id not in self.accounts:
            return False
        user = self.accounts[user_id]
        for k, v in updates.items():
            if hasattr(user, k):
                setattr(user, k, v)
        return True

    def login(self, user_id: str, password: str) -> Optional[User]:
        user = self.accounts.get(user_id)
        if not user:
            return None
        if user.password == password:
            return user
        return None


# -----------------------
# واجهة System (المنيو وربط كل شيء)
# -----------------------
class PropertySystem:
    def __init__(self):
        self.pm = PropertyManager()
        self.am = AccountManager()
        # حمل البيانات من الملفات
        self.pm.load_all()
        self.am.load()
        # إذا كانت البيانات فارغة، أنشئ بيانات تجريبية مشابهة للنسخة القديمة
        if not self.pm.lands and not self.pm.houses and not self.pm.apartments:
            self._load_sample_properties()
        if not self.am.accounts:
            self._load_sample_accounts()

    def _load_sample_properties(self):
        # بيانات أصلية بسيطة
        self.pm.lands = {
            "land1": Land("land1", "Taiz", "Almoshky", 10000, "1000 hector"),
            "land2": Land("land2", "Ibb", "Alrodah", 12000, "1200 hector"),
            "land3": Land("land3", "Taiz", "alqadi valley", 9000, "1500 hector"),
            "land4": Land("land4", "Ibb", "almasbah", 12500, "1400 hector"),
        }
        self.pm.houses = {
            "house1": House("house1", "taiz", "almasbah", 1000, "3", "6")
        }
        self.pm.apartments = {
            "apartment1": Apartment("apartment1", "taiz", "alrodah", 1000, "2", "6")
        }

    def _load_sample_accounts(self):
        # بعض الحسابات تجريبية
        samples = {
            "admin": User("admin", "Mohammed AL-SHAMERI", "moh4321", "manager", "dofla@gmail.com", "730395069", "CR7"),
            "emp1": User("emp1", "Mohammed Al-sharafi", "messi10", "employee", "alsharfi@gmail.com", "778076278", "M10"),
            "ten1": User("ten1", "Qusai", "11223344", "tenant", "qousai@gmail.com", "770022891", "M10",
                         property_data=self.pm.apartments.get("apartment1").to_dict() if "apartment1" in self.pm.apartments else None),
            "cus1": User("cus1", "Ahmed", "11223344", "customer", None, None, "M10")
        }
        for k, v in samples.items():
            self.am.add_user(v)

    def save_all(self):
        self.pm.save_all()
        self.am.save()

    # ----- منيو وواجهات نصية (مشابهة للنسخة القديمة) -----
    def run(self):
        while True:
            print("=" * 50)
            print("PROPERTY MANAGEMENT SYSTEM (OOP)")
            print("1- Login")
            print("0- Exit")
            print("=" * 50)
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a valid number")
                continue
            if choice == 0:
                self.save_all()
                print("Saved. Goodbye!")
                break
            elif choice == 1:
                user_id = input("Username: ").strip()
                password = input("Password: ").strip()
                user = self.am.login(user_id, password)
                if user:
                    print(f"Welcome {user.name} ({user.role})")
                    self._dispatch_user_menu(user)
                else:
                    print("Invalid credentials.")
            else:
                print("Invalid option.")

    def _dispatch_user_menu(self, user: User):
        if user.role == "manager":
            self._manager_menu(user)
        elif user.role == "employee":
            self._employee_menu(user)
        elif user.role == "tenant":
            self._tenant_menu(user)
        elif user.role == "customer":
            self._customer_menu(user)
        else:
            print("Unknown role.")

    # ---------- شيفرات منيو المدير ----------
    def _manager_menu(self, user: User):
        while True:
            print("=" * 50)
            print("MANAGER DASHBOARD")
            print("1- Search for property")
            print("2- View all properties available")
            print("3- List a property for sale (add)")
            print("4- Edit a property information")
            print("5- Confirm a property sale (mark sold)")
            print("6- Manage employee accounts")
            print("7- Manage customers accounts")
            print("0- Logout")
            print("=" * 50)
            try:
                c = int(input("Enter number of operation: "))
            except ValueError:
                print("Please enter a valid number")
                continue
            if c == 0:
                break
            if c == 1:
                self._menu_search()
            elif c == 2:
                self._menu_list_properties()
            elif c == 3:
                self._menu_add_property()
            elif c == 4:
                self._menu_edit_property()
            elif c == 5:
                self._menu_mark_sold()
            elif c == 6:
                self._menu_manage_employees()
            elif c == 7:
                self._menu_manage_customers()
            else:
                print("Invalid choice.")

    # ---------- شيفرات منيو الموظف ----------
    def _employee_menu(self, user: User):
        while True:
            print("=" * 50)
            print("EMPLOYEE DASHBOARD")
            print("1- Search for properties")
            print("2- View properties (with filters)")
            print("3- List a property for sale (add)")
            print("4- Edit a property information")
            print("5- Add a new tenant")
            print("6- Calculate a tenant payment")
            print("0- Logout")
            print("=" * 50)
            try:
                c = int(input("Enter number of operation: "))
            except ValueError:
                print("Please enter a valid number")
                continue
            if c == 0:
                break
            if c == 1:
                self._menu_search()
            elif c == 2:
                self._menu_list_properties()
            elif c == 3:
                self._menu_add_property()
            elif c == 4:
                self._menu_edit_property()
            elif c == 5:
                self._menu_add_tenant()
            elif c == 6:
                self._menu_calculate_tenant_payment()
            else:
                print("Invalid choice.")

    # ---------- شيفرات منيو المستأجر ----------
    def _tenant_menu(self, user: User):
        while True:
            print("=" * 50)
            print("TENANT DASHBOARD")
            print("1- View your property")
            print("2- View rent details")
            print("3- Auto calculate rent fees")
            print("4- Request contract renewal")
            print("5- Edit personal info")
            print("6- View payment history")
            print("0- Logout")
            print("=" * 50)
            try:
                c = int(input("Enter number of operation: "))
            except ValueError:
                print("Please enter a valid number")
                continue
            if c == 0:
                break
            if c == 1:
                if user.property:
                    for k, v in user.property.items():
                        print(f"{k}: {v}")
                else:
                    print("No property attached.")
            elif c == 2:
                try:
                    price = float(user.property.get("price", 0))
                except Exception:
                    price = 0
                print("RENT DETAILS:")
                print(f"Monthly Rent: {price * 0.1}")
                print(f"Annual Rent: {price * 0.1 * 12}")
                print(f"Security Deposit: {price * 0.2}")
            elif c == 3:
                try:
                    months = int(input("Enter number of months: "))
                except ValueError:
                    print("Please enter a number")
                    continue
                price = float(user.property.get("price", 0)) if user.property else 0
                print(f"Total rent for {months} months: {price * 0.1 * months}")
            elif c == 4:
                print("Contract renewal request has been sent to management.")
            elif c == 5:
                print("Edit personal information (leave blank to keep current):")
                new_name = input("Enter new name: ").strip()
                new_email = input("Enter new email: ").strip()
                new_phone = input("Enter new phone: ").strip()
                new_password = input("Enter new password: ").strip()
                if new_name:
                    user.name = new_name
                if new_email:
                    user.email = new_email
                if new_phone:
                    user.phone = new_phone
                if new_password:
                    user.password = new_password
                print("Information updated.")
            elif c == 6:
                print("PAYMENT HISTORY: (not implemented) No history available.")
            else:
                print("Invalid choice.")

    # ---------- شيفرات منيو الزبون ----------
    def _customer_menu(self, user: User):
        while True:
            print("=" * 50)
            print("CUSTOMER DASHBOARD")
            print("1- Search for available properties")
            print("2- Send purchase interest request")
            print("3- Request to show property for sale")
            print("4- Register or make inquiry (update account info)")
            print("0- Logout")
            print("=" * 50)
            try:
                c = int(input("Enter number of operation: "))
            except ValueError:
                print("Please enter a valid number")
                continue
            if c == 0:
                break
            if c == 1:
                self._menu_search()
            elif c == 2:
                cid = user.id
                print("Choose property type to view:")
                t = self._input_property_type()
                if t == 0:
                    continue
                container = {1: self.pm.lands, 2: self.pm.houses, 3: self.pm.apartments}[t]
                if not container:
                    print("No properties available in this type.")
                    continue
                for pid, p in container.items():
                    print("-" * 20)
                    p.display()
                pid = input("Enter ID of property you're interested in: ").strip()
                if pid in container:
                    self.pm.request_of_purchase[cid] = container[pid].to_dict()
                    print("Your request has been sent successfully")
                else:
                    print("Property not found")
            elif c == 3:
                print("Sell Property Request")
                t = self._input_property_type()
                if t == 0:
                    continue
                pid = input("Enter ID for the property: ").strip()
                container = {1: self.pm.lands, 2: self.pm.houses, 3: self.pm.apartments}[t]
                if pid in container:
                    print("This property already exists in our system")
                    continue
                # collect details
                data = self._collect_property_data_for_type(t, pid)
                self.pm.request_of_sell[pid] = data
                print("Your request has been submitted. We will contact you soon.")
            elif c == 4:
                print("Update your account info (leave blank to keep current):")
                new_name = input("Enter new name: ").strip()
                new_password = input("Enter new password: ").strip()
                new_secret = input("Enter new secretword: ").strip()
                if new_name:
                    user.name = new_name
                if new_password:
                    user.password = new_password
                if new_secret:
                    user.secretword = new_secret
                print("Account updated.")
            else:
                print("Invalid choice.")

    # ---------- وظائف مساعدة للقوائم ----------
    def _menu_search(self):
        while True:
            print("\nSEARCH PROPERTIES:")
            print("1- By city name")
            print("2- By neighborhood name")
            print("3- By price range")
            print("4- Full search (type-specific)")
            print("0- Back")
            try:
                ch = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a number")
                continue
            if ch == 0:
                break
            if ch == 1:
                city = input("Enter city name: ").strip()
                results = self.pm.search_by_city(city)
                if results:
                    for r in results:
                        print("-" * 20)
                        r.display()
                else:
                    print("No properties found.")
            elif ch == 2:
                nb = input("Enter neighborhood name: ").strip()
                results = self.pm.search_by_neighborhood(nb)
                if results:
                    for r in results:
                        print("-" * 20)
                        r.display()
                else:
                    print("No properties found.")
            elif ch == 3:
                try:
                    mn = float(input("Enter minimum price: "))
                    mx = float(input("Enter maximum price: "))
                except ValueError:
                    print("Please enter valid numbers")
                    continue
                results = self.pm.search_by_price_range(mn, mx)
                if results:
                    for r in results:
                        print("-" * 20)
                        r.display()
                else:
                    print("No properties found.")
            elif ch == 4:
                t = self._input_property_type()
                if t == 0:
                    continue
                criteria = {}
                if t == 1:
                    criteria["city"] = input("City: ").strip()
                    criteria["neighborhood"] = input("Neighborhood: ").strip()
                    criteria["size"] = input("Size: ").strip()
                elif t == 2:
                    criteria["city"] = input("City: ").strip()
                    criteria["neighborhood"] = input("Neighborhood: ").strip()
                    criteria["floors"] = input("Floors: ").strip()
                    criteria["number_of_apartments"] = input("Number of apartments: ").strip()
                elif t == 3:
                    criteria["city"] = input("City: ").strip()
                    criteria["neighborhood"] = input("Neighborhood: ").strip()
                    criteria["floor"] = input("Floor: ").strip()
                    criteria["rooms"] = input("Number of rooms: ").strip()
                results = self.pm.search_full(t, criteria)
                if results:
                    for r in results:
                        print("-" * 20)
                        r.display()
                else:
                    print("No properties found.")
            else:
                print("Invalid choice.")

    def _menu_list_properties(self):
        while True:
            print("\nVIEW PROPERTIES BY TYPE:")
            print("1- Lands")
            print("2- Houses")
            print("3- Apartments")
            print("0- Back")
            try:
                t = int(input("Enter choice: "))
            except ValueError:
                print("Enter a number")
                continue
            if t == 0:
                break
            if t == 1:
                self.pm.list_properties("lands")
            elif t == 2:
                self.pm.list_properties("houses")
            elif t == 3:
                self.pm.list_properties("apartments")
            else:
                print("Invalid choice.")

    def _menu_add_property(self):
        t = self._input_property_type()
        if t == 0:
            return
        pid = input("Enter property ID: ").strip()
        container = {1: self.pm.lands, 2: self.pm.houses, 3: self.pm.apartments}[t]
        if pid in container:
            print("This ID already exists.")
            return
        prop = self._collect_property_data_for_type(t, pid)
        # بناء الكائن
        if t == 1:
            obj = Land(pid, prop["city"], prop["neighborhood"], prop["price"], prop["size"])
        elif t == 2:
            obj = House(pid, prop["city"], prop["neighborhood"], prop["price"], prop["floors"], prop["number_of_apartments"])
        else:
            obj = Apartment(pid, prop["city"], prop["neighborhood"], prop["price"], prop["floor"], prop["rooms"])
        if self.pm.add_property(obj):
            print("Property added successfully.")
        else:
            print("Failed to add property (maybe duplicate).")

    def _menu_edit_property(self):
        t = self._input_property_type()
        if t == 0:
            return
        pid = input("Enter property ID to edit: ").strip()
        container = {1: self.pm.lands, 2: self.pm.houses, 3: self.pm.apartments}[t]
        if pid not in container:
            print("Property not found.")
            return
        prop = container[pid]
        print("Current data:")
        prop.display()
        print("\nEnter new values (leave blank to keep current):")
        updates = {}
        new_city = input("City: ").strip()
        new_neighborhood = input("Neighborhood: ").strip()
        new_price = input("Price: ").strip()
        if new_city:
            updates["city"] = new_city
        if new_neighborhood:
            updates["neighborhood"] = new_neighborhood
        if new_price:
            try:
                updates["price"] = float(new_price)
            except ValueError:
                print("Invalid price. Skipping price update.")
        if t == 1:
            new_size = input("Size: ").strip()
            if new_size:
                updates["size"] = new_size
        elif t == 2:
            new_floors = input("Floors: ").strip()
            new_num_ap = input("Number of apartments: ").strip()
            if new_floors:
                updates["floors"] = new_floors
            if new_num_ap:
                updates["number_of_apartments"] = new_num_ap
        else:
            new_floor = input("Floor: ").strip()
            new_rooms = input("Number of rooms: ").strip()
            if new_floor:
                updates["floor"] = new_floor
            if new_rooms:
                updates["rooms"] = new_rooms
        success = self.pm.edit_property({1: "land", 2: "house", 3: "apartment"}[t], pid, updates)
        print("Changes saved." if success else "Failed to save changes.")

    def _menu_mark_sold(self):
        t = self._input_property_type()
        if t == 0:
            return
        pid = input("Enter property ID to mark as sold: ").strip()
        typname = {1: "land", 2: "house", 3: "apartment"}[t]
        if self.pm.mark_as_sold(typname, pid):
            print("Property marked as sold.")
        else:
            print("Property not found.")

    def _menu_manage_employees(self):
        while True:
            print("\nEMPLOYEE MANAGEMENT")
            print("1- View all employees")
            print("2- Add employee")
            print("3- Edit employee")
            print("4- Delete employee")
            print("0- Back")
            try:
                ch = int(input("Enter choice: "))
            except ValueError:
                print("Enter a number")
                continue
            if ch == 0:
                break
            if ch == 1:
                for uid, u in self.am.accounts.items():
                    if u.role == "employee":
                        print("-" * 20)
                        print(f"ID: {u.id}, Name: {u.name}, Email: {u.email}, Phone: {u.phone}")
            elif ch == 2:
                uid = input("Enter employee ID: ").strip()
                if uid in self.am.accounts:
                    print("ID exists.")
                    continue
                name = input("Enter name: ").strip()
                email = input("Enter email: ").strip()
                phone = input("Enter phone: ").strip()
                password = input("Enter password: ").strip()
                secret = input("Enter secret word: ").strip()
                u = User(uid, name, password, "employee", email, phone, secret)
                self.am.add_user(u)
                print("Employee added.")
            elif ch == 3:
                uid = input("Enter employee ID to edit: ").strip()
                if uid not in self.am.accounts or self.am.accounts[uid].role != "employee":
                    print("Employee not found.")
                    continue
                name = input("Enter new name (leave blank to keep): ").strip()
                email = input("Enter new email (leave blank): ").strip()
                phone = input("Enter new phone (leave blank): ").strip()
                password = input("Enter new password (leave blank): ").strip()
                if name:
                    self.am.accounts[uid].name = name
                if email:
                    self.am.accounts[uid].email = email
                if phone:
                    self.am.accounts[uid].phone = phone
                if password:
                    self.am.accounts[uid].password = password
                print("Updated.")
            elif ch == 4:
                uid = input("Enter employee ID to delete: ").strip()
                if self.am.remove_user(uid):
                    print("Deleted.")
                else:
                    print("Not found.")
            else:
                print("Invalid choice.")

    def _menu_manage_customers(self):
        while True:
            print("\nCUSTOMER MANAGEMENT")
            print("1- View all purchase requests")
            print("2- View property offers")
            print("3- Confirm property offer (add offer to system)")
            print("0- Back")
            try:
                ch = int(input("Enter choice: "))
            except ValueError:
                print("Enter a number")
                continue
            if ch == 0:
                break
            if ch == 1:
                if not self.pm.request_of_purchase:
                    print("No purchase requests.")
                else:
                    for cid, data in self.pm.request_of_purchase.items():
                        user = self.am.accounts.get(cid)
                        print("-" * 20)
                        print(f"Customer: {user.name if user else cid}")
                        print("Requested property:")
                        for k, v in data.items():
                            print(f"{k}: {v}")
            elif ch == 2:
                if not self.pm.request_of_sell:
                    print("No property offers.")
                else:
                    for pid, data in self.pm.request_of_sell.items():
                        print("-" * 20)
                        print(f"Offer ID: {pid}")
                        for k, v in data.items():
                            print(f"{k}: {v}")
            elif ch == 3:
                if not self.pm.request_of_sell:
                    print("No offers available.")
                    continue
                print("Available offers IDs:")
                for pid in self.pm.request_of_sell.keys():
                    print(f"- {pid}")
                pid = input("Enter ID of property to confirm: ").strip()
                if pid not in self.pm.request_of_sell:
                    print("Not found.")
                    continue
                t = self._input_property_type()
                if t == 0:
                    continue
                data = self.pm.request_of_sell[pid]
                try:
                    if t == 1:
                        obj = Land(pid, data["city"], data["neighborhood"], float(data["price"]), data.get("size", ""))
                        self.pm.lands[pid] = obj
                    elif t == 2:
                        obj = House(pid, data["city"], data["neighborhood"], float(data["price"]), data.get("floors", ""), data.get("number_of_apartments", ""))
                        self.pm.houses[pid] = obj
                    else:
                        obj = Apartment(pid, data["city"], data["neighborhood"], float(data["price"]), data.get("floor", ""), data.get("rooms", ""))
                        self.pm.apartments[pid] = obj
                    del self.pm.request_of_sell[pid]
                    print("Property added to system.")
                except Exception as e:
                    print("Failed to add property:", e)
            else:
                print("Invalid choice.")

    def _menu_add_tenant(self):
        uid = input("Enter ID for new tenant: ").strip()
        if uid in self.am.accounts:
            print("This ID already exists")
            return
        name = input("Enter name of tenant: ").strip()
        email = input("Enter email: ").strip()
        phone = input("Enter phone: ").strip()
        password = input("Enter password: ").strip()
        secretword = input("Enter secret word: ").strip()
        t = self._input_property_type()
        if t == 0:
            return
        pid = input("Enter property ID to assign to tenant: ").strip()
        container = {1: self.pm.lands, 2: self.pm.houses, 3: self.pm.apartments}[t]
        if pid not in container:
            print("Property not found")
            return
        prop_data = container[pid].to_dict()
        user = User(uid, name, password, "tenant", email, phone, secretword, property_data=prop_data)
        self.am.add_user(user)
        print("Tenant added successfully")

    def _menu_calculate_tenant_payment(self):
        uid = input("Enter tenant ID: ").strip()
        user = self.am.accounts.get(uid)
        if not user or user.role != "tenant":
            print("Tenant not found")
            return
        try:
            price = float(user.property.get("price", 0))
        except Exception:
            price = 0
        print(f"Tenant: {user.name}")
        print(f"Property Price: {price}")
        print(f"Monthly Rent: {price * 0.1}")

    # ---------- أدوات بسيطة ----------
    @staticmethod
    def _input_property_type() -> int:
        print("\nCHOOSE PROPERTY TYPE:")
        print("1- Land")
        print("2- House")
        print("3- Apartment")
        print("0- Back")
        try:
            t = int(input("Enter your choice: "))
            if 0 <= t <= 3:
                return t
        except ValueError:
            pass
        print("Invalid input. Returning to menu.")
        return 0

    @staticmethod
    def _collect_property_data_for_type(t: int, pid: str) -> Dict[str, Any]:
        data = {"id": pid}
        city = input("Enter city: ").strip()
        neighborhood = input("Enter neighborhood: ").strip()
        while True:
            price_raw = input("Enter price: ").strip()
            try:
                price = float(price_raw)
                break
            except ValueError:
                print("Please enter a valid number for price")
        data["city"] = city
        data["neighborhood"] = neighborhood
        data["price"] = price
        if t == 1:
            size = input("Enter size of land: ").strip()
            data["size"] = size
        elif t == 2:
            floors = input("Enter number of floors: ").strip()
            num_ap = input("Enter number of apartments: ").strip()
            data["floors"] = floors
            data["number_of_apartments"] = num_ap
        else:
            floor = input("Enter floor number: ").strip()
            rooms = input("Enter number of rooms: ").strip()
            data["floor"] = floor
            data["rooms"] = rooms
        return data


# -----------------------
# تشغيل النظام
# -----------------------
if __name__ == "__main__":
    system = PropertySystem()
    try:
        system.run()
    except KeyboardInterrupt:
        print("\nInterrupted. Saving data...")
        system.save_all()
        print("Saved. Bye.")