# Databricks notebook source
# DBTITLE 1,Day 2 — Mock Interview Practice
# MAGIC %md
# MAGIC # 📅 Day 2 — Mock Interview Practice
# MAGIC
# MAGIC **Date**: Oct 14, 2026
# MAGIC
# MAGIC **Topics Covered**:
# MAGIC | # | Category | Questions |
# MAGIC |---|----------|----------|
# MAGIC | 1 | SQL Advanced | 2 |
# MAGIC | 2 | Python (Loop/Function/List/Dict) | 2 |
# MAGIC | 3 | PySpark Coding | 2 |
# MAGIC | 4 | Spark Optimization & Deep Spark | 2 |
# MAGIC | 5 | ETL (Failures, Duplicates, Bad Records) | 2 |
# MAGIC | 6 | Data Modeling | 2 |
# MAGIC | 7 | Snowflake | 2 |
# MAGIC | 8 | Monitoring, Logging & Orchestration | 3 |
# MAGIC
# MAGIC **Total**: 17 questions
# MAGIC
# MAGIC **Difficulty**: BASIC → INTERMEDIATE (Week 1)
# MAGIC
# MAGIC ---
# MAGIC **Instructions**: Read the question, try to solve it yourself first, then check the solution cell below.

# COMMAND ----------

# DBTITLE 1,Q1: More Than Manager
# MAGIC %md
# MAGIC ## 🔷 Section 1: SQL Advanced (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q1: Employees Earning More Than Their Manager
# MAGIC
# MAGIC **Table**: `emp (emp_id, emp_name, salary, manager_id)`
# MAGIC
# MAGIC **Question**: Write a SQL query to find all employees who earn **more than their manager**. Return `emp_name, salary, manager_name, manager_salary`.
# MAGIC
# MAGIC **Hint**: Classic **self-join** problem. The CEO (no manager) should be excluded automatically.

# COMMAND ----------

# DBTITLE 1,Solution Q1
# MAGIC %sql
# MAGIC -- SOLUTION Q1
# MAGIC -- Sample data (temp view so the solution is runnable)
# MAGIC CREATE OR REPLACE TEMP VIEW emp AS
# MAGIC SELECT * FROM VALUES
# MAGIC   (1, 'Amit',   90000, NULL),
# MAGIC   (2, 'Bhavna', 80000, 1),
# MAGIC   (3, 'Chirag', 95000, 1),
# MAGIC   (4, 'Divya',  70000, 2),
# MAGIC   (5, 'Esha',   85000, 2),
# MAGIC   (6, 'Farhan', 60000, 3)
# MAGIC AS emp(emp_id, emp_name, salary, manager_id);
# MAGIC
# MAGIC -- Self-join: join emp to itself on manager_id
# MAGIC SELECT
# MAGIC   e.emp_name,
# MAGIC   e.salary,
# MAGIC   m.emp_name AS manager_name,
# MAGIC   m.salary   AS manager_salary
# MAGIC FROM emp e
# MAGIC JOIN emp m
# MAGIC   ON e.manager_id = m.emp_id      -- CEO has NULL manager_id → excluded
# MAGIC WHERE e.salary > m.salary
# MAGIC ORDER BY e.salary DESC;

# COMMAND ----------

# DBTITLE 1,Q2: MoM Growth
# MAGIC %md
# MAGIC ---
# MAGIC ### Q2: Month-over-Month Revenue Growth
# MAGIC
# MAGIC **Table**: `monthly_sales (sale_month, revenue)`
# MAGIC
# MAGIC **Question**: Write a SQL query to show each month's revenue, the previous month's revenue, and the **percentage growth** vs the previous month (rounded to 2 decimals).
# MAGIC
# MAGIC **Hint**: Use the `LAG()` window function.

# COMMAND ----------

# DBTITLE 1,Solution Q2
# MAGIC %sql
# MAGIC -- SOLUTION Q2
# MAGIC CREATE OR REPLACE TEMP VIEW monthly_sales AS
# MAGIC SELECT * FROM VALUES
# MAGIC   ('2026-01-01', 100000),
# MAGIC   ('2026-02-01', 120000),
# MAGIC   ('2026-03-01', 115000),
# MAGIC   ('2026-04-01', 150000),
# MAGIC   ('2026-05-01', 145000)
# MAGIC AS monthly_sales(sale_month, revenue);
# MAGIC
# MAGIC SELECT
# MAGIC   sale_month,
# MAGIC   revenue,
# MAGIC   LAG(revenue) OVER (ORDER BY sale_month) AS prev_month_revenue,
# MAGIC   ROUND(
# MAGIC     (revenue - LAG(revenue) OVER (ORDER BY sale_month)) * 100.0
# MAGIC     / LAG(revenue) OVER (ORDER BY sale_month)
# MAGIC   , 2) AS growth_pct
# MAGIC FROM monthly_sales
# MAGIC ORDER BY sale_month;

