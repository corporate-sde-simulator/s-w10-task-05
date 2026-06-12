# Beginner Explanatory Guide: DATA-203: Refactor Legacy Database Schema

> **Task Type**: Service Task  
> **Domain/Focus**: Database Schema Normalization

---

## 1. The Goal (In-Depth Beginner Explanation)

### The Core Problem
In many applications, especially those that have been around for a while, the database schema can become unwieldy and inefficient. This task focuses on a legacy `orders` table that has grown to over 50 columns, many of which contain redundant data. This means that the same customer information is repeated multiple times for different orders, leading to wasted storage space and potential inconsistencies. For example, if a customer's email changes, it would need to be updated in multiple places, increasing the risk of errors.

The lack of proper indexing on frequently queried columns further exacerbates the problem. Without indexes, the database has to scan the entire table to find relevant records, which slows down performance significantly, especially as the amount of data grows. This task aims to refactor the `orders` table into a more efficient, normalized structure, which will not only reduce redundancy but also improve query performance and maintainability. Normalization is a process that organizes data in a way that minimizes duplication and dependency.

Fixing this issue is crucial for the overall health of the application. A well-structured database enhances performance, reduces the risk of data anomalies, and makes it easier for developers to work with the data. Users will benefit from faster response times and more reliable data handling, which ultimately leads to a better user experience.

### Jargon Buster (Key Terms Explained)
* **Normalization**: This is the process of organizing data in a database to reduce redundancy and improve data integrity. For example, instead of storing customer information in every order, we create a separate `customers` table and link it to the `orders` table using a unique customer ID.

* **Indexing**: An index is a data structure that improves the speed of data retrieval operations on a database table. Think of it like an index in a book; instead of reading every page to find a topic, you can quickly look it up in the index. For instance, if we index the `customer_id` in the `orders` table, queries that filter by customer will run much faster.

* **Foreign Key**: A foreign key is a field (or collection of fields) in one table that uniquely identifies a row of another table. It establishes a relationship between the two tables. For example, in our new `orders` table, `customer_id` serves as a foreign key that links to the `customers` table, ensuring that every order is associated with a valid customer.

* **Denormalization**: This is the opposite of normalization, where data is intentionally duplicated to improve read performance at the cost of increased storage and potential data anomalies. In our case, the legacy `orders` table is denormalized, leading to redundancy.

### Expected Outcome
After implementing the solution, the database schema will be significantly improved. 

**Before**: The `orders` table contains redundant customer data, lacks indexes, and is difficult to maintain. Queries are slow, and data integrity is at risk due to duplication.

**After**: The database will have separate `customers`, `products`, `orders`, and `order_items` tables. Each table will be properly indexed, ensuring fast query performance. The data will be normalized, meaning customer information is stored only once, reducing redundancy and improving data integrity. This structured approach will make it easier to manage and query the data effectively.

---

## 2. Related Coding Concepts & Syntax (50% Theory, 50% Practice)

### Concept 1: Database Schema Design
#### 📘 Theoretical Overview (50%)
* **Why it exists**: Database schema design is crucial because it defines how data is organized, stored, and accessed. A well-designed schema ensures that data is stored efficiently and can be retrieved quickly. Poor schema design can lead to data redundancy, inconsistency, and performance issues. Without a proper schema, applications may struggle to scale and maintain data integrity.

* **Key Mechanisms**: The core mechanisms of schema design include defining tables, columns, data types, and relationships between tables. Normalization is a key aspect, which involves dividing large tables into smaller, related tables to eliminate redundancy. Each table should have a primary key that uniquely identifies each record, and foreign keys should be used to establish relationships between tables.

#### 💻 Syntax & Practical Examples (50%)
* **Language Syntax**:
  ```sql
  CREATE TABLE customers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      phone TEXT
  );
  ```
  - `CREATE TABLE`: This command is used to create a new table in the database.
  - `customers`: The name of the table being created.
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`: This defines a column named `id` that is an integer, serves as the primary key, and will automatically increment with each new record.
  - `name TEXT NOT NULL`: This defines a column for the customer's name, which cannot be null.
  - `email TEXT NOT NULL UNIQUE`: This defines a column for the customer's email, which must be unique and cannot be null.

* **Real-World Application**:
  ```sql
  INSERT INTO customers (name, email, phone)
  VALUES ('John Doe', 'john@example.com', '123-456-7890');
  ```
  - This command inserts a new customer record into the `customers` table. The values provided correspond to the columns defined in the table.

---

## 3. Step-by-Step Logic & Walkthrough

1. **Step 1: Locate and Analyze the Target File**
   * Navigate to the `src/` folder in your project directory. The relevant file for this task is `migration.py`.
   * Open `migration.py` and inspect the functions defined within it, particularly `create_legacy_schema`, `migrate_schema`, and `migrate_data`.

2. **Step 2: Input Verification & Validation**
   * Before running the migration, ensure that the legacy schema is created by calling `create_legacy_schema(conn)` to set up the initial state of the database.
   * Check if the `legacy_orders` table exists and contains data. You can do this by executing a simple `SELECT` query.

3. **Step 3: Core Implementation / Modification**
   * In the `migrate_schema` function, ensure that the new tables (`customers`, `products`, `orders`, and `order_items`) are created correctly.
   * In the `migrate_data` function, modify the SQL statements to ensure that data is migrated correctly without creating duplicates. For example, use `INSERT OR IGNORE` to avoid inserting duplicate customer records.

4. **Step 4: Output Verification & Testing**
   * After implementing the changes, run the test suite using `pytest` to verify that all tests pass. This will ensure that the migration logic works as intended and that the new schema is functioning correctly.

---

## 4. Detailed Walkthrough of Test Cases

### Test Case 1: Standard / Success Case
* **Description**: This test checks if the `customers` table has a unique constraint on the email column, ensuring no duplicate emails are allowed.
* **Inputs**:
  ```json
  {
      "name": "Jane Doe",
      "email": "jane@example.com",
      "phone": "987-654-3210"
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `migrate_schema` function is called, creating the `customers` table.
  2. The test queries the index list for the `customers` table.
  3. It checks if there is a unique index on the `email` column.
  4. The test passes if a unique index exists.

* **Expected Output**: The test should pass, confirming that the `customers.email` column has a UNIQUE constraint.

### Test Case 2: Edge Case / Validation Fail
* **Description**: This test checks if the `orders` table has a foreign key constraint linking to the `customers` table.
* **Inputs**:
  ```json
  {
      "order_id": 1,
      "customer_id": 999,  // Assuming this ID does not exist in the customers table
      "order_date": "2023-10-01",
      "status": "pending"
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `migrate_schema` function is called, creating the `orders` table.
  2. The test queries the foreign key list for the `orders` table.
  3. It checks if there are any foreign keys defined.
  4. If no foreign keys are found, the test fails.

* **Expected Output**: The test should fail if the foreign key constraint is not set up correctly, indicating that the `orders` table does not properly link to the `customers` table.