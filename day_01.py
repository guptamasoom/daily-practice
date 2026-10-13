# Databricks notebook source
# DBTITLE 1,Day 1 — Mock Interview Practice
# MAGIC %md
# MAGIC # 📅 Day 1 — Mock Interview Practice
# MAGIC
# MAGIC **Date**: Oct 13, 2026
# MAGIC
# MAGIC **Topics Covered**:
# MAGIC | # | Category | Questions |
# MAGIC |---|----------|----------|
# MAGIC | 1 | SQL Advanced | 2 |
# MAGIC | 2 | Python (Loop/Function/List/Dict) | 2 |
# MAGIC | 3 | PySpark Coding | 2 |
# MAGIC | 4 | Spark Optimization & Deep Spark | 2 |
# MAGIC | 5 | ETL (Failures, Late Data, Schema) | 2 |
# MAGIC | 6 | Data Modeling | 2 |
# MAGIC | 7 | Snowflake | 2 |
# MAGIC
# MAGIC **Total**: 14 questions
# MAGIC
# MAGIC ---
# MAGIC **Instructions**: Read the question, try to solve it yourself first, then check the solution cell below.

# COMMAND ----------

# DBTITLE 1,Q1: 2nd Highest Salary Per Dept
# MAGIC %md
# MAGIC ## 🔷 Section 1: SQL Advanced (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q1: 2nd Highest Salary Per Department
# MAGIC
# MAGIC **Table**: `employees (emp_id, emp_name, salary, department_id)`
# MAGIC
# MAGIC **Question**: Write a SQL query to find the **2nd highest salary** in each department. If a department has fewer than 2 employees, it should not appear in the result.
# MAGIC
# MAGIC **Expected Output**: `department_id, emp_name, salary`

# COMMAND ----------

# DBTITLE 1,Solution Q1
# SOLUTION Q1
%sql
WITH ranked_salaries AS (
  SELECT
    department_id,
    emp_name,
    salary,
    DENSE_RANK() OVER (
      PARTITION BY department_id
      ORDER BY salary DESC
    ) AS salary_rank
  FROM employees
)
SELECT
  department_id,
  emp_name,
  salary
FROM ranked_salaries
WHERE salary_rank = 2
ORDER BY department_id;

# COMMAND ----------

# DBTITLE 1,Q2: Consecutive Login Days
# MAGIC %md
# MAGIC ---
# MAGIC ### Q2: Consecutive Login Days (Gaps & Islands)
# MAGIC
# MAGIC **Table**: `logins (user_id, login_date)`
# MAGIC
# MAGIC **Question**: Write a SQL query to find each user's **longest consecutive login streak** (consecutive days without a gap). Return `user_id, max_streak_days`.
# MAGIC
# MAGIC **Hint**: This is a classic "gaps & islands" problem. Use `ROW_NUMBER()` and date arithmetic to identify consecutive groups.

# COMMAND ----------

# DBTITLE 1,Solution Q2
# SOLUTION Q2
%sql
WITH login_groups AS (
  SELECT
    user_id,
    login_date,
    -- Group consecutive dates: difference between date and row_number is constant
    DATE_SUB(login_date, ROW_NUMBER() OVER (
      PARTITION BY user_id
      ORDER BY login_date
    )) AS grp
  FROM (
    SELECT DISTINCT user_id, CAST(login_date AS DATE) AS login_date
    FROM logins
  )
),
streaks AS (
  SELECT
    user_id,
    grp,
    COUNT(*) AS streak_days
  FROM login_groups
  GROUP BY user_id, grp
)
SELECT
  user_id,
  MAX(streak_days) AS max_streak_days
FROM streaks
GROUP BY user_id
ORDER BY max_streak_days DESC;

# COMMAND ----------

# DBTITLE 1,Q3: Prime Numbers
# MAGIC %md
# MAGIC ## 🐍 Section 2: Python (Loop / Function / List / Dict) (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q3: Prime Numbers Using Function + Loop
# MAGIC
# MAGIC **Question**: Write a Python function `find_primes(n)` that returns all prime numbers up to `n` (inclusive). Use a loop inside the function. Optimize it by checking divisibility only up to `√n`.
# MAGIC
# MAGIC **Example**: `find_primes(20)` → `[2, 3, 5, 7, 11, 13, 17, 19]`