# COMMAND ----------

# DBTITLE 1,Q3: First Non-Repeating Char
# MAGIC %md
# MAGIC ## 🐍 Section 2: Python (Loop / Function / List / Dict) (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q3: First Non-Repeating Character
# MAGIC
# MAGIC **Question**: Write a Python function `first_unique_char(s)` that returns the **first non-repeating character** in a string, or `None` if every character repeats. Use a **dictionary** for counting.
# MAGIC
# MAGIC **Example**: `first_unique_char("swiss")` → `"w"` | `first_unique_char("aabb")` → `None`

# COMMAND ----------

# DBTITLE 1,Solution Q3
# SOLUTION Q3
def first_unique_char(s):
    """Return the first non-repeating character, or None."""
    # Pass 1: count occurrences using a dict
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1

    # Pass 2: find first char with count == 1
    for ch in s:
        if counts[ch] == 1:
            return ch
    return None

# Test
print(first_unique_char("swiss"))     # w
print(first_unique_char("aabb"))      # None
print(first_unique_char("leetcode"))   # l

# COMMAND ----------

# DBTITLE 1,Q4: Flatten Nested List
# MAGIC %md
# MAGIC ---
# MAGIC ### Q4: Flatten a Nested List
# MAGIC
# MAGIC **Question**: Write a Python function `flatten(nested)` that flattens an **arbitrarily nested list** of lists into a flat list, using **recursion inside a loop**.
# MAGIC
# MAGIC **Example**: `flatten([1, [2, [3, [4]], 5], 6])` → `[1, 2, 3, 4, 5, 6]`

# COMMAND ----------

# DBTITLE 1,Solution Q4
# SOLUTION Q4
def flatten(nested):
    """Flatten an arbitrarily nested list into a flat list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            # Recurse: extend with the flattened sub-list
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Test
print(flatten([1, [2, [3, [4]], 5], 6]))       # [1, 2, 3, 4, 5, 6]
print(flatten([[1, 2], [3, [4, [5, [6]]]]]))    # [1, 2, 3, 4, 5, 6]
print(flatten([]))                              # []

# COMMAND ----------

# DBTITLE 1,Q5: Dedup Keep Latest
# MAGIC %md
# MAGIC ## ⚡ Section 3: PySpark Coding (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q5: Deduplicate — Keep Only the Latest Record
# MAGIC
# MAGIC **DataFrame**: `orders (order_id, customer_id, status, updated_at)`
# MAGIC
# MAGIC **Question**: The orders table receives multiple updates per order. Using PySpark, keep only the **latest record per `order_id`** (max `updated_at`) and drop the rest.
# MAGIC
# MAGIC **Hint**: `ROW_NUMBER()` over a window ordered by `updated_at DESC`, then filter `rn = 1`. Also know the `dropDuplicates` shortcut.

# COMMAND ----------

# DBTITLE 1,Solution Q5
# SOLUTION Q5
from pyspark.sql import functions as F
from pyspark.sql.window import Window

orders_data = [
    (1, 101, "PLACED",    "2026-01-01 10:00:00"),
    (1, 101, "SHIPPED",   "2026-01-02 10:00:00"),
    (1, 101, "DELIVERED", "2026-01-03 10:00:00"),
    (2, 102, "PLACED",    "2026-01-01 11:00:00"),
    (2, 102, "CANCELLED", "2026-01-01 12:30:00"),
    (3, 103, "PLACED",    "2026-01-02 09:00:00"),
]

orders = spark.createDataFrame(orders_data, ["order_id", "customer_id", "status", "updated_at"])
orders = orders.withColumn("updated_at", F.to_timestamp("updated_at"))

# Approach 1: Window function — full control over the ordering column
w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
latest = (
    orders
    .withColumn("rn", F.row_number().over(w))
    .filter(F.col("rn") == 1)
    .drop("rn")
)

# Approach 2: dropDuplicates — keeps the FIRST row per key, so sort first
# latest = orders.orderBy(F.col("updated_at").desc()).dropDuplicates(["order_id"])

display(latest.orderBy("order_id"))

# COMMAND ----------

# DBTITLE 1,Q6: Pct Change with LAG
# MAGIC %md
# MAGIC ---
# MAGIC ### Q6: Percentage Change vs Previous Row (LAG)
# MAGIC
# MAGIC **DataFrame**: `daily_sales (sale_date, category, revenue)`
# MAGIC
# MAGIC **Question**: Using PySpark, compute each category's **daily revenue % change vs the previous day**. Use `F.lag()` over a window partitioned by category.
# MAGIC
# MAGIC **Expected Output**: `sale_date, category, revenue, prev_revenue, pct_change`

# COMMAND ----------

# DBTITLE 1,Solution Q6
# SOLUTION Q6
from pyspark.sql import functions as F
from pyspark.sql.window import Window

daily_data = [
    ("2026-01-01", "Electronics", 1000),
    ("2026-01-02", "Electronics", 1500),
    ("2026-01-03", "Electronics", 1200),
    ("2026-01-01", "Clothing",    500),
    ("2026-01-02", "Clothing",    800),
    ("2026-01-03", "Clothing",    400),
]

daily_sales = spark.createDataFrame(daily_data, ["sale_date", "category", "revenue"])

w = Window.partitionBy("category").orderBy("sale_date")

result = (
    daily_sales
    .withColumn("prev_revenue", F.lag("revenue").over(w))
    .withColumn(
        "pct_change",
        F.round(
            (F.col("revenue") - F.col("prev_revenue")) * 100.0 / F.col("prev_revenue"),
            2,
        ),
    )
    .orderBy("category", "sale_date")
)

display(result)

# COMMAND ----------

# DBTITLE 1,Q7: repartition vs coalesce
# MAGIC %md
# MAGIC ## 🔥 Section 4: Spark Optimization & Deep Spark (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q7: repartition() vs coalesce()
# MAGIC
# MAGIC **Question**: Explain the difference between `repartition()` and `coalesce()`. Which one causes a **full shuffle**? Which one should you use when **increasing parallelism**, and which when **writing a small result table**?
# MAGIC
# MAGIC **Follow-up**: Why can `coalesce()` make an upstream computation slower?

# COMMAND ----------

# DBTITLE 1,Solution Q7
# SOLUTION Q7

"""
REPARTITION():
  - Can INCREASE or DECREASE the number of partitions
  - Performs a FULL SHUFFLE of data across the cluster
  - Data is redistributed evenly -> balanced partitions
  - Expensive (network + disk I/O) but fixes skewed partitions
  - Use when: increasing parallelism, or partitioning by a column
      df.repartition(200)
      df.repartition(100, "customer_id")   # hash partition by column

