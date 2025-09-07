
# Stock Management System (PySide6) with Cart & Customer Management

A simple desktop **stock & sales management** app built with **PySide6** and **SQLite**.  
Features include product/variant management, a persistent cart, checkout with partial/full payments, and customer management.  
The app stores its SQLite DB and user images in the user's data folder (AppData on Windows / `~/.local/share` on Linux/macOS) so updates won't overwrite user data.

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

## What to push to GitHub

* Push **source files** only (`src/`, `assets/`, `README.md`, `requirements.txt`, etc.)
* **Do not** commit `dist/`, `build/`, or `*.exe` files. Use GitHub Releases for binaries.

---

## License

MIT

```
```
