# Databricks notebook source
# DBTITLE 1,Day 5 — Mock Interview Practice
# MAGIC %md
# MAGIC # 📅 Day 5 — Mock Interview Practice
# MAGIC
# MAGIC **Date**: Oct 17, 2026
# MAGIC
# MAGIC **Topics Covered**:
# MAGIC | # | Category | Questions |
# MAGIC |---|----------|----------|
# MAGIC | 1 | SQL Advanced | 2 |
# MAGIC | 2 | Python (Loop/Function/List/Dict) | 2 |
# MAGIC | 3 | PySpark Coding | 2 |
# MAGIC | 4 | Spark Optimization & Deep Spark | 2 |
# MAGIC | 5 | ETL (Data Quality, Incremental Load, Deduplication) | 3 |
# MAGIC | 6 | Data Modeling | 2 |
# MAGIC | 7 | Snowflake | 2 |
# MAGIC | 8 | Monitoring, Logging & Orchestration | 3 |
# MAGIC
# MAGIC **Total**: 18 questions
# MAGIC
# MAGIC **Difficulty**: BASIC → INTERMEDIATE (Week 1)
# MAGIC
# MAGIC ---
# MAGIC **Instructions**: Read the question, try to solve it yourself first, then check the solution cell below.

# COMMAND ----------

# DBTITLE 1,Q1: Nth Highest Salary
# MAGIC %md
# MAGIC ## 🔷 Section 1: SQL Advanced (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q1: Nth Highest Salary [BASIC]
# MAGIC
# MAGIC **Table**: `salaries (emp_id, salary)`
# MAGIC
# MAGIC **Question**: Write a SQL query to find the **Nth highest salary** from the salaries table. If there is no Nth highest (e.g., N=5 but only 3 distinct salaries), return NULL. Use a **window function** approach.
# MAGIC
# MAGIC **Hint**: Use `DENSE_RANK() OVER (ORDER BY salary DESC)` and filter where rank = N. DENSE_RANK ensures ties at the same salary get the same rank.

# COMMAND ----------

# DBTITLE 1,Solution Q1
# MAGIC %sql
# MAGIC -- SOLUTION Q1
# MAGIC -- DENSE_RANK ensures salaries with the same value get the same rank
# MAGIC -- and the next distinct salary gets the next rank number
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW salaries AS
# MAGIC SELECT * FROM VALUES
# MAGIC   (1, 95000),
# MAGIC   (2, 85000),
# MAGIC   (3, 95000),
# MAGIC   (4, 70000),
# MAGIC   (5, 85000),
# MAGIC   (6, 60000)
# MAGIC AS salaries(emp_id, salary);
# MAGIC
# MAGIC -- Find the 2nd highest salary
# MAGIC WITH ranked AS (
# MAGIC   SELECT
# MAGIC     salary,
# MAGIC     DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
# MAGIC   FROM salaries
# MAGIC )
# MAGIC SELECT DISTINCT salary AS second_highest
# MAGIC FROM ranked
# MAGIC WHERE rank = 2;

# COMMAND ----------

# DBTITLE 1,Q2: First & Last Purchase
# MAGIC %md
# MAGIC ---
# MAGIC ### Q2: First and Last Purchase per Customer [INTERMEDIATE]
# MAGIC
# MAGIC **Table**: `purchases (customer_id, purchase_date, amount)`
# MAGIC
# MAGIC **Question**: Write a SQL query to find the **first** and **last** purchase date and amount for each customer. Return `customer_id, first_date, first_amount, last_date, last_amount`.
# MAGIC
# MAGIC **Hint**: Use `FIRST_VALUE()` and `LAST_VALUE()` window functions. For `LAST_VALUE`, you need `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to get the true last value.

# COMMAND ----------

# DBTITLE 1,Solution Q2
# MAGIC %sql
# MAGIC -- SOLUTION Q2
# MAGIC -- FIRST_VALUE gets the first row's value in the ordered partition
# MAGIC -- LAST_VALUE needs an explicit frame: without it, the default frame
# MAGIC -- ends at CURRENT ROW, so you'd get every row's own value, not the last.
# MAGIC -- Use ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING.
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW purchases AS
# MAGIC SELECT * FROM VALUES
# MAGIC   ('CUST-1', '2026-01-15', 100),
# MAGIC   ('CUST-1', '2026-02-20', 250),
# MAGIC   ('CUST-1', '2026-03-10', 150),
# MAGIC   ('CUST-2', '2026-01-05', 300),
# MAGIC   ('CUST-2', '2026-04-12', 200)
# MAGIC AS purchases(customer_id, purchase_date, amount);
# MAGIC
# MAGIC SELECT DISTINCT
# MAGIC   customer_id,
# MAGIC   FIRST_VALUE(purchase_date) OVER w AS first_date,
# MAGIC   FIRST_VALUE(amount)      OVER w AS first_amount,
# MAGIC   LAST_VALUE(purchase_date) OVER (
# MAGIC     PARTITION BY customer_id ORDER BY purchase_date
# MAGIC     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
# MAGIC   ) AS last_date,
# MAGIC   LAST_VALUE(amount)      OVER (
# MAGIC     PARTITION BY customer_id ORDER BY purchase_date
# MAGIC     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
# MAGIC   ) AS last_amount
# MAGIC FROM purchases
# MAGIC WINDOW w AS (PARTITION BY customer_id ORDER BY purchase_date)
# MAGIC ORDER BY customer_id;

# COMMAND ----------

# DBTITLE 1,Q3: Reverse Linked List
# MAGIC %md
# MAGIC ## 🐍 Section 2: Python (Loop / Function / List / Dict) (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q3: Reverse a Linked List [BASIC]
# MAGIC
# MAGIC **Question**: Implement a **singly linked list** in Python and write a function to **reverse it in place**. Use the iterative pointer-reversal approach (O(n) time, O(1) space).
# MAGIC
# MAGIC **Hint**: Use three pointers: `prev`, `curr`, `next`. At each step, reverse the link and advance all three.

# COMMAND ----------

# DBTITLE 1,Solution Q3
# SOLUTION Q3

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    """Reverse a singly linked list iteratively. O(n) time, O(1) space."""
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next   # save the next node
        curr.next = prev          # reverse the link
        prev = curr               # advance prev
        curr = next_node         # advance curr
    return prev                   # prev is now the new head