COALESCE():
  - Can only DECREASE the number of partitions
  - NO full shuffle — existing partitions are merged on the same executors
  - Much cheaper than repartition
  - Partitions may end up unbalanced (some bigger than others)
  - Use when: cutting tiny output files after a filter
      df.filter(...).coalesce(4).write.format("delta").save(path)

FOLLOW-UP: Why can coalesce() make upstream slower?
  - coalesce() propagates UPSTREAM: going 200 -> 4 means only 4 tasks
    execute the ENTIRE pipeline (filters, joins, aggregations)
  - Parallelism of the whole stage drops to 4 -> stragglers
  - Fix: repartition BEFORE the heavy computation, coalesce only at the end

RULE OF THUMB:
  - Tune parallelism (increase / rebalance partitions) -> repartition()
  - Reduce small output files (decrease partitions)   -> coalesce()
"""

print("See comments for the full explanation.")
print("(Tip: see partition counts in the Spark UI's 'Exchange' operator, or run")
print(" df.groupBy(F.spark_partition_id()).count() on a classic cluster.)")

# COMMAND ----------

# DBTITLE 1,Q8: cache vs persist
# MAGIC %md
# MAGIC ---
# MAGIC ### Q8: cache() vs persist() — When to Cache?
# MAGIC
# MAGIC **Question**: What is the difference between `cache()` and `persist()` in Spark? List the storage levels. When should you cache a DataFrame, and which mistake causes "my cache did nothing"?
# MAGIC
# MAGIC **Follow-up**: You cached a 5 GB DataFrame and executors start failing with OOM. What do you do?

# COMMAND ----------

# DBTITLE 1,Solution Q8
# SOLUTION Q8

"""
CACHE():
  - Shorthand for persist() with the DEFAULT storage level
  - Default for DataFrames = MEMORY_AND_DISK (Spark 3.x)
  - LAZY: nothing is stored until the first ACTION runs

