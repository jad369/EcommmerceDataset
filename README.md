# E-Commerce Data Analysis

Python ETL pipeline for cleaning and analyzing retail transaction data.

---

## Requirements

- Python 3.8+
- flake8 and flake8-html (for code quality)

---

## Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```bash
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flake8 flake8-html black
```

---

## Running the Program

### 1. Make sure virtual environment is activated

You should see `(venv)` at the start of your prompt.

### 2. Run the ETL pipeline
```bash
python main.py
```

### 3. Output

The program will:
- Clean data (merge files, remove cancelled orders, filter bad data)
- Generate analytics
- Create 6 CSV reports

---

## Code Quality

### Format Code (Optional)
```bash
black *.py
```

### Generate flake8 Report
```bash
flake8 --format=html --htmldir=flake8-report --exclude=venv .
```

View the report:

**Windows:**
```bash
start flake8-report\index.html
```

**Mac:**
```bash
open flake8-report/index.html
```

**Linux:**
```bash
xdg-open flake8-report/index.html
```

---

## Input Files Required

- `09_10_dataset.csv`
- `10_11_dataset.csv`

Place these files in the same folder as `main.py`

---

## Output Files

- `final_dataset.csv` - Cleaned data
- `monthly_sales_2010.csv` - Monthly sales for 2010
- `monthly_sales_2011.csv` - Monthly sales for 2011
- `stock_code_by_year.csv` - Products by year
- `country_sales_2010.csv` - Country sales for 2010
- `country_sales_2011.csv` - Country sales for 2011

---

## Project Structure
```
OOP/
├── customer.py           # Customer model
├── product.py            # Product model
├── invoice.py            # Invoice model
├── mappers.py            # CSV to object mappers
├── output_models.py      # Output formatting
├── data_cleaner.py       # Data cleaning pipeline
├── processors.py         # CSV data processor
├── analytics.py          # Analytics and reporting
├── reports.py            # Report generation
├── main.py               # Main script
├── 09_10_dataset.csv     # Input data
├── 10_11_dataset.csv     # Input data
└── README.md             # This file
```

---

## Deactivate Virtual Environment

When finished:
```bash
deactivate
```

---

## Author
Jorge Davila