def list_to_array(head):
    """Helper: convert linked list to array for printing."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

# Build: 1 -> 2 -> 3 -> 4 -> 5
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)

print(f"Original: {list_to_array(head)}")
new_head = reverse_linked_list(head)
print(f"Reversed: {list_to_array(new_head)}")

# Edge case: single node
single = ListNode(42)
print(f"Single:   {list_to_array(reverse_linked_list(single))}")

# Edge case: empty list
print(f"Empty:    {list_to_array(reverse_linked_list(None))}")

# COMMAND ----------

# DBTITLE 1,Q4: Group Anagrams
# MAGIC %md
# MAGIC ---
# MAGIC ### Q4: Group Anagrams [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: Write a Python function `group_anagrams(strs)` that groups strings that are **anagrams** of each other. Return a list of lists where each inner list contains anagrams. The key insight is that anagrams produce the same sorted string.
# MAGIC
# MAGIC **Example**: `group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])` → `[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]`
# MAGIC
# MAGIC **Hint**: Use `collections.defaultdict(list)` with `tuple(sorted(s))` as the key.

# COMMAND ----------

# DBTITLE 1,Solution Q4
# SOLUTION Q4
from collections import defaultdict

def group_anagrams(strs):
    """Group strings that are anagrams of each other."""
    groups = defaultdict(list)
    
    for s in strs:
        # Sort the string to create a canonical key
        # All anagrams produce the same sorted string
        key = tuple(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

# Test cases
print(group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat']))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

print(group_anagrams(['listen', 'silent', 'enlist', 'hello', 'world']))
# [['listen', 'silent', 'enlist'], ['hello'], ['world']]

print(group_anagrams(['a']))
# [['a']]

print(group_anagrams(['']))
# [['']]

# COMMAND ----------

# DBTITLE 1,Q5: Self-Join Employee > Manager
# MAGIC %md
# MAGIC ## ⚡ Section 3: PySpark Coding (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q5: Self-Join — Employees Earning More Than Manager [BASIC]
# MAGIC
# MAGIC **DataFrame**: `employees (emp_id, emp_name, salary, manager_id)`
# MAGIC
# MAGIC **Question**: Using PySpark, find all employees who earn **more than their direct manager**. Return `emp_name, salary, manager_name, manager_salary`.
# MAGIC
# MAGIC **Hint**: Self-join the employees table on `emp.manager_id = mgr.emp_id`, then filter where the employee's salary > manager's salary.

# COMMAND ----------

# DBTITLE 1,Solution Q5
# SOLUTION Q5
from pyspark.sql import functions as F

emp_data = [
    (1, 'Alice',  90000, 3),   # Alice's manager is Carol
    (2, 'Bob',    85000, 3),   # Bob's manager is Carol
    (3, 'Carol',  80000, 4),   # Carol's manager is Dave
    (4, 'Dave',   95000, None), # Dave is the CEO (no manager)
    (5, 'Eve',    75000, 1),   # Eve's manager is Alice
    (6, 'Frank',  100000, 3),  # Frank earns more than his manager Carol
]

employees = spark.createDataFrame(emp_data, ['emp_id', 'emp_name', 'salary', 'manager_id'])

# Self-join: join employees with itself on manager_id
result = (
    employees.alias('e')
    .join(
        employees.alias('m'),
        F.col('e.manager_id') == F.col('m.emp_id'),
        'inner'
    )
    .filter(F.col('e.salary') > F.col('m.salary'))
    .select(
        F.col('e.emp_name').alias('emp_name'),
        F.col('e.salary').alias('salary'),
        F.col('m.emp_name').alias('manager_name'),
        F.col('m.salary').alias('manager_salary'),
    )
    .orderBy(F.col('e.salary').desc())
)

display(result)

# COMMAND ----------

# DBTITLE 1,Q6: Explode Nested Array
# MAGIC %md
# MAGIC ---
# MAGIC ### Q6: Explode Nested Array Column [INTERMEDIATE]
# MAGIC
# MAGIC **DataFrame**: `orders (order_id, customer_id, items)` where `items` is a **string column containing a JSON array** like `'["laptop", "mouse", "keyboard"]'`.
# MAGIC
# MAGIC **Question**: Using PySpark, parse the JSON string column into an array and **explode** it so each item gets its own row. Return `order_id, customer_id, item`.
# MAGIC
# MAGIC **Hint**: Use `F.from_json()` to parse the string into an array, then `F.explode()` to flatten it. Define the schema as `ArrayType(StringType())`.

# COMMAND ----------

# DBTITLE 1,Solution Q6
# SOLUTION Q6
from pyspark.sql import functions as F
from pyspark.sql.types import ArrayType, StringType

orders_data = [
    ('ORD-1', 'CUST-A', '["laptop", "mouse", "keyboard"]'),
    ('ORD-2', 'CUST-B', '["monitor", "cable"]'),
    ('ORD-3', 'CUST-C', '["webcam"]'),
]

orders = spark.createDataFrame(orders_data, ['order_id', 'customer_id', 'items'])

# Step 1: Parse JSON string → array using from_json with explicit schema
array_schema = ArrayType(StringType())
parsed = orders.withColumn('items_array', F.from_json(F.col('items'), array_schema))

# Step 2: Explode the array so each item gets its own row
result = (
    parsed
    .select(
        'order_id',
        'customer_id',
        F.explode('items_array').alias('item')
    )
    .orderBy('order_id', 'item')
)

display(result)

# COMMAND ----------

# DBTITLE 1,Q7: Predicate Pushdown
# MAGIC %md
# MAGIC ## 🔥 Section 4: Spark Optimization & Deep Spark (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q7: Predicate Pushdown [BASIC]
# MAGIC
# MAGIC **Question**: What is **predicate pushdown** in Spark? How does it improve query performance? Give examples of where it applies (partition pruning, column pruning, filter pushdown to data sources).
# MAGIC
# MAGIC **Hint**: Predicate pushdown moves filters as close to the data source as possible — before reading data into Spark memory.

# COMMAND ----------

# DBTITLE 1,Solution Q7
# SOLUTION Q7

"""
PREDICATE PUSHDOWN:
  - Spark pushes filter conditions DOWN to the data source layer
  - Filters are applied BEFORE data is read into Spark memory
  - Reduces I/O: only relevant data is transferred from storage to compute
  - Spark 3.x does this automatically via the Catalyst optimizer

THREE TYPES OF PUSHDOWN:

1. PARTITION PRUNING (directory-level):
   - If a table is partitioned by date, and you filter `WHERE date = '2026-01-15'`
   - Spark reads ONLY the partition directory for that date
   - Other partition directories are NEVER scanned
   - Example:
       df.filter(F.col('date') == '2026-01-15')
       → only reads /data/date=2026-01-15/

2. COLUMN PRUNING (column-level):
   - If you SELECT only 3 columns from a 20-column table
   - Spark reads ONLY those 3 columns from the Parquet/Delta files
   - Columnar formats (Parquet, Delta, ORC) store columns separately
   - Massive I/O savings: 20 cols → 3 cols = 85% less data read
   - Example:
       df.select('id', 'name')
       → reads only id and name column chunks

3. FILTER PUSHDOWN (row-level, source-specific):
   - For JDBC sources: WHERE clause is sent to the database
     → the database filters rows before sending data to Spark
   - For Delta/Parquet: min/max statistics per file → file skipping
     → if a file's min/max for a column doesn't match the filter, skip it
   - For Kafka: only consume from specific topic-partition-offset