# COMMAND ----------

# DBTITLE 1,Solution Q3
# SOLUTION Q3
def find_primes(n):
    """Return all prime numbers up to n (inclusive)."""
    if n < 2:
        return []
    
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        # Check divisibility only up to sqrt(num)
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

# Test
print(find_primes(20))
# Output: [2, 3, 5, 7, 11, 13, 17, 19]

print(find_primes(50))
# Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# COMMAND ----------

# DBTITLE 1,Q4: Group Anagrams
# MAGIC %md
# MAGIC ---
# MAGIC ### Q4: Group Anagrams Using Dictionary
# MAGIC
# MAGIC **Question**: Given a list of strings, write a Python function `group_anagrams(words)` that groups all anagrams together using a **dictionary**. Return a list of lists.
# MAGIC
# MAGIC **Anagram**: Words with the same characters in different order (e.g., "listen" and "silent").
# MAGIC
# MAGIC **Example**: `group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])` → `[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]`

# COMMAND ----------

# DBTITLE 1,Solution Q4
# SOLUTION Q4
def group_anagrams(words):
    """Group words by anagram using a dictionary."""
    anagram_map = {}  # key = sorted tuple of chars, value = list of words
    
    for word in words:
        # Sort the characters to create a common key
        key = tuple(sorted(word))
        if key not in anagram_map:
            anagram_map[key] = []
        anagram_map[key].append(word)
    
    return list(anagram_map.values())

# Test
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

print(group_anagrams(["listen", "silent", "enlist", "hello", "world"]))
# Output: [['listen', 'silent', 'enlist'], ['hello'], ['world']]

# COMMAND ----------

# DBTITLE 1,Q5: Top 3 Products by Revenue
# MAGIC %md
# MAGIC ## ⚡ Section 3: PySpark Coding (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q5: Top 3 Products by Revenue Per Category
# MAGIC
# MAGIC **DataFrame**: `sales` with columns: `product_id, product_name, category, revenue`
# MAGIC
# MAGIC **Question**: Using PySpark, find the **top 3 products by total revenue** in each category. Use window functions over DataFrame API.
# MAGIC
# MAGIC **Expected Output**: `category, product_name, total_revenue, rank`

# COMMAND ----------

# DBTITLE 1,Solution Q5
# SOLUTION Q5
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Sample data
sales_data = [
    ("P01", "iPhone", "Electronics", 1000),
    ("P02", "MacBook", "Electronics", 2000),
    ("P03", "iPad", "Electronics", 800),
    ("P04", "AirPods", "Electronics", 200),
    ("P05", "Samsung TV", "Electronics", 1500),
    ("P06", "Jeans", "Clothing", 50),
    ("P07", "Shirt", "Clothing", 30),
    ("P08", "Jacket", "Clothing", 120),
]

sales = spark.createDataFrame(sales_data, ["product_id", "product_name", "category", "revenue"])

# Aggregate revenue per product
product_revenue = (
    sales.groupBy("category", "product_name")
    .agg(F.sum("revenue").alias("total_revenue"))
)

# Window: rank by revenue within each category
window_spec = Window.partitionBy("category").orderBy(F.col("total_revenue").desc())

top_3 = (
    product_revenue
    .withColumn("rank", F.rank().over(window_spec))
    .filter(F.col("rank") <= 3)
    .orderBy("category", "rank")
)

display(top_3)

# COMMAND ----------

# DBTITLE 1,Q6: Running Total with Reset
# MAGIC %md
# MAGIC ---
# MAGIC ### Q6: Running Total with Reset on Condition
# MAGIC
# MAGIC **DataFrame**: `telemetry` with columns: `event_id, vin, event_ts, speed_kmh`
# MAGIC
# MAGIC **Question**: Using PySpark, calculate a **running total of distance** per vehicle, but **reset the total to 0** whenever `speed_kmh == 0` (vehicle stopped). This requires a gaps-and-islands approach in Spark.
# MAGIC
# MAGIC **Hint**: Use a flag column, cumulative sum to create groups, then sum within each group.

# COMMAND ----------