PERSIST(StorageLevel) — explicit level selection:
  MEMORY_ONLY          -> JVM heap; partitions that don't fit are RECOMPUTED
  MEMORY_ONLY_SER      -> serialized: more compact, CPU cost to deserialize
  MEMORY_AND_DISK      -> spill to disk instead of recomputing
  MEMORY_AND_DISK_SER  -> serialized + disk spill (safe for big DataFrames)
  DISK_ONLY            -> disk only
  OFF_HEAP             -> off-heap memory, avoids GC pressure

WHEN TO CACHE:
  - DataFrame reused MULTIPLE times (several actions / joins reuse it)
  - Expensive upstream (joins, aggregations, ML feature prep)
  - Iterative algorithms (ML training loops)

WHEN NOT TO CACHE:
  - Used only once -> caching adds overhead for no gain
  - Tiny DataFrame -> recompute is cheaper than storing

COMMON MISTAKE ("cache did nothing"):
  1. Calling cache() without an action -> still lazy, nothing stored yet
     Correct pattern:  df.cache(); df.count()   # materialize now
  2. Never calling unpersist() -> memory held until the session ends
  3. Caching the full wide table when only 2 columns are reused

FOLLOW-UP (OOM after caching 5 GB):
  1. Switch to MEMORY_AND_DISK_SER (or DISK_ONLY)
  2. Select only needed columns BEFORE caching
  3. Unpersist as soon as reuse is over
  4. Repartition to shrink per-partition size
"""

# NOTE: On Databricks SERVERLESS compute, df.cache() raises
# NOT_SUPPORTED_WITH_SERVERLESS (PERSIST TABLE is not supported there).
# Run the cache / persist / unpersist pattern on a classic cluster:

#   df.cache()
#   df.count()          # materialize the cache
#   ... reuse df across multiple actions ...
#   df.unpersist()      # release the memory

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q9: Duplicate Records
# MAGIC %md
# MAGIC ## 🔄 Section 5: ETL (Failures, Duplicates, Bad Records) (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q9: Handling Duplicate Records in a Batch ETL
# MAGIC
# MAGIC **Scenario**: Your nightly batch ingests order files into a Delta table. One night the job **re-ran after a partial failure** and some files were loaded twice. Business complains about duplicate orders.
# MAGIC
# MAGIC **Question**: How do you (a) **prevent** duplicates from being written, and (b) **clean** the existing duplicates? Explain idempotency.

# COMMAND ----------

# DBTITLE 1,Solution Q9
# SOLUTION Q9

"""
PREVENTION — make the write IDEMPOTENT (re-running produces the same result):

  1. MERGE instead of APPEND (Delta Lake):
       MERGE INTO orders AS t
       USING new_orders AS s
         ON t.order_id = s.order_id
       WHEN MATCHED THEN UPDATE SET *
       WHEN NOT MATCHED THEN INSERT
     -> Re-loading the same file is safe: rows are upserted, never duplicated.

  2. left_anti join before append:
       existing_ids = spark.read.format("delta").load(path).select("order_id")
       new_rows = new_orders.join(existing_ids, "order_id", "left_anti")
       new_rows.write.format("delta").mode("append").save(path)

  3. Structured Streaming checkpoints track processed files exactly-once
     -> a restarted job never reprocesses the same file.

  4. Carry a batch_id / file_name column so a re-run can filter out its own data.

CLEANUP — remove existing duplicates, keep the latest per key:
  Window row_number() over (partition by order_id order by updated_at desc)
  -> DELETE WHERE rn > 1, or rewrite the table with the filtered result.

KEY POINT (interview):
  Idempotency = running the pipeline twice produces the SAME result as once.
  Batch pipelines MUST be idempotent, because failures + retries are guaranteed.