EXAMPLE — BEFORE vs AFTER PUSHDOWN:

  BAD (no pushdown awareness):
    df = spark.read.parquet('/data/sales/')
    all_data = df.collect()                       # reads EVERYTHING
    filtered = [r for r in all_data if r.date == '2026-01-15']  # filter in Python

  GOOD (Spark does pushdown automatically):
    df = spark.read.parquet('/data/sales/')
    result = (df
              .filter(F.col('date') == '2026-01-15')  # partition pruning
              .select('id', 'amount')                  # column pruning
              .filter(F.col('amount') > 1000)           # file-level pushdown
             )
    display(result)

KEY POINT:
  Pushdown = filter at the source, not in Spark memory.
  Apply filters EARLY (before joins, before aggregations).
  Catalyst does this automatically — but only if you USE DataFrame API, not RDD.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q8: Data Skew
# MAGIC %md
# MAGIC ---
# MAGIC ### Q8: Data Skew — Causes and Solutions [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: What is **data skew** in Spark? How does it manifest in the Spark UI? List at least **three strategies** to handle it. Explain the **salting technique** in detail.
# MAGIC
# MAGIC **Hint**: Skew = one partition is much larger than others. Visible in Spark UI as one task taking much longer. Solutions: broadcast join, salting, AQE skew handling, repartition.

# COMMAND ----------

# DBTITLE 1,Solution Q8
# SOLUTION Q8

"""
DATA SKEW = one or a few partitions are MUCH larger than the rest
  - Occurs when a join/groupBy key has an uneven distribution
  - Example: 90% of records have customer_id = 'CUST-001'
  - One executor gets that huge partition → takes 10x longer than others

HOW IT MANIFESTS IN SPARK UI:
  - Stage with 200 tasks: 199 finish in 10 seconds, 1 takes 5 minutes
  - Task metrics: one task reads 50 GB, others read 100 MB each
  - Executor logs: "Container killed by YARN for exceeding memory limits"
  - GC time is extremely high on one executor

STRATEGIES TO HANDLE DATA SKEW:

1. BROADCAST JOIN (eliminates shuffle entirely):
   - If one side is small (< broadcast threshold), broadcast it
   - No shuffle = no skew partition
   - F.broadcast(small_df) or increase broadcast threshold
   - Best for: large table skewed by key + small dimension table

2. SALT TECHNIQUE (adds randomness to break up hot keys):
   - Add a random 'salt' to the hot key to split it across partitions
   - Step 1: Add salt to the large table's join key
       df1 = df1.withColumn('salted_key',
              F.concat(F.col('customer_id'), F.lit('_'),
              F.floor(F.rand() * 10).cast('int')))
   - Step 2: Replicate the small table N times with all salt values
       salts = [str(i) for i in range(10)]
       df2 = (df2.withColumn('salt', F.explode(F.array([F.lit(s) for s in salts])))
              .withColumn('salted_key', F.concat(F.col('customer_id'), F.lit('_'), F.col('salt'))))
   - Step 3: Join on salted_key (hot key spread across 10 partitions)
   - Step 4: After join, remove the salt to get original keys back
   - Trade-off: small table is replicated N times (more memory)

3. AQE SKEW JOIN HANDLING (Spark 3.x, automatic):
   - spark.sql.adaptive.skewJoin.enabled = true
   - Spark detects skewed partitions by size at runtime
   - Automatically splits the large partition into smaller sub-partitions
   - Replicates the corresponding small-table partition
   - No code changes needed — just enable AQE

4. REPARTITION BEFORE JOIN (manual redistribution):
   - df.repartition(200, 'customer_id') redistributes data
   - Doesn't fix fundamental skew, but can help with moderate skew
   - Use a different distribution key if possible

5. SPLIT AND UNION (manual salting without code complexity):
   - Separate hot keys from cold keys
   - Join hot keys with broadcast (if small enough)
   - Join cold keys normally
   - Union the results

KEY POINT:
  Skew = one task dominates. Detect via Spark UI (task duration skew).
  Fix: broadcast (no shuffle), salt (spread hot keys), AQE (auto-split).
  AQE is the easiest fix — enable it and let Spark handle it.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q9: Data Quality Checks
# MAGIC %md
# MAGIC ## 🔄 Section 5: ETL — Data Quality, Incremental Load, Deduplication (3 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q9: Data Quality Checks in ETL [BASIC]
# MAGIC
# MAGIC **Question**: What are the most important **data quality checks** to perform in an ETL pipeline? Categorize them by type (completeness, validity, consistency, uniqueness) and give a SQL example for each.
# MAGIC
# MAGIC **Hint**: Think null checks (completeness), range checks (validity), cross-table checks (consistency), primary key checks (uniqueness).

# COMMAND ----------

# DBTITLE 1,Solution Q9
# SOLUTION Q9

"""
DATA QUALITY CHECKS IN ETL:

1. COMPLETENESS (no missing data):
   - Check: are required columns NULL?
   - SQL: SELECT COUNT(*) FROM orders WHERE customer_id IS NULL;
   - Alert if null_rate > threshold (e.g., 5%)
   - Example: order_id must NEVER be null; customer_name can be null < 1%

2. VALIDITY (values within expected range/domain):
   - Check: does the value fall within valid ranges?
   - SQL: SELECT COUNT(*) FROM orders WHERE amount < 0; -- amounts must be positive
   - SQL: SELECT COUNT(*) FROM orders WHERE order_date > CURRENT_DATE(); -- future dates?
   - Regex checks: email format, phone format, zip code
   - Enum checks: status IN ('PENDING', 'COMPLETED', 'CANCELLED')

3. UNIQUENESS (no duplicate keys):
   - Check: is the primary key truly unique?
   - SQL: SELECT order_id, COUNT(*) FROM orders GROUP BY order_id HAVING COUNT(*) > 1;
   - If duplicates found: deduplicate or quarantine
   - Critical for MERGE operations (duplicate keys cause issues)

4. CONSISTENCY (cross-table/column checks):
   - Check: do foreign keys have matching primary keys?
   - SQL: SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id
           WHERE c.customer_id IS NULL; -- orphaned foreign keys
   - Check: does sum of line items = order total?
   - SQL: SELECT order_id FROM orders o JOIN line_items l GROUP BY order_id
           HAVING SUM(l.amount) != o.total_amount;

5. FRESHNESS (is the data current?):
   - Check: when was the table last updated?
   - SQL: SELECT MAX(updated_at) FROM orders;
   - Alert if MAX(updated_at) < CURRENT_TIMESTAMP() - INTERVAL 6 HOURS

6. VOLUME (is the record count expected?):
   - Check: row count per day vs 7-day average
   - SQL: SELECT DATE(created_at), COUNT(*) FROM orders GROUP BY 1;
   - Alert if today's count < 50% of 7-day average