# DBTITLE 1,Solution Q6
# SOLUTION Q6
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Sample data
telemetry_data = [
    ("E1", "VIN001", "2026-01-01 10:00:00", 50.0),
    ("E2", "VIN001", "2026-01-01 10:01:00", 60.0),
    ("E3", "VIN001", "2026-01-01 10:02:00", 0.0),   # STOP → reset
    ("E4", "VIN001", "2026-01-01 10:03:00", 40.0),
    ("E5", "VIN001", "2026-01-01 10:04:00", 55.0),
    ("E6", "VIN001", "2026-01-01 10:05:00", 0.0),   # STOP → reset
    ("E7", "VIN001", "2026-01-01 10:06:00", 30.0),
]

telemetry = spark.createDataFrame(
    telemetry_data,
    ["event_id", "vin", "event_ts", "speed_kmh"]
)

telemetry = telemetry.withColumn("event_ts", F.to_timestamp("event_ts"))

w = Window.partitionBy("vin").orderBy("event_ts")

# Step 1: Flag when vehicle stops (speed = 0)
telemetry = telemetry.withColumn("is_stop", F.when(F.col("speed_kmh") == 0, 1).otherwise(0))

# Step 2: Cumulative sum of stop flags creates group IDs
telemetry = telemetry.withColumn("group_id", F.sum("is_stop").over(w))

# Step 3: Running total within each group
w_group = Window.partitionBy("vin", "group_id").orderBy("event_ts").rowsBetween(Window.unboundedPreceding, Window.currentRow)

telemetry = telemetry.withColumn("running_total_speed", F.sum("speed_kmh").over(w_group))

display(telemetry.select("event_id", "vin", "event_ts", "speed_kmh", "group_id", "running_total_speed"))

# COMMAND ----------

# DBTITLE 1,Q7: Broadcast vs Sort-Merge Join
# MAGIC %md
# MAGIC ## 🔥 Section 4: Spark Optimization & Deep Spark (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q7: Broadcast Join vs Sort-Merge Join
# MAGIC
# MAGIC **Question**: Explain the difference between **Broadcast Join** and **Sort-Merge Join** in Spark. When would you use each? What are the configuration parameters?
# MAGIC
# MAGIC **Follow-up**: What happens if you broadcast a DataFrame that is larger than `spark.sql.autoBroadcastJoinThreshold`?

# COMMAND ----------

# DBTITLE 1,Solution Q7
# SOLUTION Q7

"""
BROADCAST JOIN (BroadcastHashJoin):
- Spark broadcasts the SMALLER DataFrame to ALL executors
- Each executor joins its partition of the large DF with the broadcasted small DF in memory
- NO shuffle needed for the large DataFrame
- Best for: small DataFrame (< ~10MB by default, can go up to ~8GB)
- Config: spark.sql.autoBroadcastJoinThreshold = 10485760  (10MB default)
- Explicit: df_large.join(broadcast(df_small), "key")
- Risk: broadcasting a too-large DF → executor OOM

SORT-MERGE JOIN (SortMergeJoin):
- Both DataFrames are sorted on the join key, then merged
- Requires shuffle (both sides sorted + shuffled by join key)
- Best for: LARGE-LARGE joins (both sides are big)
- Default join in Spark for large DataFrames
- Config: spark.sql.join.preferSortMergeJoin = true
- More memory efficient for large data, but slower due to shuffle

ANSWER TO FOLLOW-UP:
If DataFrame is larger than autoBroadcastJoinThreshold:
- Spark will choose SortMergeJoin by default
- BUT if you explicitly call broadcast(df), Spark will still broadcast it
- If the DF is too large (e.g. several GB), this causes:
  1. High memory pressure on driver (collecting data to broadcast)
  2. High network I/O (sending to all executors)
  3. Risk of OOM on executors
- Solution: increase threshold ONLY if you know the DF fits in memory
"""

from pyspark.sql.functions import broadcast

# Example: Explicit broadcast join
# df_large.join(broadcast(df_small), "key")  # small DF broadcast to all executors

# Example: Set threshold
# spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)  # 50MB

# Example: Force sort-merge join (disable broadcast)
# spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)  # disables auto-broadcast

print("See comments for full explanation.")

# COMMAND ----------

