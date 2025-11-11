
# Stock Management System (PySide6) with Cart & Customer Management

A simple desktop **stock & sales management** app built with **PySide6** and **SQLite**.  
Features include product/variant management, a persistent cart, checkout with partial/full payments, and customer management.  
The app stores its SQLite DB and user images in the user's data folder (AppData on Windows / `~/.local/share` on Linux/macOS) so updates won't overwrite user data.

# use with operating systems dark theme selected otherwise colors will be unexpected 

---

## Features
- 📦 Product & variant management (with images)
- 🛒 Persistent cart (draft sale) and checkout
- 👤 Customer creation & tracking (payment status, balance)
- 💳 Partial/full payment recording and payment history
- 💾 SQLite database stored in user data folder (persistent across updates)
- 🖥️ GUI built with PySide6

---

## Requirements
- Python 3.10+ (recommend latest)
- `PySide6`

Install requirements:
```bash
pip install -r requirements.txt
````

---

## Quick start (run from source)

1. Clone:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd Stock-Management-System
```

2. (Optional but recommended) Create a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run app:

```bash
python main.py
```

---

## Build a Windows executable (PyInstaller)

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Convert your app icon to `.ico` (recommended for Windows) and place it in `assets/icons/`.
3. Build:

```bash
pyinstaller --noconfirm --onefile --windowed main.py --name StockPy --icon=assets/icons/stock.ico
```

* The built exe will appear in `dist/StockPy.exe`.
* Note: The taskbar/exe icon comes from the `.ico` passed to PyInstaller. Keep `setWindowIcon()` in code for in-window icons.

---

## Where data and images are stored

The app stores data in a per-user folder:

* **Windows:** `%APPDATA%\StockManager\stock_management.db`
* **Linux/macOS:** `~/.local/share/StockManager/stock_management.db`

Images copied from users are saved under `.../StockManager/images/`.

This keeps user data persistent across app updates.

---
Excellent point 👍 — yes, you should include both **purchase** and **selling** prices in your JSON format.

Here’s the **correct and updated JSON format section** you can add directly to your README:

---

## 🧾 JSON Import Format

When importing products from a JSON file, make sure your file follows this structure:

```json
[
    {
        "Name": "F21 Pro 4G",
        "Brand": "Oppo",
        "Categories": {
            "M+B": {
                "Purchase Price": 900,
                "Selling Price": 1500
            },
            "B": {
                "Purchase Price": 750,
                "Selling Price": 1200
            },
            "Housing Full": {
                "Purchase Price": 1200,
                "Selling Price": 1800
            }
        }
    },
    {
        "Name": "A17",
        "Brand": "Oppo",
        "Categories": {
            "Housing Full": {
                "Purchase Price": 750,
                "Selling Price": 1150
            }
        }
    }
]
```

### Notes:

* `"Name"` → Product name (**required**)
* `"Brand"` → Brand name (**optional but recommended**)
* `"Categories"` → Each category key (like `"M+B"` or `"Housing Full"`) contains:

  * `"Purchase Price"` — the cost price
  * `"Selling Price"` — the retail price
* Missing or empty category entries will be **skipped automatically** during import.
* JSON files can be created manually or generated from `.csv` using any provided CSV-to-JSON converter tool.

---





## License

MIT

```
```