IMPLEMENTATION IN DATABRICKS:
  - Delta Live Tables: expectations (EXPECT ... ON ...)
  - Lakehouse Monitoring: automated monitors
  - SQL alerts: scheduled checks with email/Slack notifications
  - Custom: write metrics to a metrics table after each run

KEY POINT:
  Check completeness, validity, uniqueness, consistency, freshness, volume.
  Automate checks — don't rely on manual inspection.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q10: Incremental Load Patterns
# MAGIC %md
# MAGIC ---
# MAGIC ### Q10: Incremental Load Patterns [INTERMEDIATE]
# MAGIC
# MAGIC **Scenario**: You have a daily ETL job that loads new data from a source table into a target Delta table. Running a full reload every day is too slow and expensive.
# MAGIC
# MAGIC **Question**: What are the common **incremental load patterns** in ETL? Explain watermark-based, CDC-based, and partition-based incremental loading with pros and cons of each.
# MAGIC
# MAGIC **Hint**: Watermark = use a timestamp column to identify new rows. CDC = use a change log. Partition = overwrite only today's partition.

# COMMAND ----------

# DBTITLE 1,Solution Q10
# SOLUTION Q10

"""
INCREMENTAL LOAD = process only NEW or CHANGED data since the last run
                  instead of reloading the entire table

PATTERN 1: WATERMARK-BASED (timestamp column):
  - Use a timestamp column (updated_at, created_at) as the watermark
  - Track the last processed timestamp in a control/state table
  - Load: SELECT * FROM source WHERE updated_at > last_watermark
  - Update the watermark after successful load
  
  Pros: simple, works with any source that has a timestamp column
  Cons: misses hard deletes (rows removed from source); depends on reliable timestamps
  
  Example:
    last_watermark = spark.sql('SELECT MAX(updated_at) FROM control_table').collect()[0][0]
    new_data = spark.sql(f'SELECT * FROM source WHERE updated_at > "{last_watermark}"')
    # MERGE into target, update watermark

PATTERN 2: CDC-BASED (change data capture):
  - Source provides a change log (INSERT, UPDATE, DELETE operations)
  - Apply changes to the target using MERGE
  - Handles inserts, updates, AND deletes
  
  Pros: captures deletes, exact changes, low latency
  Cons: source must support CDC (Debezium, Oracle GoldenGate, etc.); more complex
  
  Example:
    MERGE INTO target t USING cdc_log s ON t.id = s.id
      WHEN MATCHED AND s.op = 'DELETE' THEN DELETE
      WHEN MATCHED AND s.op = 'UPDATE' THEN UPDATE *
      WHEN NOT MATCHED AND s.op = 'INSERT' THEN INSERT *

PATTERN 3: PARTITION-BASED (overwrite one partition):
  - Source is partitioned by date/hour
  - Only process the latest partition(s)
  - INSERT OVERWRITE the target partition (idempotent)
  
  Pros: simple, idempotent, no state tracking needed; good for daily batch
  Cons: re-processes entire partition (not truly incremental within a partition);
        can't handle late-arriving data for past partitions without re-running them
  
  Example:
    today = '2026-10-17'
    new_data = spark.read.parquet(f'/source/date={today}')
    (new_data.write
     .mode('overwrite')
     .option('replaceWhere', f'date = "{today}"')
     .saveAsTable('target_table'))

PATTERN 4: DELTA CDF (Change Data Feed):
  - Delta Lake CDF tracks row-level changes
  - Read only changes since a specific version
  - spark.read.format('delta').option('readChangeFeed', 'true')
         .option('startingVersion', last_version)
  
  Pros: native Delta feature, no external CDC tool needed
  Cons: only works for Delta-to-Delta; CDF must be enabled on the source table

CHOOSING A PATTERN:
  - Watermark: simple, source has a reliable timestamp column
  - CDC: need to capture deletes, source provides change log
  - Partition: daily batch, data arrives in date-partitioned folders
  - Delta CDF: both source and target are Delta tables

KEY POINT:
  Incremental = process only new/changed data. Choose based on source capabilities.
  Watermark (simple), CDC (complete), Partition (idempotent batch), CDF (Delta-native).
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q11: Deduplication
# MAGIC %md
# MAGIC ---
# MAGIC ### Q11: Deduplication Strategies [INTERMEDIATE]
# MAGIC
# MAGIC **Scenario**: Your ETL pipeline occasionally produces duplicate rows due to retries or upstream issues. You need to deduplicate while keeping the most recent version of each record.
# MAGIC
# MAGIC **Question**: What are the different **deduplication strategies** in Spark/Delta? Explain `dropDuplicates`, window-based dedup, and MERGE-based dedup with examples. When do you use each?
# MAGIC
# MAGIC **Hint**: dropDuplicates (simple), row_number + filter (keep latest), MERGE (idempotent upsert). Use watermark + event time for streaming dedup.

# COMMAND ----------

# DBTITLE 1,Solution Q11
# SOLUTION Q11
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Sample data with duplicates
dup_data = [
    (1, 'Alice', 50000, '2026-01-15 10:00'),
    (1, 'Alice', 55000, '2026-01-16 12:00'),  # duplicate id, newer salary
    (2, 'Bob',   60000, '2026-01-15 09:00'),
    (3, 'Carol', 70000, '2026-01-15 11:00'),
    (3, 'Carol', 75000, '2026-01-17 08:00'),  # duplicate id, newer salary
]

raw = spark.createDataFrame(dup_data, ['id', 'name', 'salary', 'updated_at'])

# STRATEGY 1: dropDuplicates (simple, keeps first occurrence)
# Good for: exact duplicate rows (same data in all columns)
# NOT good for: keeping the latest version when data differs
simple_dedup = raw.dropDuplicates(['id'])
print('Strategy 1: dropDuplicates (keeps first)')
display(simple_dedup.orderBy('id'))

# STRATEGY 2: Window-based dedup (keep the LATEST version by timestamp)
# Good for: same key but different values; want the most recent
w = Window.partitionBy('id').orderBy(F.col('updated_at').desc())
window_dedup = (
    raw.withColumn('rn', F.row_number().over(w))
    .filter(F.col('rn') == 1)
    .drop('rn')
)
print('Strategy 2: Window-based (keeps latest by timestamp)')
display(window_dedup.orderBy('id'))

# STRATEGY 3: MERGE-based dedup (idempotent upsert in Delta)
# Good for: production pipelines with Delta tables
# MERGE INTO target t USING source s ON t.id = s.id
# WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE *
# WHEN NOT MATCHED THEN INSERT *
# → Only updates if source is newer; no duplicates

# STRATEGY 4: Streaming dedup (with watermark)
# Good for: structured streaming with late-arriving data
# df.withWatermark('event_time', '10 minutes')
#   .dropDuplicates('id', 'event_time')
# → dedup within a 10-minute window; older duplicates are dropped

print('Strategy 3 (MERGE) and Strategy 4 (streaming watermark) shown in comments.')

# COMMAND ----------

# DBTITLE 1,Q12: Medallion Architecture
# MAGIC %md
# MAGIC ## 📊 Section 6: Data Modeling (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q12: Medallion Architecture (Bronze/Silver/Gold) [BASIC]
# MAGIC
# MAGIC **Question**: What is the **medallion architecture** (also called multi-hop architecture)? Explain the **Bronze**, **Silver**, and **Gold** layers. What happens at each layer, and what data quality level does each represent?
# MAGIC
# MAGIC **Hint**: Bronze = raw ingestion, Silver = cleaned/conformed, Gold = business-level aggregates. Also called Lakehouse pattern.

# COMMAND ----------

# DBTITLE 1,Solution Q12
# SOLUTION Q12

"""
MEDALLION ARCHITECTURE (Multi-Hop):
  A data design pattern that organizes data in progressively refined layers.
  Each layer improves data quality and adds business value.

