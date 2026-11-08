import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# ==========================================
# البيانات الافتراضية (مطابقة لملف المشروع الأصلي)
# ==========================================
lands = {
    "land1": {"city": "Taiz", "neighborhood": "Almoshky", "size": "1000 hector", "price": "10000"},
    "land2": {"city": "Ibb", "neighborhood": "Alrodah", "size": "1200 hector", "price": "12000"},
    "land3": {"city": "Taiz", "neighborhood": "alqadi valley", "size": "1500 hector", "price": "9000"},
    "land4": {"city": "Ibb", "neighborhood": "almasbah", "size": "1400 hector", "price": "12500"}
}

houses = {
    "house1": {"city": "taiz", "neighborhood": "almasbah", "floors": "3", "price": "1000", "number of apartments": "6"}
}

apartments = {
    "apartment1": {"city": "taiz", "neighborhood": "alrodah", "floor": "2", "price": "1000", "number of rooms": "6"}
}

sold_lands = {}
sold_houses = {}
sold_apartments = {}
request_of_purchase = {}
request_of_sell = {}

accounts = {
    "admin": {
        "name": "Mohammed AL-SHAMERI", "password": "moh4321", "email": "dofla@gmail.com",
        "phone": "730395069", "secretword": "CR7", "role": "manager"
    },
    "emp1": {
        "name": "Mohammed Al-sharafi", "email": "alsharfi@gmail.com", "phone": "778076278",
        "password": "messi10", "secretword": "M10", "role": "employee"
    },
    "emp2": {
        "name": "Mohammed Isameil", "email": "isameil@gmail.com", "phone": "734932753",
        "password": "5432167890", "secretword": "CR7", "role": "employee"
    },
    "emp3": {
        "name": "Mohaned Al-wajeh", "email": "mohaned@gmail.com", "phone": "735478626",
        "password": "ronaldo4321", "secretword": "CR7", "role": "employee"
    },
    "ten1": {
        "name": "Qusai", "email": "qousai@gmail.com", "phone": "770022891",
        "password": "11223344", "secretword": "M10", "role": "tenant",
        "property_id": "apartment1", "city": "taiz", "neighborhood": "alrodah", "price": "1000"
    },
    "cus1": {
        "name": "Ahmed", "password": "11223344", "secretword": "M10", "role": "customer"
    }
}