# DBTITLE 1,Q8: Data Skew Handling
# MAGIC %md
# MAGIC ---
# MAGIC ### Q8: Handling Data Skew in Spark
# MAGIC
# MAGIC **Question**: You have a Spark job doing a `groupBy("customer_id")` but one customer has 10x more data than others, causing one task to take 30 minutes while all others finish in 2 minutes. How do you fix this?
# MAGIC
# MAGIC **Hint**: Explain the **salting technique** and **Adaptive Query Execution (AQE) skew join**.

# COMMAND ----------

# DBTITLE 1,Solution Q8
# SOLUTION Q8

"""
PROBLEM: Data skew — one key has disproportionately more data, causing:
  - One task runs much longer than others (straggler)
  - OutOfMemoryError on one executor
  - Overall job slow due to waiting for one task

SOLUTION 1: SALTING TECHNIQUE (manual)
  1. Add a random salt (0-9) to the skewed key on BOTH sides of the join
  2. Join on (key, salt) — distributes the skewed key across 10 partitions
  3. After join, remove the salt and re-aggregate

  df1_salted = df1.withColumn("salt", (rand() * 10).cast("int"))
  df2_salted = df2.withColumn("salt", explode(array([lit(i) for i in range(10)])))
  joined = df1_salted.join(df2_salted, ["key", "salt"])
  result = joined.drop("salt").groupBy("key").agg(...)

SOLUTION 2: ADAPTIVE QUERY EXECUTION (AQE) — Spark 3.x
  - spark.sql.adaptive.enabled = true
  - spark.sql.adaptive.skewJoin.enabled = true
  - AQE automatically detects skew at runtime and splits skewed partitions
  - No code change needed — just config

SOLUTION 3: INCREASE PARTITIONS
  - spark.sql.shuffle.partitions = 400  (default 200)
  - Or use repartition() before the operation
  - df.repartition(400, "customer_id")

SOLUTION 4: CUSTOM PARTITIONER (RDD level)
  - For extreme skew, use a custom partitioner that distributes
    the heavy key across multiple partitions

BEST PRACTICE:
  1. First try AQE skew join (zero code change)
  2. If still skewed, try increasing shuffle partitions
  3. If still skewed, use salting technique
  4. Monitor with Spark UI — look at task duration distribution
"""

# Enable AQE skew join
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Salting example
from pyspark.sql.functions import rand, lit, explode, array

# df_skewed: has a column customer_id with skewed distribution
# df_small: dimension table

# Step 1: Salt the large table
df_skewed_salted = (
    df_skewed
    .withColumn("salt", (rand() * 10).cast("int"))
)

# Step 2: Explode salt on small table (replicate 10x)
df_small_salted = (
    df_small
    .withColumn("salt", explode(array([lit(i) for i in range(10)])))
)

# Step 3: Join on (customer_id, salt)
joined = df_skewed_salted.join(df_small_salted, ["customer_id", "salt"])

# Step 4: Drop salt and re-aggregate if needed
result = joined.drop("salt")

print("See comments for full explanation.")

# COMMAND ----------

# DBTITLE 1,Q9: Schema Evolution
# MAGIC %md
# MAGIC ## 🔄 Section 5: ETL (Failures, Late Data, Schema Handling) (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q9: Schema Evolution — Source Added a New Column
# MAGIC
# MAGIC **Scenario**: Your ETL pipeline reads JSON files from S3 into a Delta Lake Bronze table. One day, the source system adds a new column `tire_pressure_psi` to the JSON events. The existing Delta table doesn't have this column.
# MAGIC
# MAGIC **Question**: How do you handle this schema change WITHOUT breaking the pipeline? Explain 3 approaches and their trade-offs.

# COMMAND ----------

# DBTITLE 1,Solution Q9
# SOLUTION Q9