BRONZE LAYER (Raw / Landing):
  - Stores raw, untransformed data exactly as ingested from source
  - Format: Delta tables (or Parquet/JSON/CSV as-is)
  - Schema: as-is from source (may be messy, all columns kept)
  - Quality: lowest — no validation, no cleaning
  - Purpose: preserve the original data for replay/audit
  - Writes: append-only (never overwrite, preserve history)
  - Example:
      Bronze: raw_customer_api_data (id, raw_json_response, ingested_at)

SILVER LAYER (Cleansed / Conformed):
  - Cleansed, filtered, and conformed data
  - Schema: normalized, typed (strings → dates, bad records quarantined)
  - Quality: medium — nulls handled, types corrected, duplicates removed
  - Purpose: provide a clean, trusted dataset for analysts and downstream
  - Operations: dedup, type casting, null handling, join with dimension tables
  - Example:
      Silver: customers (customer_id, name, email, phone, created_at, updated_at)

GOLD LAYER (Curated / Business-Level):
  - Business-level aggregates, KPIs, and reporting tables
  - Schema: star schema (fact + dimension tables)
  - Quality: highest — validated against business rules, aggregated
  - Purpose: power BI dashboards, ML models, executive reporting
  - Operations: aggregations, joins, window functions, business logic
  - Example:
      Gold: daily_sales_summary (date, region, total_revenue, order_count, avg_order_value)
      Gold: dim_customer, dim_product, fact_sales (star schema for BI)

FLOW: Source → Bronze (raw) → Silver (clean) → Gold (curated)

BENEFITS:
  1. Separation of concerns: each layer has a clear purpose
  2. Replay capability: re-run Silver from Bronze if logic changes
  3. Data quality improves progressively
  4. Performance: Gold queries are fast (pre-aggregated, optimized)
  5. ACID guarantees at every layer (Delta tables)

IMPLEMENTATION:
  - Bronze: Auto Loader → Delta table (append)
  - Silver: read Bronze → clean → MERGE into Silver Delta table
  - Gold: read Silver → aggregate → write Gold Delta table
  - Orchestration: Databricks Jobs or Spark Declarative Pipelines (SDP)

KEY POINT:
  Bronze = raw data (append-only). Silver = cleaned/conformed. Gold = business aggregates.
  Data quality increases at each layer. Re-runnable from any layer.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q13: Bridge Tables
# MAGIC %md
# MAGIC ---
# MAGIC ### Q13: Bridge Tables and Many-to-Many Relationships [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: What is a **bridge table** (also called a junction or associative table)? Why is it needed for many-to-many relationships in dimensional modeling? Give a concrete example (e.g., a patient visiting multiple doctors, a product belonging to multiple categories).
# MAGIC
# MAGIC **Hint**: A bridge table sits between two dimensions and resolves the many-to-many by holding the foreign keys of both. Example: fact_prescription (patient_id, doctor_id, date, medication).

# COMMAND ----------

# DBTITLE 1,Solution Q13
# SOLUTION Q13

"""
BRIDGE TABLE (Junction / Associative Table):
  - A table that resolves many-to-many relationships between two dimensions
  - Contains the foreign keys of BOTH dimensions it connects
  - May also contain fact measures (making it a fact table too)

WHY IT'S NEEDED:
  - In a star schema, fact tables connect to dimensions via FK-PK joins
  - A fact row can link to ONE value per dimension (one customer, one product)
  - But many real-world relationships are many-to-many:
    - A patient sees multiple doctors; a doctor sees multiple patients
    - A product belongs to multiple categories; a category has multiple products
    - A student takes multiple courses; a course has multiple students
  - You can't model this with a single FK in the fact table
  - Solution: a bridge table holds both FKs

EXAMPLE 1: PATIENT-DOCTOR (many-to-many):
  dim_patient: (patient_id, patient_name, dob, gender)
  dim_doctor:   (doctor_id, doctor_name, specialty)
  bridge_visit: (patient_id, doctor_id, visit_date, diagnosis, cost)
  
  - bridge_visit has FKs to BOTH dim_patient and dim_doctor
  - It also has measures (cost) → it's a fact table AND a bridge table
  - Query: "How many patients did Dr. Smith see in January?"
    SELECT COUNT(DISTINCT b.patient_id)
    FROM bridge_visit b
    JOIN dim_doctor d ON b.doctor_id = d.doctor_id
    WHERE d.doctor_name = 'Dr. Smith' AND MONTH(b.visit_date) = 1

EXAMPLE 2: PRODUCT-CATEGORY (many-to-many):
  dim_product:   (product_id, product_name, price)
  dim_category:  (category_id, category_name, parent_category_id)
  bridge_product_category: (product_id, category_id, is_primary)
  
  - A product can be in 'Electronics' AND 'Gift Ideas' AND 'Sale Items'
  - The is_primary flag marks the main category for reporting
  - Query: "Find all products in the Electronics category"
    SELECT p.product_name
    FROM dim_product p
    JOIN bridge_product_category b ON p.product_id = b.product_id
    JOIN dim_category c ON b.category_id = c.category_id
    WHERE c.category_name = 'Electronics'

DESIGN CONSIDERATIONS:
  1. Bridge tables can cause double-counting in aggregations
     → Use DISTINCT or set is_primary to avoid counting a product twice
  2. Bridge tables may have their own measures (making them fact tables)
  3. For hierarchy resolution (category → subcategory), use a bridge
     with parent-child relationships
  4. The bridge table grain is the intersection of the two dimensions

KEY POINT:
  Bridge table = junction table for many-to-many relationships.
  Contains FKs to both dimensions. May have measures (fact + bridge).
  Watch out for double-counting — use is_primary or DISTINCT.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q14: Materialized vs Dynamic Tables
# MAGIC %md
# MAGIC ## ❄️ Section 7: Snowflake (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q14: Materialized vs Dynamic Tables [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: What is the difference between a **Materialized View** and a **Dynamic Table** in Snowflake? How does each refresh? When would you choose one over the other?
# MAGIC
# MAGIC **Hint**: Materialized View = Snowflake auto-refreshes incrementally, query-speed optimization. Dynamic Table = user-defined refresh schedule, pipeline/ELT use case, can be downstream of other dynamic tables.

# COMMAND ----------

# DBTITLE 1,Solution Q14
# SOLUTION Q14

"""
SNOWFLAKE — MATERIALIZED VIEW vs DYNAMIC TABLE:

