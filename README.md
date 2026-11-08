# 🏢 Property Management System (نظام إدارة العقارات)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-0284c7?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-10b981?style=for-the-badge)

A comprehensive **Property Management System (PMS)** built in Python. This project provides both a modern dark-themed **Graphical User Interface (Tkinter GUI)** and a classic **Command-Line Interface (CLI)** to manage real estate properties (Lands, Houses, and Apartments), employee accounts, tenant leases, and customer purchase/sale requests with persistent `.txt` file storage.

---

##  Key Features

* **Dual Interface Support:**
  * 🖥️ **Modern Desktop GUI (`pms_gui.py`):** Features a sleek dark slate theme, interactive `Treeview` data tables, instant search/filter bars, and 1-click demo login buttons.
  * ⌨️ **Interactive CLI (`property.management.system.py`):** Menu-driven console application for terminal-based operations.
* **Role-Based Access Control (RBAC):** Custom dashboards and permissions tailored for **Managers**, **Employees**, **Tenants**, and **Customers**.
* **Real Estate Inventory Management:** Full CRUD (Create, Read, Update, Delete/Mark as Sold) support for **Lands**, **Houses**, and **Apartments**.
* **Advanced Search & Sorting:** Filter properties by type, city, neighborhood, or price range, and sort listings by city name or price.
* **Automated Rent & Deposit Calculator:** Automatically computes monthly rent ($10\%$ of property value), annual rent, security deposits ($20\%$), and custom multi-month lease totals.
* **Security & Account Recovery:** Login attempt limiter ($3$ attempts) and password recovery using personal secret words.
* **Persistent Text-File Database:** Automatically loads and saves all inventory, user accounts, and transaction requests to structured `.txt` files upon startup and exit.

---

##  User Roles & Permissions

| Role | Capabilities |
| :--- | :--- |
| ** Manager** | • View, search, sort, add, and edit all property listings.<br>• Confirm property sales and move items to sold archives.<br>• Manage employee accounts (Add, View, Edit, Delete).<br>• Review customer purchase requests and approve customer property sale offers. |
| ** Employee** | • Search, filter, add, and edit property listings.<br>• Register new tenants and assign them to properties.<br>• Calculate monthly/annual rent payments for tenants. |
| ** Tenant** | • View leased property details.<br>• View breakdown of monthly rent, annual rent, and security deposit.<br>• Use the interactive rent calculator for custom month durations.<br>• Request contract renewals and update personal profile details. |
| ** Customer** | • Register a new customer account.<br>• Browse, search, and sort available Lands, Houses, and Apartments.<br>• Submit purchase interest requests to management.<br>• Submit offers to list personal properties for sale in the system. |

---

##  Default Accounts (Demo Credentials)

You can log in using the following pre-configured accounts (or use the **Quick Demo Login** buttons in the GUI):

| Role | Username (`ID`) | Password | Secret Word | User Name |
| :--- | :--- | :--- | :--- | :--- |
| **Manager** | `admin` | `moh4321` | `CR7` | Mohammed AL-SHAMERI |
| **Employee 1** | `emp1` | `messi10` | `M10` | Mohammed Al-sharafi |
| **Employee 2** | `emp2` | `5432167890` | `CR7` | Mohammed Isameil |
| **Employee 3** | `emp3` | `ronaldo4321` | `CR7` | Mohaned Al-wajeh |
| **Tenant** | `ten1` | `11223344` | `M10` | Qusai |
| **Customer** | `cus1` | `11223344` | `M10` | Ahmed |

---

##  Project Structure

```text
📦 Property-Management-System
 ┣ 📜 pms_gui.py                      # Main Graphical User Interface (Tkinter) application
 ┣ 📜 property.management.system.py   # Command-Line Interface (CLI) application
 ┣ 📜 README.md                       # Project documentation
 ┃
 ┣ 📂 Data Files (Auto-generated / Loaded on run)
 ┃ ┣ 📄 property_l.txt                # Available lands database
 ┃ ┣ 📄 property_houses.txt           # Available houses database
 ┃ ┣ 📄 property_apartment.txt        # Available apartments database
 ┃ ┣ 📄 sold.property.lands.txt       # Archived sold lands
 ┃ ┣ 📄 sold.property.houses.txt      # Archived sold houses
 ┃ ┣ 📄 sold.property.apartments.txt  # Archived sold apartments
 ┃ ┣ 📄 purchase_requsets.txt         # Customer purchase interest requests
 ┃ ┣ 📄 offers_requset.txt            # Customer property sale offers
 ┃ ┗ 📄 users.account.txt             # User accounts, roles, and credentials
```

---

##  Getting Started

### Prerequisites

* **Python 3.x** installed on your system.
* `tkinter` (comes pre-installed with standard Python distributions on Windows and macOS; on Linux, install via `sudo apt-get install python3-tk`).

### Running the Graphical Interface (Recommended)

```bash
python pms_gui.py
```

### Running the Command-Line Interface (CLI)

```bash
python property.management.system.py
```
*(Note: Ensure the `.txt` data files exist in the same directory when running the CLI version for the first time, or run `pms_gui.py` first and close it to auto-generate all required `.txt` files with default data).*

---

##  Rent Calculation Formula

For leased properties, the system calculates rental fees based on the property's listed price ($P$):

$$\text{Monthly Rent} = P \times 0.10$$

$$\text{Annual Rent} = \text{Monthly Rent} \times 12 = P \times 1.20$$

$$\text{Security Deposit} = P \times 0.20$$

