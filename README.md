# skincare-inventory-web

# Skincare Inventory Tracker

This is a simple web app built with Python and Flask that helps track skincare product inventory and purchases.

---

## What It Does

- Shows current stock of skincare products  
- Lets users "purchase" products (reducing stock by 1 each time)  
- Logs each purchase with a timestamp  
- Shows a purchase history page with all purchases  
- Warns when product stock is low (3 or fewer items left)  

---

## Technologies Used

- **Python**: Programming language powering the app  
- **Flask**: Lightweight web framework to build the website  
- **HTML & Jinja2**: For displaying pages and data dynamically  

---

## Setup & Run Instructions

### 1. Clone the repository

```bash
git clone git@github.com:ninihuynh/skincare-inventory-web.git
cd skincare-inventory-web
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### 3. Install required packages

```bash
pip install Flask
```

### 4. Run the app

```bash
python app.py
```

### 5. Open the browser and go to

```bash
http://127.0.0.1:5000/
```

---

## How to Use

- On the homepage, see the list of skincare products and their current stock

- Click the "Purchase" button to buy one unit of a product

- If stock is low (3 or less), you will see a warning message

- Go to /log page (click the link or type in browser) to view purchase history