MATERIALIZED VIEW:
  - A pre-computed result of a query, stored for faster reads
  - Snowflake maintains it AUTOMATICALLY — no manual refresh needed
  - Refresh type: INCREMENTAL (only changes are recomputed)
  - Query rewrites: Snowflake automatically routes queries to use the MV
    instead of the base table when possible
  - Syntax:
      CREATE MATERIALIZED VIEW mv_daily_sales AS
      SELECT date, region, SUM(revenue) FROM raw_sales GROUP BY 1, 2;
  - Limitations:
    * Cannot use non-deterministic functions (CURRENT_DATE, RANDOM)
    * Limited join types
    * Cannot reference other materialized views
    * Not suitable for complex multi-step ELT pipelines

DYNAMIC TABLE:
  - A new Snowflake feature (2023) for declarative ELT pipelines
  - User defines a REFRESH SCHEDULE (e.g., every 1 hour)
  - The target lag: MAX DATA FRESHNESS (e.g., '1 hour')
  - Can reference OTHER dynamic tables → multi-step ELT pipeline
  - Syntax:
      CREATE OR REPLACE DYNAMIC TABLE dt_daily_sales TARGET_LAG = '1 hour'
      WAREHOUSE = 'my_wh' AS
      SELECT date, region, SUM(revenue) FROM raw_sales GROUP BY 1, 2;
  - Refresh: full recomputation of the query at each scheduled interval
  - Supports complex joins, CTEs, non-deterministic functions
  - Snowflake tracks dependencies and refreshes in topological order

