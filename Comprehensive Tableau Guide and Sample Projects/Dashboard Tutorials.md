## Step-by-Step Dashboard Tutorials

### Tutorial 1: Sales Performance Dashboard (Superstore)

**Goal:** Build a 3-view dashboard showing Sales by Category, Sales over Time, and a Regional Map.

---

**Step 1: Prepare your data**
1. Open Tableau, connect to **Sample - Superstore**.
2. Drag the **Orders** sheet to the canvas.

**Step 2: Create View 1 — Sales by Category (Bar Chart)**
1. Open **Sheet 1**, rename it `Sales by Category`.
2. Drag `Category` → **Rows**.
3. Drag `Sales` → **Columns**.
4. Drag `Category` → **Color** (Marks card).
5. Click the sort descending button on the axis.

**Step 3: Create View 2 — Sales over Time (Line Chart)**
1. Create a new sheet, name it `Sales Trend`.
2. Drag `Order Date` → **Columns**. Right-click → select **Month (continuous)**.
3. Drag `Sales` → **Rows**.
4. Drag `Category` → **Color**.

**Step 4: Create View 3 — Sales by State (Map)**
1. Create a new sheet, name it `Sales Map`.
2. Double-click `State`. Tableau auto-creates a map.
3. Drag `Sales` → **Color** (Marks card).
4. Edit color → choose a sequential blue palette.

**Step 5: Assemble the Dashboard**
1. Click **New Dashboard** icon.
2. Set size to **Automatic**.
3. Drag `Sales by Category` to the top-left.
4. Drag `Sales Trend` to the top-right.
5. Drag `Sales Map` to the bottom — spanning full width.
6. Add a **Text** object at the top: "Sales Performance Overview".

**Step 6: Add Interactivity**
1. Click the `Sales by Category` view on the dashboard.
2. Click the **funnel icon** (Use as Filter) that appears in the top-right of the view.
3. Now clicking a bar filters both the line chart and the map!

---

### Tutorial 2: KPI Summary Dashboard

**Goal:** Show 4 KPI numbers at the top of a dashboard (Total Sales, Total Profit, # Orders, Profit Ratio).

**Step 1: Create KPI Sheets**

For each KPI, create a new sheet:
1. Drag the measure (e.g., `Sales`) to **Text** in the Marks card.
2. Change the mark type to **Text** (from the Marks dropdown).
3. Right-click the measure on the Text card → **Format** → increase font size to 28–36pt.
4. Remove all headers and gridlines: **Format > Lines** → set all to None.

**Step 2: Create Profit Ratio Calculated Field**
```tableau
SUM([Profit]) / SUM([Sales])
```
Format as percentage (right-click → Default Properties → Number Format → Percentage).

**Step 3: Assemble**
1. On a new dashboard, drag the 4 KPI sheets side by side at the top in a **Horizontal container**.
2. Below them, add a trend chart or table.
3. Add a date filter to control the KPI period.

---

### Tutorial 3: Customer Segmentation Scatter Plot

**Goal:** Visualize customers by their Sales vs Profit, colored by Segment.

1. Create a new sheet.
2. Drag `Sales` → **Columns** (it will aggregate to SUM).
3. Drag `Profit` → **Rows**.
4. Drag `Customer Name` → **Detail** (Marks card). This disaggregates to one mark per customer.
5. Drag `Segment` → **Color**.
6. Drag `Profit` → **Size** (optional — bubble size shows profit magnitude).
7. Add a **Reference Line** at 0 on the Profit axis (right-click axis → Add Reference Line → Value = 0, Label = None, dashed red line).

Now you can clearly see unprofitable customers (below the 0 line) vs profitable ones.

---