"""
APPROACH 1: AutoMerge (simplest)
  - Delta Lake supports automatic schema evolution on write
  - Set .option("mergeSchema", "true") on the write
  - New columns are added to the Delta table automatically
  - Existing rows get NULL for the new column

  df.write.format("delta").option("mergeSchema", "true").mode("append").save(path)

  Pros: Zero code change, works automatically
  Cons: No control over column position, type mismatches possible

APPROACH 2: Explicit Schema Evolution with ALTER TABLE
  - Detect the new column before writing
  - ALTER TABLE to add the column explicitly
  - Then write as normal

  ALTER TABLE delta.`/path/to/bronze` ADD COLUMNS (tire_pressure_psi DOUBLE)

  Pros: Full control, can add column comments, set default values
  Cons: Requires pre-detection logic, more code

APPROACH 3: Schema Registry + Validation (production-grade)
  - Maintain a schema registry (e.g. in a config table)
  - Compare incoming schema against expected schema
  - If new column detected:
    1. Alert the data engineering team
    2. Auto-add to schema registry
    3. Update the Delta table schema
    4. Update downstream consumers (Silver/Gold)
  - If column removed or type changed → quarantine + alert

  Pros: Full governance, audit trail, controlled changes
  Cons: Most complex, requires infrastructure

BEST PRACTICE:
  - Use mergeSchema=true for Bronze (accept everything)
  - Use explicit schema for Silver/Gold (controlled)
  - Auto Loader's schemaLocation handles schema evolution automatically
  - Set spark.databricks.delta.schema.autoMerge.enabled = true for global
"""

# Auto Loader with schema evolution
raw_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/checkpoint/schema/")
    .option("cloudFiles.inferColumnTypes", "true")  # evolve types too
    .load("/s3/raw/")
)

# Write with mergeSchema
(raw_stream.writeStream
    .format("delta")
    .option("mergeSchema", "true")  # auto-add new columns
    .option("checkpointLocation", "/checkpoint/bronze/")
    .start("/delta/bronze/"))

print("See comments for 3 approaches.")

# COMMAND ----------

# DBTITLE 1,Q10: Late Data in Batch ETL
# MAGIC %md
# MAGIC ---
# MAGIC ### Q10: Late Arriving Data in Batch ETL
# MAGIC
# MAGIC **Scenario**: Your batch ETL runs nightly at 2 AM. It reads yesterday's data from S3, processes it through Bronze → Silver → Gold, and updates a checkpoint. But sometimes, files arrive late (even 2-3 days late) because of upstream delays.
# MAGIC
# MAGIC **Question**: How do you handle late-arriving data in a **batch** ETL pipeline? Explain your strategy for ensuring no data is lost.

# COMMAND ----------

# DBTITLE 1,Solution Q10
# SOLUTION Q10

"""
STRATEGY 1: Checkpoint with Lookback Window
  - Instead of processing only yesterday, look back N days
  - Process all runs newer than checkpoint
  - Late files get picked up on the next run

  checkpoint = last_processed_run_id  (e.g. 20261010)
  all_runs = discover_runs_from_s3()
  new_runs = [r for r in all_runs if r > checkpoint]
  process(new_runs)  # includes late arrivals

  Pros: Simple, handles late data naturally
  Cons: Re-reads some data (idempotency needed)

STRATEGY 2: Idempotent Writes (critical for reprocessing)
  - Use event_id as unique key
  - Before writing to Bronze, check if event_id already exists
  - Use left_anti join to filter out duplicates
  - OR use MERGE INTO with event_id as merge key

  existing_ids = spark.read.delta("/bronze").select("event_id")
  new_data = new_data.join(existing_ids, "event_id", "left_anti")
  new_data.write.delta("/bronze", mode="append")

STRATEGY 3: Partition by Event Date (not ingestion date)
  - Partition by event_date, not ingestion_date
  - Late data lands in the correct event_date partition
  - Downstream queries by date always get complete data
  - Use MERGE to update aggregates for affected dates

STRATEGY 4: MERGE for Aggregations (Gold)
  - When late data arrives, Gold aggregates must be recomputed
  - Use MERGE INTO to upsert affected keys
  - Only recompute for affected partitions (not full rebuild)

  MERGE INTO gold_hourly AS target
  USING (SELECT vin, event_hour, avg(speed) FROM new_silver GROUP BY vin, event_hour) AS source
  ON target.vin = source.vin AND target.event_hour = source.event_hour
  WHEN MATCHED THEN UPDATE SET *
  WHEN NOT MATCHED THEN INSERT *

BEST PRACTICE (our Tesla pipeline):
  1. Checkpoint tracks last_processed_run_id
  2. Bronze: append-only with event_id idempotency (left_anti join)
  3. Silver: append-only with event_id idempotency
  4. Gold: MERGE for aggregation tables, append for event-level
  5. Checkpoint updated ONLY after successful write
  6. Retry-safe: re-run processes same data → 0 duplicates
"""

print("See comments for full strategy.")