COMPARISON:

  | Feature            | Materialized View      | Dynamic Table              |
  |-------------------|------------------------|----------------------------|
  | Purpose            | Query speed-up        | ELT pipeline / data product  |
  | Refresh            | Auto (incremental)    | Scheduled (full or incremental) |
  | Refresh trigger    | Snowflake manages     | User-defined schedule + lag  |
  | Chaining           | No (can't reference MVs) | Yes (DT → DT → DT)      |
  | Non-deterministic  | Not allowed           | Allowed                     |
  | Complex joins      | Limited               | Full support                |
  | Warehouse needed   | No (uses server-side) | Yes (user specifies)       |
  | Best for           | Read-heavy dashboards  | Multi-step ELT pipelines   |

WHEN TO USE MATERIALIZED VIEW:
  ✓ Simple aggregation for dashboard acceleration
  ✓ Read-heavy workload with infrequent source changes
  ✓ You want automatic incremental refresh (no management)
  ✓ Simple single-table or two-table joins

WHEN TO USE DYNAMIC TABLE:
  ✓ Multi-step ELT pipeline (bronze → silver → gold)
  ✓ Complex transformations with CTEs and multiple joins
  ✓ Need a specific refresh cadence (e.g., hourly, daily)
  ✓ Need to chain transformations (DT referencing another DT)

KEY POINT:
  MV = auto-refresh, query acceleration, simple aggregations.
  DT = user-scheduled, ELT pipeline, complex transforms, can chain.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q15: Data Sharing
# MAGIC %md
# MAGIC ---
# MAGIC ### Q15: Data Sharing in Snowflake [BASIC]
# MAGIC
# MAGIC **Question**: What is **Snowflake Data Sharing**? How does it work without copying data? What is a **Secure Share**, a **Reader Account**, and how does sharing differ from copying or ETL?
# MAGIC
# MAGIC **Hint**: Snowflake shares data by reference (no copy). Provider creates a share, grants to consumer. Reader accounts are for consumers without a Snowflake account.

# COMMAND ----------

# DBTITLE 1,Solution Q15
# SOLUTION Q15

"""
SNOWFLAKE DATA SHARING:
  - Share data with external organizations WITHOUT copying it
  - The provider and consumer both see the SAME micro-partitions
  - No data movement = zero storage cost for the consumer, instant access

HOW IT WORKS (NO COPY):
  - Provider creates a SHARE object containing tables, views, schemas
  - Provider grants the share to a consumer account (by account ID)
  - Consumer creates a DATABASE FROM the share:
      CREATE DATABASE shared_sales FROM SHARE provider_account.sales_share;
  - Consumer queries the shared database normally
  - All queries run on the CONSUMER's warehouse (consumer pays compute)
  - Storage is paid by the PROVIDER (data lives in provider's account)
  - Changes in the provider's data are INSTANTLY visible to the consumer
    (no sync, no ETL, no lag)

SECURE SHARE:
  - A share where the provider can restrict what the consumer sees:
    * Secure Views: filter rows/columns based on the consumer
    * Secure UDFs: mask sensitive data
    * Row access policies: consumer sees only their own data
  - Example:
      CREATE SECURE VIEW customer_orders AS
      SELECT order_id, total_amount
      FROM orders
      WHERE customer_id = CURRENT_REGION();  -- consumer-specific filter

READER ACCOUNT:
  - For consumers who DON'T have their own Snowflake account
  - The provider creates a reader account on their behalf
  - Reader accounts are limited to SELECT queries (read-only)
  - Provider pays for the reader's compute (can set resource limits)
  - Use when: sharing with partners, customers, or vendors without Snowflake

DATA SHARING vs ETL / COPYING:

  | Approach      | Data Sharing            | ETL / Copy                |
  |---------------|------------------------|---------------------------|
  | Data movement | None (shared by ref)   | Full copy (expensive)      |
  | Freshness     | Real-time (instant)    | Batch (lag = ETL schedule) |
  | Storage cost  | Provider only          | Both sides pay storage     |
  | Setup         | Grant + create database | Full pipeline to build     |
  | Best for      | Snowflake-to-Snowflake  | Cross-platform sharing    |

USE CASES:
  1. Data marketplace: share datasets with customers (free or paid)
  2. Internal: share between business units in different accounts
n  3. Partner integration: share with vendors/suppliers
  4. Regulatory: share audit data with regulators (secure, read-only)

LIMITATIONS:
  - Snowflake-to-Snowflake only (for native sharing)
  - Consumer can't modify shared data (read-only)
  - Provider controls schema changes (consumer can't ALTER shared tables)

KEY POINT:
  Sharing = zero-copy, real-time, provider pays storage, consumer pays compute.
  Reader accounts for consumers without Snowflake. Secure views for row/column filtering.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q16: Job Retries & Repair Runs
# MAGIC %md
# MAGIC ## 🛠️ Section 8: Monitoring, Logging & Orchestration (3 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q16: Job Retries and Repair Runs [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: How do **retries** work in Databricks Jobs? What is a **Repair Run** and how is it different from a full re-run? Explain the retry policy settings and when to use each.
# MAGIC
# MAGIC **Hint**: Retries = re-run failed tasks automatically. Repair Run = re-run only failed/skipped tasks from a previous run, not the entire job. Configurable per-task.

# COMMAND ----------

# DBTITLE 1,Solution Q16
# SOLUTION Q16

"""
DATABRICKS JOBS — RETRIES:
  - Each task in a job can be configured with a retry policy
  - If a task fails, Databricks automatically retries it N times
  - After all retries are exhausted, the task is marked FAILED

RETRY SETTINGS (per task):
  - max_retries: number of retry attempts (default: 0)
    Example: max_retries = 3 → try up to 4 times (1 initial + 3 retries)
  - min_retry_interval_millis: minimum wait between retries
  - retry_on_timeout: whether to retry if the task times out (default: false)
  
  When to set retries:
    ✓ Transient failures: S3 throttling, network blips, OOM from skew
    ✗ Persistent failures: code bug, schema mismatch, missing file
    → Retrying a code bug wastes compute — the same error will repeat

REPAIR RUN (re-run only failed tasks):
  - When a job fails, you can REPAIR the run instead of re-running everything
  - Repair Run re-executes ONLY the failed and downstream-skipped tasks
  - Successfully completed tasks are NOT re-run (save compute + time)
  - Available from: Job run page → Repair (or API: jobs/run-now with repair parameters)
  
  How it works:
    Run 1: Task A (✓) → Task B (✓) → Task C (✗ FAILED) → Task D (SKIPPED)
    Repair Run: only re-runs Task C and Task D
    Task A and B are NOT re-run (their results are reused)
  
  API:
    POST /api/2.1/jobs/run-now
    {
      "job_id": 12345,
      "rerun_all_failed_tasks": true,
      "rerun_dependent_tasks": true
    }

REPAIR vs FULL RE-RUN:

  | Aspect         | Repair Run              | Full Re-Run              |
  |----------------|-------------------------|--------------------------|
  | Scope          | Only failed + skipped    | All tasks from scratch    |
  | Cost           | Low (skip completed)    | High (redo everything)    |
  | Time           | Fast                    | Slow (full pipeline)     |
  | Use when       | Few tasks failed        | Major change, full retest |
  | Idempotency    | Still needed            | Still needed             |

WHEN TO USE RETRIES vs REPAIR:
  - Retries (max_retries): set on tasks likely to have transient failures
    → automatic, no manual intervention
  - Repair Run: manual action after a run fails and root cause is fixed
    → saves time by not re-running successful tasks

BEST PRACTICES:
  1. Set max_retries = 2-3 for tasks that may hit transient failures
  2. Set retry_on_timeout = true for long-running ETL tasks
  3. Use Repair Run when only a few tasks failed (not a code bug)
  4. For code bugs: fix the code first, then do a full re-run
  5. Always make tasks idempotent so retries don't produce duplicates

KEY POINT:
  Retries = automatic re-attempt of failed tasks (transient errors).
  Repair Run = re-run only failed/skipped tasks from a previous run (saves compute).
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q17: Spark UI Analysis
# MAGIC %md
# MAGIC ---
# MAGIC ### Q17: Spark UI — Stage Analysis [BASIC]
# MAGIC
# MAGIC **Question**: How do you use the **Spark UI** to diagnose performance issues? Walk through the key tabs (Stages, Executors, SQL/DataFrame) and explain what metrics to look for when a job is slow.
# MAGIC
# MAGIC **Hint**: Stages tab → task duration skew, shuffle spill. Executors tab → GC time, memory. SQL tab → query plan, scan size, join type.

# COMMAND ----------

# DBTITLE 1,Solution Q17
# SOLUTION Q17

"""
SPARK UI — KEY TABS AND WHAT TO LOOK FOR:

1. STAGES TAB (most important for performance):
   - Shows all stages in the job with duration, tasks, shuffle data
   - Key metrics per stage:
     * Duration: how long the stage took (compare with expected)
     * Tasks: number of tasks, completed vs failed
     * Shuffle read/write: data movement between stages
     * Spill (memory/disk): if > 0, the task ran out of memory and spilled
   - Click a stage → see per-task details:
     * Duration column: look for SKEW (one task taking 10x longer)
     * Shuffle spill: if one task spills 50 GB while others spill 100 MB → skew
     * GC time: if > 20% of task time → memory pressure
   - Red flags:
     * One task takes 5 min while 199 tasks take 10 sec → DATA SKEW
     * High shuffle write + high shuffle read → expensive shuffle (consider broadcast)
     * Spill to disk → need more memory or fewer partitions

2. EXECUTORS TAB:
   - Shows per-executor metrics (cores, memory, GC time, tasks)
   - Key metrics:
     * Task count: even distribution across executors?
     * GC time: if one executor has 90% GC time → memory leak or skew
     * Used memory: if maxed out → increase executor memory or reduce partition size
     * Shuffle read/write per executor: uneven → skewed partition
   - Red flags:
     * Dead/excluded executors → node failures
     * One executor doing 90% of work → skewed data or bad partitioning

3. SQL / DATAFRAME TAB (Spark 3.x):
  - Shows the executed query plan with actual metrics
  - Key info:
     * Scan: how many rows/bytes were read from each source
     * Filter: selectivity (how many rows were filtered out)
     * Join: join type (BroadcastHash vs SortMerge), build side size
     * Exchange (shuffle): number of partitions, shuffle bytes
     * Aggregate: hash vs sort-based aggregation
  - Red flags:
     * SortMergeJoin when one side is small → switch to BroadcastJoin
     * Reading 1 TB when filter should reduce to 10 GB → missing partition pruning
     * Filter after Join instead of before → pushdown not working

4. STORAGE TAB (if caching is used):
  - Shows cached DataFrames and their memory usage
  - Fraction cached: if < 100%, some partitions are spilled to disk
  - Use this to verify cache hit ratio

5. ENVIRONMENT TAB:
  - Shows Spark config, classpath, system properties
  - Useful for debugging: AQE enabled? Broadcast threshold set? Shuffle partitions?

DEBUGGING WORKFLOW:
  1. SQL tab → find the slow query → click to see the plan
  2. Identify the slowest node in the plan (longest duration)
  3. Stages tab → click the corresponding stage
  4. Look at task-level metrics: skew, spill, GC
  5. Based on findings:
     - Skew → salting, broadcast, or AQE skew handling
     - Spill → more memory, fewer partitions, or larger executors
     - Slow scan → partition pruning, column pruning, ZORDER
     - SortMerge → switch to broadcast if one side is small

KEY POINT:
  Stages → task-level skew/spill/GC. Executors → resource usage. SQL → plan-level diagnosis.
  Always look at per-task metrics to find the bottleneck (not just averages).
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q18: Metrics Table for Monitoring
# MAGIC %md
# MAGIC ---
# MAGIC ### Q18: Building a Metrics Table for ETL Monitoring [INTERMEDIATE]
# MAGIC
# MAGIC **Scenario**: You run 20 ETL pipelines daily. You want a single dashboard showing row counts, null rates, max timestamps, and anomaly flags for every table after each run.
# MAGIC
# MAGIC **Question**: Design a **metrics table** schema and a Python/SQL pattern that writes metrics after each ETL run. How do you detect anomalies (sudden volume drop, freshness breach)? Write the SQL for the metrics table and a sample insert.
# MAGIC
# MAGIC **Hint**: Create a metrics table (run_date, table_name, row_count, null_rate, max_updated_at, anomaly_flag). Write metrics after each run. Compare today vs 7-day average for anomaly detection.

# COMMAND ----------

# DBTITLE 1,Solution Q18
# SOLUTION Q18
from pyspark.sql import functions as F

# === METRICS TABLE SCHEMA ===
# CREATE TABLE IF NOT EXISTS monitoring.etl_metrics (
#   run_date        DATE,
#   table_name       STRING,
#   row_count       BIGINT,
#   null_rate       DOUBLE,
#   max_updated_at  TIMESTAMP,
#   anomaly_flag    BOOLEAN,
#   anomaly_reason   STRING,
#   pipeline_run_id STRING
# )
# USING DELTA
# PARTITIONED BY (run_date);

# === SAMPLE: Collect metrics for a table ===
# Simulate a fact table
import datetime
now = datetime.datetime.now()

data = [
    (1, 100, now - datetime.timedelta(hours=1)),
    (2, 200, now - datetime.timedelta(hours=2)),
    (3, None, now - datetime.timedelta(hours=3)),
    (4, 150, now - datetime.timedelta(hours=1)),
]

fact_df = spark.createDataFrame(data, ['id', 'amount', 'updated_at'])

# Step 1: Compute current metrics
row_count = fact_df.count()
null_count = fact_df.filter(F.col('amount').isNull()).count()
null_rate = (null_count / row_count) if row_count > 0 else 0.0
max_updated = fact_df.agg(F.max('updated_at')).collect()[0][0]

print(f"=== METRICS FOR fact_orders ===")
print(f"Row count:    {row_count}")
print(f"Null rate:    {null_rate:.2%}")
print(f"Max updated:  {max_updated}")

# Step 2: In production, fetch 7-day average from metrics table for comparison
# prev_metrics = spark.sql('''
#   SELECT AVG(row_count) AS avg_7d_count
#   FROM monitoring.etl_metrics
#   WHERE table_name = 'fact_orders'
#     AND run_date >= CURRENT_DATE() - INTERVAL 7 DAYS
#     AND run_date < CURRENT_DATE()
# ''').collect()[0]
# avg_7d = prev_metrics['avg_7d_count'] or row_count
avg_7d = row_count  # Demo: assume same as today

# Step 3: Anomaly detection
anomaly_flag = False
anomaly_reason = ''

if row_count < avg_7d * 0.5:
    anomaly_flag = True
    anomaly_reason = f'Volume drop: {row_count} < 50% of 7-day avg ({avg_7d})'

hours_since = (now - max_updated).total_seconds() / 3600 if max_updated else 999
if hours_since > 6:
    anomaly_flag = True
    anomaly_reason += f' Freshness breach: {hours_since:.1f}h since last update'

print(f"Anomaly flag: {anomaly_flag}")
if anomaly_reason:
    print(f"Anomaly:     {anomaly_reason.strip()}")

# Step 4: Insert into metrics table
# metrics_row = spark.createDataFrame([(
#     datetime.date.today(), 'fact_orders', row_count,
#     null_rate, max_updated, anomaly_flag, anomaly_reason, 'RUN-2026-10-17-001'
# )], monitoring_schema)
#
# metrics_row.write
#     .mode('append')
#     .format('delta')
#     .saveAsTable('monitoring.etl_metrics')

print("\n=== PRODUCTION SQL (metrics table) ===")
print("""
CREATE TABLE IF NOT EXISTS monitoring.etl_metrics (
  run_date        DATE,
  table_name       STRING,
  row_count       BIGINT,
  null_rate       DOUBLE,
  max_updated_at  TIMESTAMP,
  anomaly_flag    BOOLEAN,
  anomaly_reason   STRING,
  pipeline_run_id STRING
) USING DELTA
PARTITIONED BY (run_date);

-- After each ETL run, insert metrics:
INSERT INTO monitoring.etl_metrics
SELECT
  CURRENT_DATE()              AS run_date,
  'fact_orders'               AS table_name,
  COUNT(*)                    AS row_count,
  AVG(CASE WHEN amount IS NULL THEN 1.0 ELSE 0.0 END) AS null_rate,
  MAX(updated_at)             AS max_updated_at,
  -- Anomaly: volume < 50% of 7-day average OR stale > 6h
  CASE
    WHEN COUNT(*) < 0.5 * (
      SELECT AVG(row_count) FROM monitoring.etl_metrics
      WHERE table_name = 'fact_orders'
        AND run_date >= CURRENT_DATE() - INTERVAL 7 DAYS
        AND run_date < CURRENT_DATE()
    )
    OR MAX(updated_at) < CURRENT_TIMESTAMP() - INTERVAL 6 HOURS
    THEN true ELSE false
  END AS anomaly_flag,
  CASE
    WHEN COUNT(*) < 0.5 * (
      SELECT AVG(row_count) FROM monitoring.etl_metrics
      WHERE table_name = 'fact_orders'
        AND run_date >= CURRENT_DATE() - INTERVAL 7 DAYS
        AND run_date < CURRENT_DATE()
    )
    THEN 'Volume drop below 50% of 7-day average'
    ELSE ''
  END AS anomaly_reason,
  'RUN-' || CURRENT_DATE() || '-001' AS pipeline_run_id
FROM fact_orders;
""")

# COMMAND ----------

# DBTITLE 1,Day 5 Complete
# MAGIC %md
# MAGIC ---
# MAGIC ## ✅ Day 5 Complete!
# MAGIC
# MAGIC **18 questions covered across 8 categories.**
# MAGIC
# MAGIC ### Score Yourself:
# MAGIC | Category | Questions | Your Score |
# MAGIC |----------|-----------|------------|
# MAGIC | SQL Advanced | 2 | / 2 |
# MAGIC | Python | 2 | / 2 |
# MAGIC | PySpark | 2 | / 2 |
# MAGIC | Spark Optimization | 2 | / 2 |
# MAGIC | ETL | 3 | / 3 |
# MAGIC | Data Modeling | 2 | / 2 |
# MAGIC | Snowflake | 2 | / 2 |
# MAGIC | Monitoring, Logging & Orchestration | 3 | / 3 |
# MAGIC
# MAGIC **Total: / 18**
# MAGIC
# MAGIC ---
# MAGIC Next day: `day_06` notebook with fresh questions! 🚀

# COMMAND ----------

