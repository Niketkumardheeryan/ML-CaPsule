
---

# 🗄️ SQL Cheat Sheet

````markdown
# 🗄️ SQL Cheat Sheet

## Links to refer
https://dev.mysql.com/doc/

https://dev.mysql.com/doc/mysql-tutorial-excerpt/



---

## SQL Execution Order

```
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

---

## SELECT

```sql
SELECT * FROM employees;
```

---

## WHERE

```sql
SELECT *
FROM employees
WHERE salary > 50000;
```

---

## ORDER BY

```sql
SELECT *
FROM employees
ORDER BY salary DESC;
```

---

## GROUP BY

```sql
SELECT department,
COUNT(*)
FROM employees
GROUP BY department;
```

---

## HAVING

```sql
SELECT department,
AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary)>50000;
```

---

## Aggregate Functions

```sql
COUNT()

SUM()

AVG()

MAX()

MIN()
```

---

## INSERT

```sql
INSERT INTO employee
VALUES(1,'John',50000);
```

---

## UPDATE

```sql
UPDATE employee
SET salary=60000
WHERE id=1;
```

---

## DELETE

```sql
DELETE FROM employee
WHERE id=1;
```

---

## JOINS

```sql
INNER JOIN

LEFT JOIN

RIGHT JOIN

FULL JOIN
```

---

## CREATE TABLE

```sql
CREATE TABLE Student(
id INT PRIMARY KEY,
name VARCHAR(50)
);
```

---

## ALTER TABLE

```sql
ALTER TABLE Student
ADD Age INT;
```

---

## Constraints

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE
- NOT NULL
- CHECK
- DEFAULT

---

## Interview Tips

✔ WHERE filters rows

✔ HAVING filters groups

✔ GROUP BY before HAVING

✔ INDEX improves searching

✔ PRIMARY KEY is Unique