"""

from pyspark.sql import functions as F
from pyspark.sql.window import Window

dup_data = [
    (1, "PLACED",    "2026-01-01 10:00"),
    (1, "DELIVERED", "2026-01-03 10:00"),   # duplicate order_id, later update
    (2, "PLACED",    "2026-01-01 11:00"),
    (2, "CANCELLED", "2026-01-01 12:30"),   # duplicate order_id, later update
    (3, "PLACED",    "2026-01-02 09:00"),
]

orders = spark.createDataFrame(dup_data, ["order_id", "status", "updated_at"])

w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())
clean = (
    orders
    .withColumn("rn", F.row_number().over(w))
    .filter(F.col("rn") == 1)
    .drop("rn")
    .orderBy("order_id")
)
display(clean)

# COMMAND ----------

# DBTITLE 1,Q10: Bad Records / DLQ
# MAGIC %md
# MAGIC ---
# MAGIC ### Q10: Handling Bad / Corrupt Records in ETL
# MAGIC
# MAGIC **Scenario**: You read JSON/CSV files where a few rows have missing required fields, wrong types (`"abc"` in a numeric column), or malformed JSON. The pipeline fails on the first bad row.
# MAGIC
# MAGIC **Question**: How do you process the **good** records while capturing the **bad** ones? Explain schema modes (`PERMISSIVE` / `DROPMALFORMED` / `FAILFAST`) and the **dead letter queue (DLQ)** pattern.

# COMMAND ----------

# DBTITLE 1,Solution Q10
# SOLUTION Q10

"""
SCHEMA MODES (spark.read option 'mode'):

  PERMISSIVE (default):
    - Bad rows are KEPT with NULLs in the corrupt columns
    - Add a _corrupt_record column to capture the raw bad payload:
      .option("mode", "PERMISSIVE")
      .option("columnNameOfCorruptRecord", "_corrupt_record")

  DROPMALFORMED:
    - Bad rows are silently dropped (fast, but you lose the evidence)

  FAILFAST:
    - Abort on the first bad row (for strict curated datasets)

DEAD LETTER QUEUE (DLQ) PATTERN:
  1. Read PERMISSIVE with _corrupt_record
  2. Split:  good = _corrupt_record IS NULL,  bad = IS NOT NULL
  3. Write good rows to the target table
  4. Write bad rows to a quarantine table/volume with:
     source file, ingest timestamp, error reason
  5. Alert + reprocess the DLQ after fixing upstream

AUTO LOADER equivalent:
  .option("badRecordsPath", "/path/to/bad/")  -> bad records written to files

INTERVIEW POINT:
  Never silently drop data in production — quarantine it.
  Monitor data quality metrics (good vs bad record counts) every run.
"""

from pyspark.sql import functions as F

raw = spark.createDataFrame(
    [("1", "100"), ("2", "abc"), ("3", None), ("4", "250")],
    "order_id STRING, amount STRING",
)

# try_cast-style guard: validate BEFORE casting
# (ANSI mode rejects malformed casts like 'abc' -> double)
is_valid = F.col("amount").rlike(r"^\d+(\.\d+)?$")
cleaned = raw.withColumn(
    "amount_clean",
    F.when(is_valid, F.col("amount").cast("double")).otherwise(F.lit(None).cast("double")),
)

good = cleaned.filter(F.col("amount_clean").isNotNull()).drop("amount")
bad = (
    cleaned.filter(F.col("amount_clean").isNull())
    .drop("amount_clean")
    .withColumn("reason", F.lit("invalid amount"))
)

print("— good records —")
display(good)
print("— dead letter queue (bad records) —")
display(bad)

# COMMAND ----------

# DBTITLE 1,Q11: Kimball vs Inmon
# MAGIC %md
# MAGIC ## 📊 Section 6: Data Modeling (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q11: Kimball vs Inmon
# MAGIC
# MAGIC **Question**: Explain the difference between the **Kimball** and **Inmon** data warehouse methodologies. Which approach does the **medallion architecture** (Bronze/Silver/Gold) resemble, and why?

# COMMAND ----------

# DBTITLE 1,Solution Q11
# SOLUTION Q11

"""
INMON (top-down):
  - Build a NORMALIZED (3NF) enterprise data warehouse (EDW) FIRST
  - Single integrated source of truth for the whole organization
  - Departmental data marts are built ON TOP of the EDW
  - Pros: consistent, deduplicated, auditable enterprise model
  - Cons: slow to deliver value (months), heavy upfront modeling

KIMBALL (bottom-up):
  - Build dimensional MODELS (star schemas) directly per BUSINESS PROCESS
  - Conformed facts + dimensions (bus matrix) integrate the marts over time
  - Pros: quick wins, BI-friendly, agile delivery
  - Cons: risk of inconsistent dimensions if not conformed; rework later

WHICH DOES MEDALLION RESEMBLE?
  It's a HYBRID:
    - Silver = normalized / conformed enterprise layer  (Inmon idea)
    - Gold   = dimensional marts per business process    (Kimball idea)

WHEN TO PICK WHICH:
  - Inmon:   large org, strict governance/compliance, single EDW mandate
  - Kimball: fast time-to-value, BI teams per department, agile delivery