# COMMAND ----------

# DBTITLE 1,Q11: Star vs Snowflake Schema
# MAGIC %md
# MAGIC ## 📊 Section 6: Data Modeling (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q11: Star Schema vs Snowflake Schema
# MAGIC
# MAGIC **Question**: Explain the difference between **Star Schema** and **Snowflake Schema**. When would you choose one over the other? Give an example of each.

# COMMAND ----------

# DBTITLE 1,Solution Q11
# SOLUTION Q11

"""
STAR SCHEMA:
  - Fact table at center, directly connected to dimension tables
  - Dimensions are FLAT (denormalized) — all attributes in one table
  - No snowflaking — no dimension references another dimension

  Example:
    fact_sales (sale_id, product_id, store_id, date_id, quantity, amount)
    dim_product (product_id, product_name, category, brand)  ← all in one table
    dim_store (store_id, store_name, city, state, region)       ← all in one table
    dim_date (date_id, date, month, quarter, year)

  Pros:
    - Simpler queries (fewer joins)
    - Faster query performance (fewer joins)
    - Easier for BI tools to understand
  Cons:
    - Data redundancy in dimension tables
    - Larger storage

SNOWFLAKE SCHEMA:
  - Dimensions are NORMALIZED into multiple tables
  - A dimension can reference another dimension (snowflaking)

  Example:
    fact_sales (sale_id, product_id, store_id, date_id, quantity, amount)
    dim_product (product_id, product_name, category_id)  → references dim_category
    dim_category (category_id, category_name, brand_id)   → references dim_brand
    dim_brand (brand_id, brand_name)
    dim_store (store_id, store_name, city_id)             → references dim_city
    dim_city (city_id, city_name, state_id)               → references dim_state
    dim_date (date_id, date, month, quarter, year)

  Pros:
    - Less data redundancy (normalized)
    - Smaller storage
    - Easier to maintain (update a category name in one place)
  Cons:
    - More joins needed for queries
    - Slower query performance
    - More complex for BI tools

WHEN TO USE STAR:
  - OLAP / Data warehousing for BI dashboards
  - Performance is priority (fewer joins)
  - Storage is not a concern
  - Most common in modern data platforms (Databricks, Snowflake)

WHEN TO USE SNOWFLAKE:
  - Highly normalized requirements
  - Storage is very expensive
  - Complex dimension hierarchies (e.g. product → category → brand → manufacturer)
  - Rare in practice — star is preferred for analytics

MODERN APPROACH:
  - Use Star Schema for the presentation layer (BI/dashboards)
  - Use normalized 3NF in the Bronze/Silver layers
  - Denormalize into Star in the Gold layer
"""

print("See comments for full comparison.")

# COMMAND ----------

# DBTITLE 1,Q12: SCD Type 2
# MAGIC %md
# MAGIC ---
# MAGIC ### Q12: SCD Type 2 Implementation
# MAGIC
# MAGIC **Question**: Explain **Slowly Changing Dimension (SCD) Type 2**. How do you implement it in a data warehouse? Show the table design and the MERGE logic.
# MAGIC
# MAGIC **Scenario**: A customer changes their city from Berlin to Munich. How do you track this change historically?

# COMMAND ----------

# DBTITLE 1,Solution Q12
# SOLUTION Q12

"""
SCD TYPE 2:
  - Tracks historical changes by keeping MULTIPLE versions of a row
  - Each version has effective_date, end_date, and is_current flag
  - When a change occurs, the old record is expired and a new one is inserted

TABLE DESIGN:
  dim_customer (
    customer_sk       BIGINT,        -- surrogate key (unique per version)
    customer_id       VARCHAR,       -- natural key (business key)
    customer_name     VARCHAR,
    city              VARCHAR,
    effective_date    TIMESTAMP,     -- when this version became active
    end_date          TIMESTAMP,     -- when this version expired (NULL = current)
    is_current        BOOLEAN,       -- TRUE for the latest version
  )

EXAMPLE:
  customer_id=100, city=Berlin, effective=2026-01-01, end=NULL, is_current=TRUE
  → Customer moves to Munich on 2026-06-01
  → Old row: end=2026-05-31, is_current=FALSE
  → New row: city=Munich, effective=2026-06-01, end=NULL, is_current=TRUE
"""