# ==========================================
# دوال حفظ وتحميل الملفات النصية (.txt)
# ==========================================
def save_to_file(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        for key, value in data.items():
            f.write(f"{key}:\n")
            if isinstance(value, dict):
                for k, v in value.items():
                    if not isinstance(v, dict):
                        f.write(f"{k}:{v}\n")
            f.write("\n")

def load_from_file(file, default_data):
    if not os.path.exists(file):
        return default_data
    data = {}
    try:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        current_key = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.endswith(":") and ":" not in line[:-1]:
                current_key = line[:-1].strip()
                data[current_key] = {}
            elif ":" in line and current_key:
                inner_key, value = line.split(":", 1)
                data[current_key][inner_key.strip()] = value.strip()
        return data if data else default_data
    except Exception:
        return default_data

def load_all_data():
    global lands, houses, apartments, sold_lands, sold_houses, sold_apartments, request_of_purchase, request_of_sell, accounts
    lands = load_from_file("property_l.txt", lands)
    houses = load_from_file("property_houses.txt", houses)
    apartments = load_from_file("property_apartment.txt", apartments)
    sold_lands = load_from_file("sold.property.lands.txt", sold_lands)
    sold_houses = load_from_file("sold.property.houses.txt", sold_houses)
    sold_apartments = load_from_file("sold.property.apartments.txt", sold_apartments)
    request_of_purchase = load_from_file("purchase_requsets.txt", request_of_purchase)
    request_of_sell = load_from_file("offers_requset.txt", request_of_sell)
    accounts = load_from_file("users.account.txt", accounts)

def save_all_data():
    save_to_file("property_l.txt", lands)
    save_to_file("property_houses.txt", houses)
    save_to_file("property_apartment.txt", apartments)
    save_to_file("users.account.txt", accounts)
    save_to_file("sold.property.lands.txt", sold_lands)
    save_to_file("sold.property.houses.txt", sold_houses)
    save_to_file("sold.property.apartments.txt", sold_apartments)
    save_to_file("purchase_requsets.txt", request_of_purchase)
    save_to_file("offers_requset.txt", request_of_sell)


# ==========================================
# تطبيق الواجهة الرسومية (Tkinter GUI)
# ==========================================
class PropertyManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Property Management System - نظام إدارة العقارات")
        self.geometry("1050x680")
        self.configure(bg="#0f172a")

        load_all_data()
        self.current_user_id = None
        self.login_attempts = 3

        # تنسيق الجداول والأزرار
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#1e293b", foreground="white", fieldbackground="#1e293b", rowheight=30, font=("Arial", 10))
        self.style.configure("Treeview.Heading", background="#0284c7", foreground="white", font=("Arial", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#0ea5e9")])

        self.main_container = tk.Frame(self, bg="#0f172a")
        self.main_container.pack(fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.show_login_screen()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def on_exit(self):
        save_all_data()
        self.destroy()

    # ==========================================
    # شاشة تسجيل الدخول
    # ==========================================
    def show_login_screen(self):
        self.clear_container()
        self.current_user_id = None

        card = tk.Frame(self.main_container, bg="#1e293b", padx=35, pady=35, highlightbackground="#334155", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=460)

        tk.Label(card, text="PROPERTY MANAGEMENT SYSTEM", font=("Arial", 15, "bold"), bg="#1e293b", fg="#38bdf8").pack(pady=(0, 5))
        tk.Label(card, text="نظام إدارة العقارات - تسجيل الدخول", font=("Arial", 11), bg="#1e293b", fg="#94a3b8").pack(pady=(0, 20))

        tk.Label(card, text="Username (ID):", font=("Arial", 10, "bold"), bg="#1e293b", fg="white", anchor="w").pack(fill="x")
        self.username_entry = tk.Entry(card, font=("Arial", 12), bg="#0f172a", fg="white", insertbackground="white")
        self.username_entry.pack(fill="x", pady=(5, 15), ipady=5)

        tk.Label(card, text="Password:", font=("Arial", 10, "bold"), bg="#1e293b", fg="white", anchor="w").pack(fill="x")
        self.password_entry = tk.Entry(card, font=("Arial", 12), show="*", bg="#0f172a", fg="white", insertbackground="white")
        self.password_entry.pack(fill="x", pady=(5, 15), ipady=5)

        tk.Button(card, text="Login / تسجيل الدخول", font=("Arial", 11, "bold"), bg="#0284c7", fg="white", relief="flat", pady=8, command=self.handle_login).pack(fill="x", pady=5)

        btn_row = tk.Frame(card, bg="#1e293b")
        btn_row.pack(fill="x", pady=5)
        tk.Button(btn_row, text="Forgot Password?", font=("Arial", 9), bg="#334155", fg="#38bdf8", relief="flat", command=self.forgot_password_dialog).pack(side="left", expand=True, fill="x", padx=(0, 3))
        tk.Button(btn_row, text="Register Customer", font=("Arial", 9), bg="#334155", fg="#a855f7", relief="flat", command=self.register_customer_dialog).pack(side="right", expand=True, fill="x", padx=(3, 0))

        # أزرار دخول سريع للتجربة
        tk.Label(card, text="--- دخول سريع للتجربة (Demo) ---", font=("Arial", 9), bg="#1e293b", fg="#64748b").pack(pady=(15, 5))
        demo_frame = tk.Frame(card, bg="#1e293b")
        demo_frame.pack(fill="x")
        for uid, label, col in [("admin", "Manager", "#4f46e5"), ("emp1", "Employee", "#059669"), ("ten1", "Tenant", "#d97706"), ("cus1", "Customer", "#9333ea")]:
            tk.Button(demo_frame, text=label, bg=col, fg="white", font=("Arial", 8, "bold"), relief="flat", command=lambda u=uid: self.quick_login(u)).pack(side="left", expand=True, fill="x", padx=2)

    def quick_login(self, uid):
        if uid in accounts:
            self.current_user_id = uid
            self.login_attempts = 3
            self.show_dashboard()

    def handle_login(self):
        if self.login_attempts <= 0:
            messagebox.showerror("Locked", "Too many failed attempts! Restart app.")
            return
        u = self.username_entry.get().strip()
        p = self.password_entry.get().strip()
        if u in accounts:
            if accounts[u].get("password") == p:
                self.current_user_id = u
                self.login_attempts = 3
                messagebox.showinfo("Welcome", f"Welcome {accounts[u].get('name', u)}!")
                self.show_dashboard()
            else:
                self.login_attempts -= 1
                messagebox.showwarning("Error", f"Incorrect password! {self.login_attempts} attempts remaining.")
        else:
            self.login_attempts -= 1
            messagebox.showwarning("Error", f"Username not found! {self.login_attempts} attempts remaining.")

    def forgot_password_dialog(self):
        u = simpledialog.askstring("Password Recovery", "Enter your username:")
        if not u or u.strip() not in accounts:
            messagebox.showerror("Error", "Username not found!")
            return
        secret = simpledialog.askstring("Secret Word", "Enter your secret word (e.g. CR7 / M10):")
        if secret and secret.strip() == accounts[u.strip()].get("secretword"):
            messagebox.showinfo("Password Recovered", f"Your password is: {accounts[u.strip()]['password']}")
        else:
            messagebox.showerror("Error", "Incorrect secret word!")

    def register_customer_dialog(self):
        win = tk.Toplevel(self)
        win.title("Register New Customer")
        win.geometry("350x340")
        win.configure(bg="#1e293b")

        fields = {}
        for label in ["Customer ID", "Name", "Password", "Secret Word"]:
            tk.Label(win, text=label, bg="#1e293b", fg="white").pack(anchor="w", padx=20, pady=(10, 2))
            ent = tk.Entry(win, bg="#0f172a", fg="white", insertbackground="white")
            ent.pack(fill="x", padx=20, ipady=4)
            fields[label] = ent

        def save_cus():
            cid = fields["Customer ID"].get().strip()
            name = fields["Name"].get().strip()
            pwd = fields["Password"].get().strip()
            sec = fields["Secret Word"].get().strip()
            if not cid or not name or not pwd:
                messagebox.showerror("Error", "Fill all fields!")
                return
            if cid in accounts:
                messagebox.showerror("Error", "This ID already exists!")
                return
            accounts[cid] = {"name": name, "password": pwd, "secretword": sec, "role": "customer"}
            save_all_data()
            messagebox.showinfo("Success", "Registration successful! You can login now.")
            win.destroy()

        tk.Button(win, text="Register", bg="#9333ea", fg="white", font=("Arial", 10, "bold"), command=save_cus).pack(fill="x", padx=20, pady=20, ipady=5)

    # ==========================================
    # لوحة التحكم الرئيسية حسب صلاحية المستخدم
    # ==========================================
    def show_dashboard(self):
        self.clear_container()
        user = accounts[self.current_user_id]
        role = user.get("role", "customer")

        # الشريط العلوي
        header = tk.Frame(self.main_container, bg="#1e293b", pady=12, padx=20)
        header.pack(fill="x")

        tk.Label(header, text=f"{role.upper()} DASHBOARD | Welcome: {user.get('name')} ({self.current_user_id})", font=("Arial", 13, "bold"), bg="#1e293b", fg="#38bdf8").pack(side="left")
        tk.Button(header, text="Save & Logout / خروج", bg="#e11d48", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=12, command=self.logout).pack(side="right")

        # التبويبات (Notebook)
        notebook = ttk.Notebook(self.main_container)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        if role in ["manager", "employee", "customer"]:
            prop_tab = tk.Frame(notebook, bg="#0f172a")
            notebook.add(prop_tab, text="  Available Properties (العقارات)  ")
            self.build_properties_tab(prop_tab, role)

        if role == "manager":
            emp_tab = tk.Frame(notebook, bg="#0f172a")
            notebook.add(emp_tab, text="  Manage Employees (الموظفين)  ")
            self.build_employees_tab(emp_tab)

            req_tab = tk.Frame(notebook, bg="#0f172a")
            notebook.add(req_tab, text="  Customer Requests (طلبات الزبائن)  ")
            self.build_requests_tab(req_tab)

        if role == "employee":
            ten_tab = tk.Frame(notebook, bg="#0f172a")
            notebook.add(ten_tab, text="  Tenants & Rent Calculator (المستأجرين)  ")
            self.build_employee_tenant_tab(ten_tab)

        if role == "tenant":
            my_tab = tk.Frame(notebook, bg="#0f172a")
            notebook.add(my_tab, text="  My Property & Rent Calculator (عقاري والإيجار)  ")
            self.build_tenant_dashboard(my_tab)

    def logout(self):
        save_all_data()
        self.show_login_screen()

    # ==========================================
    # تبويب العقارات (بحث، ترتيب، إضافة، تعديل، بيع، طلب شراء)
    # ==========================================
    def build_properties_tab(self, parent, role):
        top_bar = tk.Frame(parent, bg="#0f172a", pady=10)
        top_bar.pack(fill="x")

        tk.Label(top_bar, text="Type:", bg="#0f172a", fg="white").pack(side="left", padx=(5, 2))
        self.prop_type_var = tk.StringVar(value="All")
        type_cb = ttk.Combobox(top_bar, textvariable=self.prop_type_var, values=["All", "Land", "House", "Apartment"], width=12, state="readonly")
        type_cb.pack(side="left", padx=5)
        type_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_properties_table())

        tk.Label(top_bar, text="Search (City/Neighborhood):", bg="#0f172a", fg="white").pack(side="left", padx=(10, 2))
        self.search_var = tk.StringVar()
        tk.Entry(top_bar, textvariable=self.search_var, width=20).pack(side="left", padx=5)
        tk.Button(top_bar, text="Search", bg="#0284c7", fg="white", command=self.refresh_properties_table).pack(side="left", padx=3)
        tk.Button(top_bar, text="Sort by Price", bg="#334155", fg="white", command=lambda: self.refresh_properties_table(sort_by="price")).pack(side="left", padx=3)
        tk.Button(top_bar, text="Sort by City", bg="#334155", fg="white", command=lambda: self.refresh_properties_table(sort_by="city")).pack(side="left", padx=3)

        # جدول عرض العقارات
        cols = ("ID", "Type", "City", "Neighborhood", "Price", "Details")
        self.prop_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols:
            self.prop_tree.heading(c, text=c)
            self.prop_tree.column(c, width=140 if c != "Details" else 240, anchor="center")
        self.prop_tree.pack(fill="both", expand=True, pady=5)

        # أزرار العمليات أسفل الجدول
        action_bar = tk.Frame(parent, bg="#0f172a", pady=10)
        action_bar.pack(fill="x")

        if role in ["manager", "employee"]:
            tk.Button(action_bar, text="+ Add Property (إضافة عقار)", bg="#10b981", fg="white", font=("Arial", 10, "bold"), padx=12, pady=5, command=self.add_property_dialog).pack(side="left", padx=5)
            tk.Button(action_bar, text="Edit Selected (تعديل)", bg="#0284c7", fg="white", font=("Arial", 10, "bold"), padx=12, pady=5, command=self.edit_selected_property).pack(side="left", padx=5)

        if role == "manager":
            tk.Button(action_bar, text="Confirm Sale (تأكيد بيع العقار)", bg="#f59e0b", fg="black", font=("Arial", 10, "bold"), padx=12, pady=5, command=self.mark_selected_sold).pack(side="left", padx=5)

        if role == "customer":
            tk.Button(action_bar, text="Send Purchase Request (طلب شراء العقار المحدد)", bg="#9333ea", fg="white", font=("Arial", 10, "bold"), padx=12, pady=5, command=self.customer_purchase_request).pack(side="left", padx=5)
            tk.Button(action_bar, text="Offer My Property for Sale (طلب عرض عقار للبيع)", bg="#0284c7", fg="white", font=("Arial", 10, "bold"), padx=12, pady=5, command=lambda: self.add_property_dialog(is_customer_offer=True)).pack(side="left", padx=5)

        self.refresh_properties_table()

    def refresh_properties_table(self, sort_by=None):
        for row in self.prop_tree.get_children():
            self.prop_tree.delete(row)

        selected_t = self.prop_type_var.get()
        q = self.search_var.get().lower().strip()
        rows = []

        if selected_t in ["All", "Land"]:
            for pid, d in lands.items():
                rows.append((pid, "Land", d.get("city", ""), d.get("neighborhood", ""), float(d.get("price", 0)), f"Size: {d.get('size', '')}"))
        if selected_t in ["All", "House"]:
            for pid, d in houses.items():
                rows.append((pid, "House", d.get("city", ""), d.get("neighborhood", ""), float(d.get("price", 0)), f"Floors: {d.get('floors', '')} | Apts: {d.get('number of apartments', '')}"))
        if selected_t in ["All", "Apartment"]:
            for pid, d in apartments.items():
                rows.append((pid, "Apartment", d.get("city", ""), d.get("neighborhood", ""), float(d.get("price", 0)), f"Floor: {d.get('floor', '')} | Rooms: {d.get('number of rooms', '')}"))

        if q:
            rows = [r for r in rows if q in r[0].lower() or q in r[2].lower() or q in r[3].lower()]

        if sort_by == "price":
            rows.sort(key=lambda x: x[4])
        elif sort_by == "city":
            rows.sort(key=lambda x: x[2].lower())

        for r in rows:
            self.prop_tree.insert("", "end", values=r)

    def add_property_dialog(self, is_customer_offer=False):
        win = tk.Toplevel(self)
        win.title("Offer Property for Sale" if is_customer_offer else "Add New Property")
        win.geometry("380x460")
        win.configure(bg="#1e293b")

        tk.Label(win, text="Property Type:", bg="#1e293b", fg="white").pack(anchor="w", padx=20, pady=(10, 2))
        ptype_var = tk.StringVar(value="Land")
        ttk.Combobox(win, textvariable=ptype_var, values=["Land", "House", "Apartment"], state="readonly").pack(fill="x", padx=20)

        entries = {}
        for lbl in ["Property ID (e.g. land5)", "City", "Neighborhood", "Price", "Extra 1 (Size / Floors / Floor)", "Extra 2 (Apartments / Rooms)"]:
            tk.Label(win, text=lbl, bg="#1e293b", fg="white").pack(anchor="w", padx=20, pady=(8, 2))
            e = tk.Entry(win, bg="#0f172a", fg="white", insertbackground="white")
            e.pack(fill="x", padx=20, ipady=3)
            entries[lbl] = e


        def submit():
            pid = entries["Property ID (e.g. land5)"].get().strip()
            city = entries["City"].get().strip()
            nb = entries["Neighborhood"].get().strip()
            price = entries["Price"].get().strip()
            ex1 = entries["Extra 1 (Size / Floors / Floor)"].get().strip()
            ex2 = entries["Extra 2 (Apartments / Rooms)"].get().strip()
            pt = ptype_var.get()

            if not pid or not city or not price:
                messagebox.showerror("Error", "Please fill ID, City, and Price!")
                return

            data = {"city": city, "neighborhood": nb, "price": price}
            if pt == "Land":
                data["size"] = ex1 or "1000 hector"
                target = lands
            elif pt == "House":
                data["floors"] = ex1 or "2"
                data["number of apartments"] = ex2 or "4"
                target = houses
            else:
                data["floor"] = ex1 or "1"
                data["number of rooms"] = ex2 or "4"
                target = apartments

            if is_customer_offer:
                data["type"] = pt
                request_of_sell[pid] = data
                save_all_data()
                messagebox.showinfo("Submitted", "Your property sale offer has been sent to the Manager!")
            else:
                if pid in target:
                    messagebox.showerror("Error", "Property ID already exists!")
                    return
                target[pid] = data
                save_all_data()
                self.refresh_properties_table()
                messagebox.showinfo("Success", f"{pt} added successfully!")
            win.destroy()

        tk.Button(win, text="Save / إرسال", bg="#10b981", fg="white", font=("Arial", 10, "bold"), command=submit).pack(fill="x", padx=20, pady=15, ipady=5)

    def edit_selected_property(self):
        sel = self.prop_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a property from the table first!")
            return
        pid, ptype, city, nb, price, _ = self.prop_tree.item(sel[0])["values"]
        target = lands if ptype == "Land" else houses if ptype == "House" else apartments

        new_city = simpledialog.askstring("Edit City", "Enter new city:", initialvalue=city)
        new_nb = simpledialog.askstring("Edit Neighborhood", "Enter new neighborhood:", initialvalue=nb)
        new_price = simpledialog.askstring("Edit Price", "Enter new price:", initialvalue=str(price))

        if new_city and new_nb and new_price:
            target[pid]["city"] = new_city.strip()
            target[pid]["neighborhood"] = new_nb.strip()
            target[pid]["price"] = new_price.strip()
            save_all_data()
            self.refresh_properties_table()
            messagebox.showinfo("Updated", f"{pid} updated successfully!")

    def mark_selected_sold(self):
        sel = self.prop_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a property to mark as sold!")
            return
        pid, ptype, *_ = self.prop_tree.item(sel[0])["values"]
        if ptype == "Land" and pid in lands:
            sold_lands[pid] = lands.pop(pid)
        elif ptype == "House" and pid in houses:
            sold_houses[pid] = houses.pop(pid)
        elif ptype == "Apartment" and pid in apartments:
            sold_apartments[pid] = apartments.pop(pid)
        save_all_data()
        self.refresh_properties_table()
        messagebox.showinfo("Confirmed", f"Property '{pid}' marked as SOLD!")

    def customer_purchase_request(self):
        sel = self.prop_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a property you want to buy!")
            return
        pid, ptype, city, nb, price, _ = self.prop_tree.item(sel[0])["values"]
        request_of_purchase[self.current_user_id] = {"property_id": pid, "type": ptype, "city": city, "neighborhood": nb, "price": str(price)}
        save_all_data()
        messagebox.showinfo("Request Sent", f"Purchase interest request for '{pid}' sent to management!")

    # ==========================================
    # تبويب إدارة الموظفين (للمدير)
    # ==========================================
    def build_employees_tab(self, parent):
        cols = ("ID", "Name", "Email", "Phone", "Password", "SecretWord")
        self.emp_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols:
            self.emp_tree.heading(c, text=c)
            self.emp_tree.column(c, width=150, anchor="center")
        self.emp_tree.pack(fill="both", expand=True, pady=10)

        btn_bar = tk.Frame(parent, bg="#0f172a")
        btn_bar.pack(fill="x", pady=5)
        tk.Button(btn_bar, text="+ Add Employee (إضافة موظف)", bg="#10b981", fg="white", font=("Arial", 10, "bold"), padx=10, command=self.add_employee_dialog).pack(side="left", padx=5)
        tk.Button(btn_bar, text="Delete Selected Employee (حذف)", bg="#e11d48", fg="white", font=("Arial", 10, "bold"), padx=10, command=self.delete_selected_employee).pack(side="left", padx=5)

        self.refresh_employees_table()

    def refresh_employees_table(self):
        for r in self.emp_tree.get_children():
            self.emp_tree.delete(r)
        for uid, d in accounts.items():
            if d.get("role") == "employee":
                self.emp_tree.insert("", "end", values=(uid, d.get("name", ""), d.get("email", ""), d.get("phone", ""), d.get("password", ""), d.get("secretword", "")))

    def add_employee_dialog(self):
        win = tk.Toplevel(self)
        win.title("Add Employee")
        win.geometry("350x420")
        win.configure(bg="#1e293b")
        fields = {}
        for lbl in ["Employee ID", "Name", "Email", "Phone", "Password", "Secret Word"]:
            tk.Label(win, text=lbl, bg="#1e293b", fg="white").pack(anchor="w", padx=20, pady=(8, 2))
            e = tk.Entry(win, bg="#0f172a", fg="white", insertbackground="white")
            e.pack(fill="x", padx=20, ipady=3)
            fields[lbl] = e

        def save_emp():
            eid = fields["Employee ID"].get().strip()
            if not eid or eid in accounts:
                messagebox.showerror("Error", "Invalid or existing ID!")
                return
            accounts[eid] = {
                "name": fields["Name"].get().strip(),
                "email": fields["Email"].get().strip(),
                "phone": fields["Phone"].get().strip(),
                "password": fields["Password"].get().strip(),
                "secretword": fields["Secret Word"].get().strip(),
                "role": "employee"
            }
            save_all_data()
            self.refresh_employees_table()
            win.destroy()

        tk.Button(win, text="Save Employee", bg="#10b981", fg="white", font=("Arial", 10, "bold"), command=save_emp).pack(fill="x", padx=20, pady=15, ipady=5)

    def delete_selected_employee(self):
        sel = self.emp_tree.selection()
        if not sel:
            return
        eid = self.emp_tree.item(sel[0])["values"][0]
        if eid in accounts:
            del accounts[eid]
            save_all_data()
            self.refresh_employees_table()
            messagebox.showinfo("Deleted", f"Employee {eid} deleted.")

    # ==========================================
    # تبويب طلبات وعروض الزبائن (للمدير)
    # ==========================================
    def build_requests_tab(self, parent):
        tk.Label(parent, text="Purchase Requests (طلبات الشراء) & Sale Offers (عروض البيع):", bg="#0f172a", fg="#38bdf8", font=("Arial", 11, "bold")).pack(anchor="w", pady=5)
        cols = ("Request Type", "ID / Customer", "City", "Neighborhood", "Price")
        self.req_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols:
            self.req_tree.heading(c, text=c)
            self.req_tree.column(c, width=180, anchor="center")
        self.req_tree.pack(fill="both", expand=True, pady=5)

        tk.Button(parent, text="Confirm Selected Sale Offer (قبول عرض البيع وإضافته للبرنامج)", bg="#10b981", fg="white", font=("Arial", 10, "bold"), pady=6, command=self.approve_sale_offer).pack(pady=10)
        self.refresh_requests_table()

    def refresh_requests_table(self):
        for r in self.req_tree.get_children():
            self.req_tree.delete(r)
        for cid, d in request_of_purchase.items():
            self.req_tree.insert("", "end", values=("Purchase Request", cid, d.get("city", ""), d.get("neighborhood", ""), d.get("price", "")))
        for pid, d in request_of_sell.items():
            self.req_tree.insert("", "end", values=("Sale Offer", pid, d.get("city", ""), d.get("neighborhood", ""), d.get("price", "")))

    def approve_sale_offer(self):
        sel = self.req_tree.selection()
        if not sel:
            return
        rtype, pid, *_ = self.req_tree.item(sel[0])["values"]
        if rtype != "Sale Offer" or pid not in request_of_sell:
            messagebox.showwarning("Notice", "Please select a 'Sale Offer' row to approve!")
            return
        offer = request_of_sell.pop(pid)
        pt = offer.pop("type", "Land")
        if pt == "Land":
            lands[pid] = offer
        elif pt == "House":
            houses[pid] = offer
        else:
            apartments[pid] = offer
        save_all_data()
        self.refresh_requests_table()
        self.refresh_properties_table()
        messagebox.showinfo("Approved", f"Property '{pid}' added to available {pt}s!")

    # ==========================================
    # تبويب الموظف: إضافة مستأجر وحساب الإيجار
    # ==========================================
    def build_employee_tenant_tab(self, parent):
        frame = tk.Frame(parent, bg="#1e293b", padx=20, pady=20)
        frame.pack(fill="both", expand=True, pady=10)

        tk.Label(frame, text="Tenant Rent Calculator (حاسبة إيجار المستأجرين - 10% شهرياً)", font=("Arial", 12, "bold"), bg="#1e293b", fg="#38bdf8").pack(anchor="w", pady=(0, 10))
        tenant_ids = [uid for uid, d in accounts.items() if d.get("role") == "tenant"]
        self.emp_ten_var = tk.StringVar(value=tenant_ids[0] if tenant_ids else "")
        cb = ttk.Combobox(frame, textvariable=self.emp_ten_var, values=tenant_ids, state="readonly", width=30)
        cb.pack(anchor="w", pady=5)

        res_lbl = tk.Label(frame, text="", font=("Arial", 12, "bold"), bg="#1e293b", fg="#10b981", justify="left")
        res_lbl.pack(anchor="w", pady=15)

        def calc():
            tid = self.emp_ten_var.get()
            if tid in accounts:
                t_acc = accounts[tid]
                price = float(t_acc.get("price", 1000))
                res_lbl.config(text=f"Tenant Name: {t_acc.get('name')}\nProperty Price: ${price:,.2f}\nMonthly Rent (10%): ${price * 0.1:,.2f}\nAnnual Rent: ${price * 1.2:,.2f}\nSecurity Deposit (20%): ${price * 0.2:,.2f}")

        tk.Button(frame, text="Calculate Payment / احسب الإيجار", bg="#0284c7", fg="white", font=("Arial", 10, "bold"), command=calc).pack(anchor="w")
        calc()

    # ==========================================
    # لوحة تحكم المستأجر (Tenant Dashboard)
    # ==========================================
    def build_tenant_dashboard(self, parent):
        user = accounts[self.current_user_id]
        price = float(user.get("price", 1000))
        monthly = price * 0.1

        card = tk.Frame(parent, bg="#1e293b", padx=25, pady=25)
        card.pack(fill="both", expand=True, pady=10)

        tk.Label(card, text="YOUR LEASED PROPERTY & RENT DETAILS", font=("Arial", 13, "bold"), bg="#1e293b", fg="#fbbf24").pack(anchor="w", pady=(0, 10))
        info_text = (
            f"Tenant Name: {user.get('name')}\n"
            f"City: {user.get('city', 'Taiz')} | Neighborhood: {user.get('neighborhood', 'Alrodah')}\n"
            f"Property Value: ${price:,.2f}\n"
            f"Monthly Rent (10%): ${monthly:,.2f}\n"
            f"Annual Rent (12 Months): ${monthly * 12:,.2f}\n"
            f"Security Deposit (20%): ${price * 0.2:,.2f}"
        )
        tk.Label(card, text=info_text, font=("Arial", 11), bg="#0f172a", fg="white", justify="left", padx=15, pady=15).pack(fill="x", pady=10)

        # حاسبة عدد الأشهر
        calc_row = tk.Frame(card, bg="#1e293b")
        calc_row.pack(fill="x", pady=10)
        tk.Label(calc_row, text="Enter Number of Months to Calculate:", bg="#1e293b", fg="white", font=("Arial", 10, "bold")).pack(side="left")
        months_ent = tk.Entry(calc_row, width=10, bg="#0f172a", fg="white", insertbackground="white")
        months_ent.insert(0, "6")
        months_ent.pack(side="left", padx=10)
        total_lbl = tk.Label(calc_row, text=f"Total: ${monthly * 6:,.2f}", bg="#1e293b", fg="#10b981", font=("Arial", 11, "bold"))
        total_lbl.pack(side="left", padx=10)

        def calc_m():
            try:
                m = int(months_ent.get())
                total_lbl.config(text=f"Total for {m} months: ${monthly * m:,.2f}")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number of months")

        tk.Button(calc_row, text="Calculate", bg="#0284c7", fg="white", command=calc_m).pack(side="left")

        tk.Button(card, text="Request Contract Renewal (طلب تجديد العقد)", bg="#10b981", fg="white", font=("Arial", 10, "bold"), pady=6, command=lambda: messagebox.showinfo("Renewal", "Contract renewal request has been sent to management.")).pack(anchor="w", pady=10)


if __name__ == "__main__":
    app = PropertyManagementApp()
    app.mainloop()