"""

print("See comments for the full comparison.")

# COMMAND ----------

# DBTITLE 1,Q12: Fact Table Types
# MAGIC %md
# MAGIC ---
# MAGIC ### Q12: Types of Fact Tables
# MAGIC
# MAGIC **Question**: Explain the three main types of **fact tables** — transactional, periodic snapshot, and accumulating snapshot. Give a real example of each, and state how a row changes over time in each type.

# COMMAND ----------

# DBTITLE 1,Solution Q12
# SOLUTION Q12

"""
1. TRANSACTION FACTS:
   - One row per EVENT / BUSINESS TRANSACTION at a point in time
   - Immutable after insert (append-only)
   - Example: order_line_items, payments, sensor readings, clicks
   - Grain: one row = one transaction line

2. PERIODIC SNAPSHOT FACTS:
   - One row per KEY per PERIOD (day/week/month), even if nothing happened
   - Example: month-end bank account balance, daily inventory snapshot
   - Gotcha: a missing period means NO data was captured that day
   - Grain: one row = one account per period

3. ACCUMULATING SNAPSHOT FACTS:
   - One row per PROCESS / WORKFLOW, updated as the process progresses
   - Row carries MULTIPLE milestone timestamps
     (start -> approved -> shipped -> delivered -> closed)
   - Example: order fulfillment, insurance claim lifecycle
   - The SAME row keeps being UPDATED until the process closes
   - Grain: one row = one business process instance

HOW A ROW CHANGES OVER TIME:
  transaction facts        -> never changes after insert
  periodic snapshot facts  -> a NEW row every period; old rows untouched
  accumulating snapshot    -> the SAME row updated at each milestone

INTERVIEW POINT:
  Always state the GRAIN first — the rest of the model follows from it.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q13: Virtual Warehouses
# MAGIC %md
# MAGIC ## ❄️ Section 7: Snowflake (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q13: Virtual Warehouses — Auto-Suspend, Auto-Resume & Multi-Cluster
# MAGIC
# MAGIC **Question**: Explain Snowflake **virtual warehouses** and the settings `AUTO_SUSPEND`, `AUTO_RESUME`, and `MIN_CLUSTER_COUNT` / `MAX_CLUSTER_COUNT` (multi-cluster). How do these control **cost** and **concurrency**?

# COMMAND ----------

# DBTITLE 1,Solution Q13
# SOLUTION Q13

"""
VIRTUAL WAREHOUSE (VW):
  - Independent compute cluster that runs queries
    (compute is fully separate from storage)
  - No infrastructure management — resize with a SQL command
  - Sizes: XSMALL -> 6XL (each step roughly doubles credits/hour)
  - Teams can share one VW or have isolated VWs (ETL vs BI)

AUTO_SUSPEND:
  - VW suspends after N seconds of inactivity (e.g. 60s)
  - You stop paying compute while suspended
  - Best practice for dev/test: AUTO_SUSPEND = 60

AUTO_RESUME:
  - A suspended VW wakes up automatically when a query arrives
  - Users don't manage warehouse state (a few seconds of warm-up)

MIN / MAX CLUSTER COUNT (multi-cluster):
  - For high CONCURRENCY: scale OUT with identical clusters
  - MIN = always keep N clusters; MAX = grow up to N when queries queue
  - SCALING_POLICY: STANDARD (fill each cluster) vs ECONOMY (spread load)

COST vs CONCURRENCY:
  - One slow heavy query  -> scale UP (bigger size)
  - Many users queuing    -> scale OUT (multi-cluster)
  - Never leave AUTO_SUSPEND = 0 in dev/test warehouses!

CONFIG EXAMPLE:
  CREATE WAREHOUSE analytics_wh
    WAREHOUSE_SIZE = XSMALL
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 4
    SCALING_POLICY = STANDARD;
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q14: Time Travel & Cloning
# MAGIC %md
# MAGIC ---
# MAGIC ### Q14: Time Travel & Zero-Copy Cloning
# MAGIC
# MAGIC **Question**: Explain Snowflake **Time Travel** and **zero-copy cloning**. How do you recover a dropped table or undo a bad `UPDATE`? What is **Fail-safe**? What makes a clone stop being "zero-copy" over time?

# COMMAND ----------

# DBTITLE 1,Solution Q14
# SOLUTION Q14

"""
TIME TRAVEL:
  - Query or restore data AS OF a past point
    (1 day on standard edition, up to 90 days on Enterprise)
  - Uses AT | BEFORE clauses:
      SELECT * FROM orders AT  (TIMESTAMP => '2026-10-13 12:00');
      SELECT * FROM orders BEFORE (STATEMENT => '8e5d0ca9-...');
  - Undo a bad UPDATE:
      CREATE TABLE orders_good CLONE orders
        BEFORE (STATEMENT => '<id_of_bad_statement>');
  - Cost: changed micro-partitions are retained -> extra storage