from pyspark.sql import functions as F
from delta.tables import DeltaTable

# MERGE logic for SCD Type 2 in Delta Lake

def apply_scd2(delta_path, new_data, natural_key="customer_id"):
    """
    Apply SCD Type 2 merge to a Delta dimension table.
    
    new_data: DataFrame with latest snapshot from source
    natural_key: business key to match on
    """
    target = DeltaTable.forPath(spark, delta_path)
    
    (
        target.alias("old")
        .merge(
            new_data.alias("new"),
            f"old.{natural_key} = new.{natural_key} AND old.is_current = true"
        )
        .whenMatchedUpdate(
            condition=F.col("old.city") != F.col("new.city"),  # only if changed
            set={
                "end_date": F.current_timestamp(),
                "is_current": F.lit(False),
            }
        )
        .whenNotMatchedInsert(
            values={
                natural_key: F.col(f"new.{natural_key}"),
                "customer_name": F.col("new.customer_name"),
                "city": F.col("new.city"),
                "effective_date": F.current_timestamp(),
                "end_date": F.lit(None).cast("timestamp"),
                "is_current": F.lit(True),
            }
        )
        .execute()
    )
    
    # Insert new versions for changed records
    changed = (
        target.toDF()
        .filter(F.col("is_current") == False)
        .join(new_data, natural_key)
        .select(
            f"new.{natural_key}",
            "new.customer_name",
            "new.city",
            F.current_timestamp().alias("effective_date"),
            F.lit(None).cast("timestamp").alias("end_date"),
            F.lit(True).alias("is_current"),
        )
    )
    
    changed.write.format("delta").mode("append").save(delta_path)

print("SCD Type 2 implementation shown above.")

# COMMAND ----------

# DBTITLE 1,Q13: Micro-Partitions
# MAGIC %md
# MAGIC ## ❄️ Section 7: Snowflake (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q13: Snowflake Micro-Partition Architecture
# MAGIC
# MAGIC **Question**: Explain Snowflake's **micro-partition** architecture. How does it differ from traditional partitioning? Why does it enable fast queries without manual partition pruning?

# COMMAND ----------

# DBTITLE 1,Solution Q13
# SOLUTION Q13

"""
SNOWFLAKE MICRO-PARTITIONS:

What are they?
  - Snowflake automatically divides each table into small partitions called micro-partitions
  - Each micro-partition contains 50-500 MB of compressed data (typically 50-100MB)
  - Each micro-partition stores columnar data with min/max statistics for EVERY column

Key Characteristics:
  1. AUTOMATIC — no manual partitioning needed (unlike Hive/Delta where you specify partitionBy)
  2. COLUMNAR — data within each micro-partition is stored column-by-column
  3. STATISTICS — for each column, Snowflake stores: min, max, distinct count, NULL count
  4. IMMUTABLE — micro-partitions are never updated in place; new versions create new micro-partitions (copy-on-write)

How it differs from traditional partitioning:

  Traditional (Hive/Delta):
    - You manually specify partition columns (e.g. PARTITION BY (event_date))
    - Partition pruning only works on the partition column
    - If you query by a non-partition column, full scan
    - Partition count is typically 10s-100s

  Snowflake Micro-Partitions:
    - ALL columns have statistics, so pruning works on ANY column
    - Query by event_date → prunes micro-partitions by date range
    - Query by customer_id → ALSO prunes by customer_id range
    - A table can have millions of micro-partitions
    - No need to choose partition columns — Snowflake optimizes automatically

Why fast without manual pruning?
  1. Query optimizer reads min/max stats for each micro-partition
  2. If the filter value is outside [min, max] of a micro-partition → skip it
  3. Example: SELECT * FROM sales WHERE date = '2026-01-15'
     - Snowflake checks each micro-partition's date min/max
     - Only reads micro-partitions where date range includes Jan 15
     - Could skip 99% of micro-partitions without reading them
  4. This is called "column pruning" + "partition pruning" combined

Performance Benefit:
  - Traditional: scan 1 partition (manually partitioned) but miss non-partition filters
  - Snowflake: scan only relevant micro-partitions across ALL filter columns
  - Called "zonemap pruning" — similar to Delta's data skipping but automatic and multi-column

Example:
  Table: 1 billion rows, 1TB
  Micro-partitions: ~10,000 (each ~100MB)
  Query: WHERE city = 'Berlin' AND date = '2026-01-15'
  - Snowflake prunes by city AND date simultaneously
  - Might read only 50 micro-partitions (5MB) out of 10,000
  - 99.5% data skipped without being read
"""

