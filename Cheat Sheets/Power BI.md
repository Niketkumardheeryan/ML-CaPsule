# 📊 Power BI Cheat Sheet

> One-page quick reference for Microsoft Power BI.

---
# Links to refer
https://learn.microsoft.com/en-us/power-bi/

---

# Power BI Workflow

```
Get Data
      ↓
Power Query
      ↓
Clean Data
      ↓
Load Data
      ↓
Create Relationships
      ↓
Create Measures (DAX)
      ↓
Build Reports
      ↓
Publish Dashboard
```

---

# Power BI Components

| Component | Purpose |
|------------|---------|
| Power Query | Data Cleaning |
| Data View | View Tables |
| Model View | Relationships |
| Report View | Visualizations |
| Power BI Service | Share Reports |

---

# Data Loading

- Excel
- CSV
- SQL Server
- MySQL
- PostgreSQL
- Oracle
- Web
- Azure

---

# Power Query Tasks

- Remove Duplicates
- Replace Values
- Split Columns
- Merge Queries
- Append Queries
- Pivot
- Unpivot
- Change Data Types

---

# Relationships

```
One-to-One (1:1)

One-to-Many (1:*)

Many-to-Many (*:*)
```

---

# Data Model

```
Fact Table

↓

Dimension Tables

↓

Star Schema
```

⭐ Star Schema is recommended.

---

# DAX Functions

## Aggregate

```DAX
SUM()

AVERAGE()

COUNT()

MIN()

MAX()
```

---

## Logical

```DAX
IF()

SWITCH()

AND()

OR()
```

---

## Filter

```DAX
CALCULATE()

FILTER()

ALL()

VALUES()
```

---

## Date

```DAX
TODAY()

NOW()

YEAR()

MONTH()

DAY()
```

---

## Common Examples

### Total Sales

```DAX
Total Sales =
SUM(Sales[Amount])
```

---

### Average Sales

```DAX
Average Sales =
AVERAGE(Sales[Amount])
```

---

### Profit

```DAX
Profit =
SUM(Sales[Sales]) - SUM(Sales[Cost])
```

---

### Safe Division

```DAX
DIVIDE(A,B,0)
```

---

# Measures vs Calculated Columns

| Measure | Calculated Column |
|----------|-------------------|
| Dynamic | Stored |
| Uses less memory | Uses more memory |
| Calculated during visualization | Calculated during refresh |

---

# Common Visualizations

- Bar Chart
- Column Chart
- Line Chart
- Pie Chart
- Donut Chart
- KPI
- Card
- Table
- Matrix
- Map
- Tree Map
- Scatter Plot
- Gauge
- Slicer

---

# Filters

- Visual Level
- Page Level
- Report Level
- Drill Through

---

# Dashboard Tips

✅ Keep visuals simple

✅ Use slicers

✅ Maintain consistent colors

✅ Add titles

✅ Remove unnecessary visuals

---

# Performance Tips

- Remove unused columns
- Remove duplicate rows
- Use Measures instead of Columns
- Prefer Star Schema
- Avoid many calculated columns
- Optimize relationships

---

# Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + S | Save |
| Ctrl + C | Copy Visual |
| Ctrl + V | Paste |
| Ctrl + Z | Undo |
| Ctrl + Y | Redo |
| Ctrl + F | Search |

---

# Power BI Interview Tips

✅ Power Query is used for data cleaning.

✅ DAX is used for calculations.

✅ Measures are dynamic.

✅ Calculated Columns are stored.

✅ Star Schema is preferred over Snowflake Schema.

✅ Fact Table contains numerical data.

✅ Dimension Table contains descriptive data.

✅ Relationships connect tables.

✅ Publish reports to Power BI Service.

✅ Use slicers for interactive filtering.