ZERO-COPY CLONING:
  - CREATE TABLE dev_orders CLONE orders;
  - The clone SHARES the same micro-partitions — no data copied at creation
  - Writes on either side create NEW micro-partitions (copy-on-write)
  - Great for: dev/test environments, risky experiments on prod data

RECOVER A DROPPED TABLE:
  - Within the Time Travel window:  UNDROP TABLE orders;  (instant)
  - Fail-safe: 7 days AFTER Time Travel expires — recoverable only by
    Snowflake support; a last resort, NOT a routine tool

WHEN A CLONE STOPS BEING "ZERO-COPY":
  - Any writes to the clone or the source -> diverging partitions are
    stored separately, so divergence (and storage) grows over time
  - Cloning does NOT copy grants/permissions on the object

DATABRICKS PARALLEL (if asked):
  - Delta Lake: time travel via version AS OF; SHALLOW CLONE for zero-copy
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q15: Pipeline Orchestration
# MAGIC %md
# MAGIC ## 🛠️ Section 8: Monitoring, Logging & Orchestration (3 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q15: Pipeline Orchestration in Databricks
# MAGIC
# MAGIC **Scenario**: You have a multi-step ETL pipeline: extract from S3 → transform in Bronze → Silver → Gold → send notification. Steps depend on each other and some can fail.
# MAGIC
# MAGIC **Question**: How do you **orchestrate** this pipeline in Databricks? Explain **Databricks Jobs**, task dependencies, retries, and failure handling. What are the alternatives (Airflow, ADF)?
# MAGIC
# MAGIC **Hint**: Databricks Jobs = tasks + dependencies (Run If / For Each), with retries and alerting.

# COMMAND ----------

# DBTITLE 1,Solution Q15
# SOLUTION Q15

"""
DATABRICKS JOBS — the native orchestrator:

  1. TASK TYPES:
     - Notebook task: run a notebook (pass parameters)
     - Python script task: run a .py file
     - SQL task: run a SQL query or a dashboard refresh
     - Pipeline task: trigger a Spark Declarative Pipeline (SDP)
     - dbt task: run a dbt model
     - Custom: run any code

  2. TASK DEPENDENCIES:
     - Define an ordered DAG: task B depends on task A (Run After)
     - 'Run If' condition: run only if previous succeeded / failed / all_done
     - 'For Each' task: fan-out parallel iterations over a list

  3. RETRIES:
     - max_retries: re-run the task N times before failing
     - retry_interval_seconds: wait between retries
     - Example: max_retries=3, min_retry_interval_millis=60000

  4. FAILURE HANDLING:
     - on_failure: retry, skip, or stop the whole job
     - Email / webhook / Slack notifications on failure
     - 'Run If' with condition 'always' for cleanup tasks

  5. TRIGGERS:
     - Schedule (cron): e.g., daily at 2 AM
     - File arrival: trigger when new file lands in S3/ADLS
     - Table update: trigger when a Delta table changes
     - Manual / API trigger

ALTERNATIVES:
  - Apache Airflow: DAGs with Python operators, more flexible but self-managed.
  - Azure Data Factory (ADF): visual pipeline builder, cloud-native for Azure.
  - Databricks Jobs is simplest when your entire pipeline is in Databricks.

INTERVIEW POINT:
  Orchestration = ordering + retries + error handling + alerting.
  A good pipeline is: idempotent, retriable, observable, and fails fast.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q16: Pipeline Monitoring
# MAGIC %md
# MAGIC ---
# MAGIC ### Q16: Monitoring a Data Pipeline (Observability)
# MAGIC
# MAGIC **Scenario**: Your nightly ETL runs "green" (no failures), but analysts complain the reports are wrong — volumes dropped silently, data is stale.
# MAGIC
# MAGIC **Question**: What do you **monitor** in a production data pipeline? Cover **pipeline-level** monitoring (runs, durations, SLAs, backlogs) AND **data-level** monitoring (freshness, volume, quality). Which Databricks tools would you use?
# MAGIC
# MAGIC **Hint**: Monitor the DATA, not just the JOB. system tables, Lakehouse Monitoring, SQL alerts.

# COMMAND ----------

# DBTITLE 1,Solution Q16
# SOLUTION Q16

"""
MONITORING = PIPELINE-LEVEL + DATA-LEVEL