print("See comments for full explanation.")

# COMMAND ----------

# DBTITLE 1,Q14: Snowflake Table Types
# MAGIC %md
# MAGIC ---
# MAGIC ### Q14: Snowflake Table Types — PERMANENT vs TRANSIENT vs TEMPORARY
# MAGIC
# MAGIC **Question**: Explain the difference between **PERMANENT**, **TRANSIENT**, and **TEMPORARY** tables in Snowflake. When would you use each? What are the cost implications?

# COMMAND ----------

# DBTITLE 1,Solution Q14
# SOLUTION Q14

"""
SNOWFLAKE TABLE TYPES:

PERMANENT TABLES:
  - Created with: CREATE TABLE (default)
  - Fail-safe: 7 days of data recovery after Time Travel expires
  - Time Travel: Up to 90 days (Enterprise+)
  - Survives session close, account restart
  - Storage cost: Full cost + Fail-safe storage
  - Use case: Production tables, source of truth, compliance-required data

TRANSIENT TABLES:
  - Created with: CREATE TRANSIENT TABLE
  - Fail-safe: NO fail-safe (0 days)
  - Time Travel: 0-1 day (default 1 day, can set to 0)
  - Survives session close, persists until explicitly dropped
  - Storage cost: Cheaper than permanent (no fail-safe storage)
  - Use case: ETL intermediate tables, staging tables, data that can be re-created
    Example: Bronze/Silver staging tables in a pipeline

TEMPORARY TABLES:
  - Created with: CREATE TEMPORARY TABLE
  - Fail-safe: NO fail-safe
  - Time Travel: 0-1 day (default 1 day)
  - Visible ONLY to the session that created them
  - Automatically dropped when session ends (connection closed)
  - Storage cost: Cheapest (no fail-safe, auto-cleaned)
  - Use case: Session-specific calculations, debugging, ad-hoc analysis
    Example: Temporary transformations during a data exploration session

COMPARISON TABLE:

  Feature          | Permanent | Transient | Temporary
  -----------------|-----------|-----------|----------
  Fail-safe        | 7 days    | None      | None
  Time Travel      | Up to 90d | 0-1 day   | 0-1 day
  Session-scoped   | No        | No        | Yes (auto-drop on session end)
  Visible to others| Yes       | Yes       | No (only creating session)
  Storage cost     | Highest   | Lower     | Lowest (auto-cleaned)
  Best for         | Production| ETL staging| Ad-hoc/debug

COST IMPLICATIONS:
  - Permanent: Pay for data + fail-safe storage (7 days extra after TTL)
  - Transient: Pay only for data storage (no fail-safe)
  - Temporary: Pay only while session is active (auto-dropped → no ongoing cost)

BEST PRACTICES:
  - Production fact/dim tables → PERMANENT
  - ETL staging, intermediate results → TRANSIENT
  - Debugging, session-specific work → TEMPORARY
  - Set data retention deliberately: short TTL for transient, longer for permanent
"""

print("See comments for full comparison.")

# COMMAND ----------

# DBTITLE 1,Day 1 Complete
# MAGIC %md
# MAGIC ---
# MAGIC ## ✅ Day 1 Complete!
# MAGIC
# MAGIC **14 questions covered across 7 categories.**
# MAGIC
# MAGIC ### Score Yourself:
# MAGIC | Category | Questions | Your Score (0-2) |
# MAGIC |----------|-----------|-----------------|
# MAGIC | SQL Advanced | 2 | / 2 |
# MAGIC | Python | 2 | / 2 |
# MAGIC | PySpark | 2 | / 2 |
# MAGIC | Spark Optimization | 2 | / 2 |
# MAGIC | ETL | 2 | / 2 |
# MAGIC | Data Modeling | 2 | / 2 |
# MAGIC | Snowflake | 2 | / 2 |
# MAGIC
# MAGIC **Total: / 14**
# MAGIC
# MAGIC ---
# MAGIC Next day: `day_02` notebook with fresh questions! 🚀