1. PIPELINE / OPERATIONAL MONITORING:
   - Job runs: success / failure, duration trends, retries
   - SLAs: did the daily table land before 8 AM?
   - Backlog: streaming lag, Auto Loader queued files
   - Compute: utilization, cost per run
   - Alerting: email / webhook / Slack on failure or SLA breach

2. DATA-LEVEL MONITORING (the half everyone forgets!):
   - FRESHNESS: MAX(updated_at) — how stale is the table?
   - VOLUME: row counts per day — sudden drops/spikes = upstream break
   - QUALITY: null rates, duplicates, value ranges, schema drift
   - DISTRIBUTION: mean/stddev of key metrics — silent corruption

DATABRICKS TOOLS:
   - system.lakeflow.* system tables: job + pipeline run history (account-wide)
   - system.query.* / system.billing.*: query history + cost monitoring
   - Lakehouse Monitoring: scheduled data-quality monitors on tables
     (freshness, completeness, drift metrics tracked over time)
   - Databricks SQL alerts + dashboards: scheduled checks with email/webhook

PATTERN (interview favorite — build it yourself):
  1. After each ETL run, write metrics to a metrics table:
     (run_date, table_name, row_count, null_rate, max_updated_at)
  2. Scheduled SQL compares today's metrics vs a 7-day average
  3. Alert fires when deviation > threshold (e.g. volume -40%)

KEY POINT:
  A pipeline that runs GREEN can still deliver WRONG data.
  Monitor the DATA, not just the JOB.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q17: Logging & Debugging
# MAGIC %md
# MAGIC ---
# MAGIC ### Q17: Logging & Debugging Best Practices (Spark / Databricks)
# MAGIC
# MAGIC **Question**: What are the **logging best practices** for Spark/Databricks pipelines (log4j levels, Python `logging` vs `print`, what to log)? Walk me through **debugging a job that failed at 3 AM** — where exactly do you look?
# MAGIC
# MAGIC **Hint**: Job run page → error/stack trace → driver logs (stdout/stderr) → Spark UI / query profile → Delta DESCRIBE HISTORY.

# COMMAND ----------

# DBTITLE 1,Solution Q17
# SOLUTION Q17

"""
LOGGING BEST PRACTICES:

1. LOG LEVELS (log4j): ERROR > WARN > INFO > DEBUG
   - Spark default is WARN; use INFO only when debugging
   - In production pipelines: keep application logs at INFO

2. USE `logging`, NOT `print`:
   - logger = logging.getLogger("etl")
     logger.info("loaded %d rows", df.count())   # lazy formatting
   - print() has no levels, no timestamps, and buffers output

3. WHAT TO LOG (make failures debuggable):
   - run_id / batch_id / file names (traceability)
   - row counts IN and OUT of each step (catches data loss)
   - durations per step, partitions, files written
   - job version + config for reproducibility

4. NEVER swallow exceptions:
   - `except: pass` = interview red flag. Fail FAST with a clear message
     naming the table / file / batch that broke.

DEBUGGING A 3 AM FAILURE (walk-through):
  1. Job run page: which task failed, when, stack trace
  2. Read the ROOT exception (bottom of the trace), not the wrapper
  3. Driver logs: cluster -> Driver logs (stdout/stderr/log4j),
     or log delivery to S3 for long-term storage
  4. Spark UI / query profile: which stage/task, shuffle, spill
  5. Data checks: Delta DESCRIBE HISTORY (recent commits),
     row counts vs yesterday, schema of the file that failed
  6. system.access.audit if a permission change is suspected

INTERVIEW POINT:
  Good logging + idempotent retries + batch IDs = failures become
  5-minute investigations instead of all-night debugging.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Day 2 Complete
# MAGIC %md
# MAGIC ---
# MAGIC ## ✅ Day 2 Complete!
# MAGIC
# MAGIC **17 questions covered across 8 categories.**
# MAGIC
# MAGIC ### Score Yourself:
# MAGIC | Category | Questions | Your Score |
# MAGIC |----------|-----------|-----------|
# MAGIC | SQL Advanced | 2 | / 2 |
# MAGIC | Python | 2 | / 2 |
# MAGIC | PySpark | 2 | / 2 |
# MAGIC | Spark Optimization | 2 | / 2 |
# MAGIC | ETL | 2 | / 2 |
# MAGIC | Data Modeling | 2 | / 2 |
# MAGIC | Snowflake | 2 | / 2 |
# MAGIC | Monitoring, Logging & Orchestration | 3 | / 3 |
# MAGIC
# MAGIC **Total: / 17**
# MAGIC
# MAGIC ---
# MAGIC Next day: `day_03` notebook with fresh questions! 🚀