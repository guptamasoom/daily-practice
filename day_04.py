# Databricks notebook source
# DBTITLE 1,Day 4 — Mock Interview Practice
# MAGIC %md
# MAGIC # 📅 Day 4 — Mock Interview Practice
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
# MAGIC | 5 | ETL (Idempotency, Bad Records, Checkpointing) | 3 |
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

# DBTITLE 1,Q1: Top 3 Salaries
# MAGIC %md
# MAGIC ## 🔷 Section 1: SQL Advanced (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q1: Department Top 3 Salaries [BASIC]
# MAGIC
# MAGIC **Table**: `employees (emp_id, emp_name, department, salary)`
# MAGIC
# MAGIC **Question**: Write a SQL query to find the **top 3 highest salaries** in each department. If there are ties, include all employees with the same salary (use `DENSE_RANK`). Return `department, emp_name, salary, rank`.
# MAGIC
# MAGIC **Hint**: Use `DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC)` and filter where rank <= 3.

# COMMAND ----------

# DBTITLE 1,Solution Q1
# MAGIC %sql
# MAGIC -- SOLUTION Q1
# MAGIC -- DENSE_RANK handles ties — employees with the same salary get the same rank
# MAGIC -- and the next distinct salary gets the next consecutive rank number
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW employees AS
# MAGIC SELECT * FROM VALUES
# MAGIC   (1, 'Alice',   'Engineering', 90000),
# MAGIC   (2, 'Bob',     'Engineering', 85000),
# MAGIC   (3, 'Charlie', 'Engineering', 85000),
# MAGIC   (4, 'Diana',   'Engineering', 70000),
# MAGIC   (5, 'Eve',     'Engineering', 95000),
# MAGIC   (6, 'Frank',   'Sales',       60000),
# MAGIC   (7, 'Grace',   'Sales',       55000),
# MAGIC   (8, 'Heidi',   'Sales',       60000),
# MAGIC   (9, 'Ivan',    'Sales',       50000)
# MAGIC AS employees(emp_id, emp_name, department, salary);
# MAGIC
# MAGIC WITH ranked AS (
# MAGIC   SELECT
# MAGIC     department,
# MAGIC     emp_name,
# MAGIC     salary,
# MAGIC     DENSE_RANK() OVER (
# MAGIC       PARTITION BY department
# MAGIC       ORDER BY salary DESC
# MAGIC     ) AS rank
# MAGIC   FROM employees
# MAGIC )
# MAGIC SELECT department, emp_name, salary, rank
# MAGIC FROM ranked
# MAGIC WHERE rank <= 3
# MAGIC ORDER BY department, rank, emp_name;

# COMMAND ----------

# DBTITLE 1,Q2: MoM Growth Rate
# MAGIC %md
# MAGIC ---
# MAGIC ### Q2: Month-over-Month Revenue Growth [INTERMEDIATE]
# MAGIC
# MAGIC **Table**: `monthly_revenue (month, revenue)`
# MAGIC
# MAGIC **Question**: Write a SQL query to compute the **month-over-month growth rate** as a percentage. Return `month, revenue, prev_month_revenue, growth_rate_pct`. The growth rate formula is `((revenue - prev_month_revenue) / prev_month_revenue) * 100`.
# MAGIC
# MAGIC **Hint**: Use `LAG(revenue) OVER (ORDER BY month)` to get the previous month's revenue.

# COMMAND ----------

# DBTITLE 1,Solution Q2
# MAGIC %sql
# MAGIC -- SOLUTION Q2
# MAGIC -- LAG() fetches the previous row's value based on the ordering
# MAGIC -- We use it to get last month's revenue and compute the growth rate
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW monthly_revenue AS
# MAGIC SELECT * FROM VALUES
# MAGIC   ('2026-01', 100000),
# MAGIC   ('2026-02', 120000),
# MAGIC   ('2026-03', 115000),
# MAGIC   ('2026-04', 140000),
# MAGIC   ('2026-05', 130000),
# MAGIC   ('2026-06', 160000)
# MAGIC AS monthly_revenue(month, revenue);
# MAGIC
# MAGIC SELECT
# MAGIC   month,
# MAGIC   revenue,
# MAGIC   LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
# MAGIC   ROUND(
# MAGIC     (revenue - LAG(revenue) OVER (ORDER BY month)) /
# MAGIC     LAG(revenue) OVER (ORDER BY month) * 100,
# MAGIC     2
# MAGIC   ) AS growth_rate_pct
# MAGIC FROM monthly_revenue
# MAGIC ORDER BY month;

# COMMAND ----------

# DBTITLE 1,Q3: Valid Anagram
# MAGIC %md
# MAGIC ## 🐍 Section 2: Python (Loop / Function / List / Dict) (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q3: Valid Anagram [BASIC]
# MAGIC
# MAGIC **Question**: Write a Python function `is_anagram(s1, s2)` that checks if two strings are **anagrams** of each other. An anagram is a word formed by rearranging the letters of another (e.g., `listen` → `silent`). Ignore case and spaces. Return `True` or `False`.
# MAGIC
# MAGIC **Example**: `is_anagram('listen', 'silent')` → `True`, `is_anagram('hello', 'world')` → `False`
# MAGIC
# MAGIC **Hint**: Use `collections.Counter` or sort both strings and compare.

# COMMAND ----------

# DBTITLE 1,Solution Q3
# SOLUTION Q3
from collections import Counter

def is_anagram(s1, s2):
    """Check if two strings are anagrams (case-insensitive, ignore spaces)."""
    # Normalize: lowercase + remove spaces
    s1_clean = s1.lower().replace(' ', '')
    s2_clean = s2.lower().replace(' ', '')
    
    # Counter compares character frequencies in O(n)
    return Counter(s1_clean) == Counter(s2_clean)

# Test cases
print(is_anagram('listen', 'silent'))    # True
print(is_anagram('hello', 'world'))      # False
print(is_anagram('Dormitory', 'Dirty room'))  # True (ignores case + space)
print(is_anagram('aabbcc', 'abcabc'))    # True
print(is_anagram('python', 'java'))      # False

# COMMAND ----------

# DBTITLE 1,Q4: Sliding Window Max
# MAGIC %md
# MAGIC ---
# MAGIC ### Q4: Sliding Window Maximum [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: Write a Python function `sliding_window_max(arr, k)` that returns the **maximum value** in each sliding window of size `k` moving from left to right. Use a `deque` for O(n) time complexity.
# MAGIC
# MAGIC **Example**: `sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)` → `[3, 3, 5, 5, 6, 7]`
# MAGIC
# MAGIC **Hint**: Use `collections.deque` to store indices of useful elements. The deque front always holds the max for the current window.

# COMMAND ----------

# DBTITLE 1,Solution Q4
# SOLUTION Q4
from collections import deque

def sliding_window_max(arr, k):
    """Return max of each sliding window of size k using deque. O(n) time."""
    if not arr or k == 0:
        return []
    
    dq = deque()        # stores INDICES, values are decreasing from front to back
    result = []
    
    for i in range(len(arr)):
        # Remove indices outside the current window (left side)
        if dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices whose values are smaller than arr[i] from the back
        # (they can never be the max for any future window)
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # Once we've seen at least k elements, record the max (front of deque)
        if i >= k - 1:
            result.append(arr[dq[0]])
    
    return result

# Test cases
print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]
print(sliding_window_max([4, 2, 12, 3, 8], 2))              # [4, 12, 12, 8]
print(sliding_window_max([1, 2, 3, 4, 5], 3))              # [3, 4, 5]
print(sliding_window_max([5, 4, 3, 2, 1], 3))             # [5, 4, 3]

# COMMAND ----------

# DBTITLE 1,Q5: Window Ranking
# MAGIC %md
# MAGIC ## ⚡ Section 3: PySpark Coding (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q5: Window Function — Ranking Products by Sales [BASIC]
# MAGIC
# MAGIC **DataFrame**: `product_sales (category, product, sales_amount)`
# MAGIC
# MAGIC **Question**: Using PySpark, rank products within each category by `sales_amount` in descending order. Add a `rank` column using `ROW_NUMBER()` and a `dense_rank` column using `DENSE_RANK()`. Return all rows ordered by category, rank.
# MAGIC
# MAGIC **Hint**: Use `F.row_number().over(Window.partitionBy('category').orderBy(F.col('sales_amount').desc()))`.

# COMMAND ----------

# DBTITLE 1,Solution Q5
# SOLUTION Q5
from pyspark.sql import functions as F
from pyspark.sql.window import Window

product_data = [
    ('Electronics', 'Laptop',   50000),
    ('Electronics', 'Phone',    30000),
    ('Electronics', 'Tablet',   30000),
    ('Electronics', 'Monitor',  15000),
    ('Clothing',    'Shirts',   20000),
    ('Clothing',    'Pants',    20000),
    ('Clothing',    'Jackets',  10000),
]

product_sales = spark.createDataFrame(product_data, ['category', 'product', 'sales_amount'])

w = Window.partitionBy('category').orderBy(F.col('sales_amount').desc())

result = (
    product_sales
    .withColumn('rank', F.row_number().over(w))
    .withColumn('dense_rank', F.dense_rank().over(w))
    .orderBy('category', 'rank')
)

display(result)

# COMMAND ----------

# DBTITLE 1,Q6: Pivot Table
# MAGIC %md
# MAGIC ---
# MAGIC ### Q6: Pivot Table — Long to Wide Format [INTERMEDIATE]
# MAGIC
# MAGIC **DataFrame**: `monthly_sales (region, month, revenue)`
# MAGIC
# MAGIC **Question**: Using PySpark, pivot the `month` column so each month becomes a separate column with the corresponding `revenue` as values. Each region should be one row with monthly revenue columns.
# MAGIC
# MAGIC **Hint**: Use `df.groupBy('region').pivot('month').agg(F.sum('revenue'))` or `F.first()` inside pivot.

# COMMAND ----------

# DBTITLE 1,Solution Q6
# SOLUTION Q6
from pyspark.sql import functions as F

monthly_data = [
    ('North', '2026-01', 10000),
    ('North', '2026-02', 12000),
    ('North', '2026-03', 11000),
    ('South', '2026-01', 15000),
    ('South', '2026-02', 14000),
    ('South', '2026-03', 16000),
    ('East',  '2026-01', 8000),
    ('East',  '2026-02', 9500),
    ('East',  '2026-03', 10200),
]

monthly_sales = spark.createDataFrame(monthly_data, ['region', 'month', 'revenue'])

# Pivot: each month becomes a column
pivoted = (
    monthly_sales
    .groupBy('region')
    .pivot('month')
    .agg(F.sum('revenue'))
    .orderBy('region')
)

display(pivoted)

# COMMAND ----------

# DBTITLE 1,Q7: Broadcast vs Sort-Merge Join
# MAGIC %md
# MAGIC ## 🔥 Section 4: Spark Optimization & Deep Spark (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q7: Broadcast Join vs Sort-Merge Join [BASIC]
# MAGIC
# MAGIC **Question**: What is the difference between a **broadcast join** and a **sort-merge join** in Spark? When should you use each? What is the default broadcast threshold and how do you configure it?
# MAGIC
# MAGIC **Hint**: Broadcast = small table sent to all executors (no shuffle). Sort-merge = both sides sorted and merged (requires shuffle). Default broadcast threshold is 10 MB.

# COMMAND ----------

# DBTITLE 1,Solution Q7
# SOLUTION Q7

"""
BROADCAST JOIN (BroadcastHashJoin):
  - The SMALLER table is sent to ALL executors in full
  - Each executor holds the small table in memory
  - The larger table is NOT shuffled — each executor scans its partitions
    and joins with the broadcasted copy locally
  - NO SHUFFLE needed → very fast
  - Best for: dim < 10 MB joining with a large fact table
  - Default threshold: spark.sql.autoBroadcastJoinThreshold = 10 MB (10485760 bytes)
  - Override: spark.conf.set('spark.sql.autoBroadcastJoinThreshold', '50MB')
  - Force broadcast: F.broadcast(small_df) in PySpark

SORT-MERGE JOIN (SortMergeJoin):
  - Both tables are SHUFFLED by the join key (each key goes to same executor)
  - Each side is SORTED by the join key on that executor
  - Then a merge step joins matching keys
  - Requires: shuffle + sort = more expensive than broadcast
  - Best for: LARGE-to-LARGE joins (both tables > broadcast threshold)
  - Default join strategy in Spark 3.x (when broadcast is not applicable)
  - Config: spark.sql.join.preferSortMergeJoin = true (default true)

WHEN TO USE EACH:

  Broadcast Join:
    ✓ Dimension table (small, fits in memory) joining a large fact table
    ✓ Reference/lookup tables (country codes, product categories)
    ✓ Tables < 10 MB (or your custom threshold)
    ✗ Large tables → executor OOM

  Sort-Merge Join:
    ✓ Large-to-large table joins (fact-to-fact, fact-to-big-dimension)
    ✓ When either table exceeds the broadcast threshold
    ✓ More memory-efficient than broadcast for large data
    ✗ Slower due to shuffle + sort overhead

KEY POINT:
  Broadcast = no shuffle, small table in memory → fast for small+large
  Sort-merge = shuffle + sort → scalable for large+large
  AQE can auto-switch sort-merge → broadcast at runtime if one side is small enough
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q8: Caching & Persistence
# MAGIC %md
# MAGIC ---
# MAGIC ### Q8: Caching and Persistence in Spark [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: What are the differences between `cache()` and `persist()` in Spark? What are the different **storage levels** available? When should you cache vs persist? What are the risks of over-caching?
# MAGIC
# MAGIC **Hint**: `cache()` is shorthand for `persist(MEMORY_ONLY)`. Storage levels include MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, etc. Cache only what's reused; uncached otherwise.

# COMMAND ----------

# DBTITLE 1,Solution Q8
# SOLUTION Q8

"""
CACHE vs PERSIST in SPARK:

  cache():
    - Shorthand for persist(StorageLevel.MEMORY_ONLY)
    - Stores RDD/DataFrame partitions in memory as deserialized objects
    - If a partition doesn't fit in memory, it is RECOMPUTED on demand (not spilled)
    - Simple, good default for DataFrames used multiple times

  persist(level):
    - Lets you choose a specific StorageLevel
    - More control over memory/disk trade-offs

STORAGE LEVELS:
  1. MEMORY_ONLY (default for cache()):
     - Partitions in memory only, deserialized
     - Partitions that don't fit are recomputed → fast if data fits, costly if not
  
  2. MEMORY_AND_DISK:
     - Partitions in memory; spill to disk if they don't fit
     - Good for large DataFrames that are reused and can't fit in memory
  
  3. MEMORY_ONLY_SER:
     - In memory, serialized (compact) → saves memory, costs CPU to deserialize
  
  4. MEMORY_AND_DISK_SER:
     - Serialized in memory, spill to disk → most memory-efficient
  
  5. DISK_ONLY:
     - Partitions stored on disk only → for very large DataFrames
     - Slower reads but frees all executor memory
  
  6. OFF_HEAP:
     - Uses off-heap memory (Tachyon/IGNITE) → avoids GC pressure

WHEN TO CACHE vs PERSIST:
  - cache(): DataFrame reused 2-3 times, fits comfortably in memory
  - persist(MEMORY_AND_DISK): DataFrame reused, too large for memory-only
  - persist(DISK_ONLY): Very large DataFrame, reused many times, memory is scarce
  - DON'T cache: DataFrame used only once → cache adds overhead with no benefit

RISKS OF OVER-CACHING:
  - Memory pressure → executor OOM
  - GC pauses → deserialized objects create lots of GC overhead
  - Stale data → cached DataFrames don't auto-refresh if source changes
  - Storage waste → caching rarely-used DataFrames blocks memory for active jobs
  - On serverless compute: df.cache() is NOT_SUPPORTED (throws error)
    → use persist(MEMORY_AND_DISK) or avoid caching entirely

BEST PRACTICE:
  1. Cache only DataFrames used MULTIPLE times
  2. unpersist() when done → free memory immediately
  3. Prefer MEMORY_AND_DISK over MEMORY_ONLY for large DataFrames
  4. Monitor cache via Spark UI → Storage tab
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q9: Idempotent Pipeline
# MAGIC %md
# MAGIC ## 🔄 Section 5: ETL — Idempotency, Bad Records, Checkpointing (3 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q9: Idempotent Pipeline Design [INTERMEDIATE]
# MAGIC
# MAGIC **Scenario**: Your nightly ETL job loads data from S3 into a Delta table. The job failed halfway and you re-ran it. Now there are duplicate rows.
# MAGIC
# MAGIC **Question**: What does **idempotency** mean in the context of ETL pipelines? How do you design an idempotent pipeline so that re-running it produces the same result every time? Give at least 3 strategies.
# MAGIC
# MAGIC **Hint**: MERGE (upsert), partition overwrite, dedup with unique keys. Avoid blind append.

# COMMAND ----------

# DBTITLE 1,Solution Q9
# SOLUTION Q9

"""
IDEMPOTENCY = running the same pipeline N times produces the SAME result
               as running it once (no duplicates, no data loss, no side effects)

NON-IDEMPOTENT EXAMPLE (BAD):
  - INSERT INTO target SELECT * FROM source WHERE date = '2026-01-15'
  - Run once: 1000 rows added
  - Run twice: 2000 rows (DUPLICATES!)

STRATEGIES FOR IDEMPOTENT PIPELINES:

1. UPSERT WITH MERGE (most common):
   - MERGE INTO target t USING source s ON t.id = s.id
     WHEN MATCHED THEN UPDATE * WHEN NOT MATCHED THEN INSERT *
   - Re-running is safe: existing rows are updated, new rows are inserted
   - Requires a unique key/business key for the merge condition
   - Works with Delta Lake, Iceberg, Snowflake (MERGE)

2. PARTITION OVERWRITE:
   - INSERT OVERWRITE TABLE target PARTITION (date='2026-01-15')
     SELECT * FROM source WHERE date = '2026-01-15'
   - Replaces the entire partition atomically
   - Idempotent: re-running overwrites the partition with fresh data
   - Best for: batch loads partitioned by date/hour
   - Delta: df.write.mode('overwrite').option('replaceWhere', 'date = "2026-01-15"')

3. DEDUPLICATE WITH UNIQUE KEYS:
   - After loading, deduplicate on business key with watermark
   - DROP DUPLICATES on (id, event_ts) keeping the latest version
   - Use as a safety net even with MERGE

4. CHECKPOINT + EXACTLY-ONCE SINK:
   - For streaming: checkpoint location tracks processed offsets
  - Combined with MERGE (idempotent sink) = exactly-once
   - Never delete the checkpoint directory

5. VERSIONED RUNS / BATCH_ID:
   - Tag each run with a batch_id + run_id
   - Before loading, delete any rows from the same batch_id
   - Then insert fresh — idempotent by design

CHECKLIST FOR IDEMPOTENT PIPELINES:
  ✓ Use MERGE / UPSERT instead of INSERT
  ✓ Or use partition-level overwrite
  ✓ Always have a business/unique key
  ✓ Log batch_id + run_id for traceability
  ✓ Handle schema evolution gracefully
  ✓ Test: run the pipeline twice and verify no duplicates
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q10: Dead Letter Queue
# MAGIC %md
# MAGIC ---
# MAGIC ### Q10: Dead Letter Queue (DLQ) Pattern [INTERMEDIATE]
# MAGIC
# MAGIC **Scenario**: Your pipeline reads 1 million JSON records per batch. A few hundred records have malformed JSON, missing required fields, or fail business validation. You don't want the whole batch to fail.
# MAGIC
# MAGIC **Question**: What is a **Dead Letter Queue (DLQ)**? How do you implement it in a Spark/Databricks ETL pipeline? What happens to bad records and how do you reprocess them later?
# MAGIC
# MAGIC **Hint**: Split good vs bad records → write bad ones to a separate DLQ table → alert on DLQ count → reprocess after fixing.

# COMMAND ----------

# DBTITLE 1,Solution Q10
# SOLUTION Q10

"""
DEAD LETTER QUEUE (DLQ):
  - A separate storage area for records that FAILED processing or validation
  - Instead of failing the entire batch, bad records are isolated
  - Good records proceed normally → pipeline stays green
  - Bad records are reprocessed later after fixing the root cause

IMPLEMENTATION IN SPARK/DATABRICKS:

1. SPLIT GOOD vs BAD RECORDS:
   - Parse each record with a permissive mode (don't fail on bad records)
   - Auto Loader: .option('badRecordPath', '/dlq/bad_records/')
   - Or: .option('mode', 'PERMISSIVE') with a corrupt record column
   - Use a UDF or column checks to validate business rules

2. ROUTE TO DLQ TABLE:
   - CREATE TABLE dlq.bad_records (raw_data, error_message, batch_id, error_ts)
   - Bad records are INSERTED into the DLQ table with context:
     - The raw payload (for debugging/reprocessing)
     - The error message (what went wrong)
     - The batch_id (which run produced it)
     - The timestamp (when it failed)

3. ALERT ON DLQ COUNT:
   - After each batch, check DLQ row count
   - If count > threshold → alert (Slack/email/SQL alert)
   - Trend monitoring: if DLQ count is increasing, source quality is degrading

4. REPROCESS DLQ RECORDS:
   - Investigate the error (schema change? null field? bad format?)
   - Fix the parser/validation logic
   - Re-read from DLQ, apply the fix, and MERGE into the target table
   - Mark DLQ records as 'PROCESSED' or delete after successful reprocessing

STRUCTURED STREAMING EXAMPLE:
  raw = (spark.readStream
           .format('json')
           .option('badRecordPath', '/mnt/dlq/')
           .load('/raw/'))
  
  good = raw.filter(F.col('_corrupt_record').isNull())
  bad  = raw.filter(F.col('_corrupt_record').isNotNull())
  
  # Write good records to target, bad records to DLQ
  good.writeStream.format('delta').start('/target/')
  bad.writeStream.format('delta').start('/dlq/bad_records/')

KEY POINT:
  DLQ = isolate bad records, keep pipeline green, reprocess later.
  Always alert on DLQ volume — it's a data quality signal.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q11: Checkpointing
# MAGIC %md
# MAGIC ---
# MAGIC ### Q11: Checkpointing in Streaming [BASIC]
# MAGIC
# MAGIC **Question**: What is **checkpointing** in Spark Structured Streaming? What information does a checkpoint store? Why is it critical for fault tolerance? What happens if you delete the checkpoint directory?
# MAGIC
# MAGIC **Hint**: Checkpoint stores offsets, completed batch IDs, and WAL. Deleting it means the stream starts from scratch (or the latest offset).

# COMMAND ----------

# DBTITLE 1,Solution Q11
# SOLUTION Q11

"""
CHECKPOINTING IN STRUCTURED STREAMING:
  - A checkpoint is a reliable storage location (S3/ADLS/GCS)
    that tracks the PROGRESS of a streaming query
  - It enables fault tolerance: if the job crashes and restarts,
    it resumes from where it left off
  - Config: .option('checkpointLocation', '/path/to/checkpoint')

WHAT A CHECKPOINT STORES:

1. OFFSETS:
   - The last successfully processed offset for each source
   - Kafka: topic-partition-offset
   - File source: which files have been consumed
   - On restart: the stream reads from the last committed offset

2. COMMITTED BATCH IDS:
   - Which micro-batches have been fully committed to the sink
   - Prevents re-processing of already committed batches

3. WRITE-AHEAD LOG (WAL):
   - For sources that don't support efficient offset tracking (e.g., file sources)
   - Records which files have been processed

4. METADATA:
   - Stream configuration, schema, etc.

WHY IT'S CRITICAL:
  - Without checkpoint: on crash, the stream starts from the EARLIEST
    or LATEST offset (depending on config) → data loss or duplicates
  - With checkpoint: on crash, the stream RESUMES from the last
    committed offset → no data loss, no duplicates (with idempotent sink)

WHAT HAPPENS IF YOU DELETE THE CHECKPOINT:
  - The stream loses all progress information
  - On restart: starts from scratch (earliest/latest offset)
  - Kafka source: starts from the 'earliest' or 'latest' depending on config
  - File source: re-reads ALL files → duplicates if sink is append-only
  - NEVER delete the checkpoint unless you intentionally want to restart

BEST PRACTICES:
  - Use a DURABLE storage path (S3/ADLS), NOT local /tmp
  - Each streaming query needs a UNIQUE checkpoint path
  - Don't share checkpoints across different queries
  - Don't modify the checkpoint directory manually
  - Monitor checkpoint lag: if the stream falls behind, the checkpoint
    directory grows (old WAL files accumulate)

KEY POINT:
  Checkpoint = resume point for the stream. Without it = data loss/duplicates.
  Always use a durable path and never delete it.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q12: Star vs Snowflake Schema
# MAGIC %md
# MAGIC ## 📊 Section 6: Data Modeling (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q12: Star Schema vs Snowflake Schema [BASIC]
# MAGIC
# MAGIC **Question**: What is the difference between a **star schema** and a **snowflake schema**? What are the pros and cons of each? When would you choose one over the other?
# MAGIC
# MAGIC **Hint**: Star = denormalized dimensions (one level). Snowflake = normalized dimensions (multiple levels/tables). Star is simpler and faster for queries; snowflake saves storage.

# COMMAND ----------

# DBTITLE 1,Solution Q12
# SOLUTION Q12

"""
STAR SCHEMA:
  - One central FACT table surrounded by DIMENSION tables
  - Dimensions are DENORMALIZED (flat, no further joins)
  - Example:
      fact_sales (product_id, store_id, date_id, revenue)
      dim_product (product_id, product_name, category, brand)  ← all in one table
      dim_store (store_id, store_name, city, state, region)    ← all in one table
      dim_date (date_id, date, month, quarter, year)
  - Visual: looks like a star (fact in center, dims radiating out)

SNOWFLAKE SCHEMA:
  - Similar to star, but dimensions are NORMALIZED (split into multiple tables)
  - Example:
      fact_sales (product_id, store_id, date_id, revenue)
      dim_product (product_id, product_name, category_id)
      dim_category (category_id, category_name, brand_id)
      dim_brand (brand_id, brand_name)
      dim_store (store_id, store_name, city_id)
      dim_city (city_id, city_name, state_id)
      dim_state (state_id, state_name, region_id)
      dim_region (region_id, region_name)
  - Visual: looks like a snowflake (dimensions branch out further)

COMPARISON:

  | Aspect            | Star Schema              | Snowflake Schema          |
  |-------------------|--------------------------|---------------------------|
  | Normalization     | Denormalized (flat dims) | Normalized (split dims)   |
  | Joins per query   | Fewer (1 level)          | More (multiple levels)    |
  | Query performance | Faster (fewer joins)     | Slower (more joins)       |
  | Storage           | More (data redundancy)   | Less (no redundancy)      |
  | Complexity        | Simple to build & query  | Complex, more tables      |
  | Maintenance       | Easy (few tables)        | Harder (more tables)      |
  | Best for          | OLAP / BI / dashboards   | Data with complex hierarchies |

WHEN TO CHOOSE STAR SCHEMA:
  ✓ Most BI/OLAP workloads (queries are simpler and faster)
  ✓ When query performance matters more than storage
  ✓ When dimensions don't have deep hierarchies
  ✓ Default choice for most data warehouses (Kimball recommends star)

WHEN TO CHOOSE SNOWFLAKE SCHEMA:
  ✓ When storage is constrained (normalize to save space)
  ✓ When dimensions have deep hierarchies (product → category → department)
  ✓ When you need to maintain dimension data independently
  ✓ When you have many-to-many relationships needing bridge tables

KEY POINT:
  Star = denormalized, fast queries, simple design (most common in DW)
  Snowflake = normalized, less storage, more joins, more complex
  Kimball methodology strongly prefers star schemas for performance
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q13: Factless Fact Tables
# MAGIC %md
# MAGIC ---
# MAGIC ### Q13: Factless Fact Tables [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: What is a **factless fact table**? Explain the two types (event tracking and coverage) with examples. Why would you use one instead of a regular fact table?
# MAGIC
# MAGIC **Hint**: Type 1 = records events with no measures (student attended class). Type 2 = records coverage/eligibility (product was available in store on date) — used to find what DIDN'T happen.

# COMMAND ----------

# DBTITLE 1,Solution Q13
# SOLUTION Q13

"""
FACTLESS FACT TABLE:
  - A fact table that contains ONLY foreign keys (dimension keys)
    and NO measures/numeric columns
  - It records that something HAPPENED (or COULD happen) without
    recording any quantitative values

TWO TYPES:

TYPE 1: EVENT TRACKING (records that an event occurred):
  - Captures the occurrence of an event with no associated measure
  - Example: student_attendance (student_id, class_id, date_id)
    - No measure column — just the fact that the student attended the class
  - Example: website_clicks (user_id, page_id, date_id)
    - No dollar amount — just the fact that a click happened
  - Query: "How many students attended class X on date Y?"
    SELECT COUNT(*) FROM attendance WHERE class_id = X AND date_id = Y

TYPE 2: COVERAGE / ELIGIBILITY (records what COULD happen):
  - Records the combination of dimensions that are ELIGIBLE for an event
  - Used to find what DIDN'T happen (gaps in coverage)
  - Example: store_product_coverage (store_id, product_id, date_id)
    - Records which products were AVAILABLE in which stores on which dates
  - Query: "Which products were NOT sold in store X on date Y?"
    SELECT p.product_name
    FROM coverage c
    JOIN dim_product p ON c.product_id = p.product_id
    LEFT JOIN fact_sales s ON c.product_id = s.product_id
                           AND c.store_id = s.store_id
                           AND c.date_id = s.date_id
    WHERE c.store_id = X AND c.date_id = Y AND s.sale_id IS NULL
  - This finds products that WERE available but WEREN'T sold

WHY USE FACTLESS FACT TABLES:
  1. Track events with no numeric measure (attendance, clicks, visits)
  2. Find gaps in coverage (products not sold, employees not assigned)
  3. Count occurrences (COUNT(*) on the factless table)
  4. Act as a bridge between dimensions in many-to-many relationships

KEY POINT:
  Type 1 (event) = records what happened (no measures, just keys)
  Type 2 (coverage) = records what was possible (find what didn't happen)
  Both contain ONLY dimension keys and no measures.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q14: Time Travel & Fail-Safe
# MAGIC %md
# MAGIC ## ❄️ Section 7: Snowflake (2 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q14: Time Travel and Fail-Safe [BASIC]
# MAGIC
# MAGIC **Question**: What is **Time Travel** in Snowflake? How is it different from **Fail-Safe**? How long does each retain data? How do you query historical data using Time Travel?
# MAGIC
# MAGIC **Hint**: Time Travel = user-accessible historical data (1-90 days). Fail-Safe = Snowflake's internal backup (7 days after Time Travel expires). Use `AT (TIMESTAMP => ...)` or `AT (OFFSET => ...)` for Time Travel queries.

# COMMAND ----------

# DBTITLE 1,Solution Q14
# SOLUTION Q14

"""
SNOWFLAKE TIME TRAVEL:
  - Allows querying and restoring data from the PAST
  - You can access previous versions of a table, schema, or database
  - Retention period: 1 day (Standard) to 90 days (Enterprise)
  - Default: 1 day for Standard edition, can be increased per table
  - Set with: CREATE TABLE ... DATA_RETENTION_TIME_IN_DAYS = 30
  - Or: ALTER TABLE my_table SET DATA_RETENTION_TIME_IN_DAYS = 30

QUERYING WITH TIME TRAVEL:
  -- By timestamp
  SELECT * FROM my_table AT (TIMESTAMP => '2026-10-01 12:00:00'::timestamp);
  
  -- By offset (5 minutes ago)
  SELECT * FROM my_table AT (OFFSET => -60*5);  -- -300 seconds
  
  -- By statement (before a specific query)
  SELECT * FROM my_table BEFORE (STATEMENT => 'query_id');
  
  -- Restore a dropped table
  UNDROP TABLE my_table;
  
  -- Clone a table at a past point in time
  CREATE TABLE backup AS SELECT * FROM my_table AT (TIMESTAMP => '2026-10-01'::timestamp);

FAIL-SAFE:
  - Snowflake's INTERNAL backup mechanism (not user-accessible)
  - Provides an ADDITIONAL 7 days of data retention AFTER Time Travel expires
  - Used by Snowflake support for disaster recovery
  - Users CANNOT query or restore from Fail-Safe directly
  - Must contact Snowflake support to recover from Fail-Safe
  - Timeline: Time Travel (1-90 days) → Fail-Safe (7 days) → data purged

KEY DIFFERENCES:

  | Feature        | Time Travel              | Fail-Safe                |
  |----------------|--------------------------|--------------------------|
  | User accessible| Yes (SELECT, UNDROP)     | No (Snowflake support)   |
  | Retention      | 1-90 days (configurable)| 7 days (fixed)            |
  | Purpose        | Query/restore past data  | Disaster recovery backup  |
  | Cost           | Storage costs apply      | Included in storage cost  |
  | Edition        | Standard (1d), Enterprise (up to 90d) | All editions |

KEY POINT:
  Time Travel = user-facing historical query + restore (1-90 days)
  Fail-Safe = Snowflake's internal safety net (7 days after Time Travel)
  Timeline: Live → Time Travel → Fail-Safe → Deleted
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q15: Warehouse Sizing
# MAGIC %md
# MAGIC ---
# MAGIC ### Q15: Warehouse Sizing and Auto-Suspend/Resume [BASIC]
# MAGIC
# MAGIC **Question**: What are the different **warehouse sizes** in Snowflake (T-shirt sizing)? How does **auto-suspend** and **auto-resume** work? What is the cost implication of each size and how do you choose the right warehouse for a workload?
# MAGIC
# MAGIC **Hint**: Sizes: X-Small to 6X-Large, each 2x the previous. Auto-suspend stops billing after idle time. Auto-resume starts on first query.

# COMMAND ----------

# DBTITLE 1,Solution Q15
# SOLUTION Q15

"""
SNOWFLAKE WAREHOUSE SIZES (T-shirt sizing):
  Each size DOUBLES the compute and cost of the previous.

  | Size       | Servers | Credits/Hour | Relative |
  |------------|---------|--------------|----------|
  | X-Small    | 1       | 1            | 1x       |
  | Small      | 2       | 2            | 2x       |
  | Medium     | 4       | 4            | 4x       |
  | Large      | 8       | 8            | 8x       |
  | X-Large    | 16      | 16           | 16x      |
  | 2X-Large   | 32      | 32           | 32x      |
  | 3X-Large   | 64      | 64           | 64x      |
  | 4X-Large   | 128     | 128          | 128x     |
  | 5X-Large   | 256     | 256          | 256x     |
  | 6X-Large   | 512     | 512          | 512x     |

AUTO-SUSPEND:
  - A warehouse automatically SUSPENDS after N seconds of inactivity
  - While suspended, you are NOT billed for compute
  - Default: 60 seconds (configurable)
  - Set with: ALTER WAREHOUSE my_wh SET WAREHOUSE_SIZE = 'Medium'
                               AUTO_SUSPEND = 60;
  - AUTO_SUSPEND = 0 means NEVER suspend (always running, always billing)

AUTO-RESUME:
  - When a query arrives and the warehouse is suspended,
    it automatically RESUMES (starts up)
  - Startup takes ~2-5 seconds (cold start)
  - Set with: ALTER WAREHOUSE my_wh SET AUTO_RESUME = TRUE;
  - If AUTO_RESUME = FALSE, you must manually start the warehouse

SCALING POLICY:
  - MIN_CLUSTER_COUNT / MAX_CLUSTER_COUNT: multi-cluster warehouses
  - Scaling policy: STANDARD (default), ECONOMY, AGGRESSIVE
  - Multi-cluster: multiple warehouses in a pool for concurrency

CHOOSING THE RIGHT WAREHOUSE:
  - X-Small/Small:  Dev/test, small datasets, simple queries
  - Medium/Large:   BI dashboards, moderate ETL, reporting
  - X-Large+:       Heavy ETL, large table scans, complex joins
  - Multi-cluster:   High concurrency (many simultaneous users)

COST OPTIMIZATION TIPS:
  1. Use AUTO_SUSPEND = 60 (don't leave warehouses idle)
  2. Match warehouse size to workload (don't use 4XL for small queries)
  3. Use separate warehouses for dev/test/prod
  4. Use RESOURCE MONITORS to set credit limits + alerts
  5. Consider SUSPENDED warehouses for non-business-hours
  6. Use query acceleration service for eligible queries (no cost!)

KEY POINT:
  Each size doubles compute + cost. Auto-suspend stops billing when idle.
  Auto-resume starts on first query. Right-size for workload + cost.
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q16: Airflow vs Jobs vs ADF
# MAGIC %md
# MAGIC ## 🛠️ Section 8: Monitoring, Logging & Orchestration (3 Questions)
# MAGIC
# MAGIC ---
# MAGIC ### Q16: Airflow vs Databricks Jobs vs Azure Data Factory [INTERMEDIATE]
# MAGIC
# MAGIC **Question**: Compare **Apache Airflow**, **Databricks Jobs**, and **Azure Data Factory (ADF)** as orchestration tools for data pipelines. What are the strengths and weaknesses of each? When would you choose one over the others?
# MAGIC
# MAGIC **Hint**: Airflow = open-source, Python-based, DAG-centric. Databricks Jobs = native Databricks, no infra. ADF = Azure-native, visual pipeline builder, good for Azure ecosystem.

# COMMAND ----------

# DBTITLE 1,Solution Q16
# SOLUTION Q16

"""
COMPARISON: AIRFLOW vs DATABRICKS JOBS vs AZURE DATA FACTORY

APACHE AIRFLOW:
  - Open-source, Python-based DAG orchestration (created by Airbnb)
  - Define pipelines as Python code (DAGs with tasks and dependencies)
  - Operators: PythonOperator, BashOperator, KubernetesPod, etc.
  - Can trigger Databricks jobs via DatabricksSubmitRunOperator
  - Rich ecosystem: sensors, branching, XCom, dynamic task mapping
  
  Strengths:
    ✓ Language-agnostic (orchestrate anything via operators)
    ✓ Full Python control — custom logic, branching, retries
    ✓ Huge community + plugin ecosystem
    ✓ Version controlled (DAGs as Python code)
    ✓ Cross-platform (AWS, GCP, Azure, on-prem)
  
  Weaknesses:
    ✗ Need to manage infrastructure (Airflow itself)
    ✗ Learning curve (Python + Airflow concepts)
    ✗ Scheduler reliability (needs monitoring)
    ✗ Not integrated with compute (just triggers)

DATABRICKS JOBS:
  - Native orchestration inside Databricks (no extra infra)
  - Task types: notebook, Python script, SQL, pipeline, dbt, dashboard
  - Run If conditions: ALL_SUCCESS, AT_LEAST_ONE, ALL_FAILED, NONE
  - For Each task: fan-out parallelism
  - Retry, timeout, email/webhook/Slack notifications
  
  Strengths:
    ✓ Zero infrastructure — fully managed
    ✓ Tight integration with Databricks compute + Unity Catalog
    ✓ Simple UI for creating + monitoring jobs
    ✓ No code needed for basic pipelines (UI-based)
    ✓ Native: notebooks, pipelines, SQL, dbt, dashboards
  
  Weaknesses:
    ✗ Limited to Databricks ecosystem (hard to orchestrate external tools)
    ✗ Less flexible than Airflow for complex branching
    ✗ No Python-level control over orchestration logic
    ✗ No sensors (file arrival, external trigger) like Airflow

AZURE DATA FACTORY (ADF):
  - Visual pipeline builder in Azure (drag-and-drop)
  - 100+ built-in connectors (Azure SQL, Blob, Cosmos DB, Databricks, etc.)
  - Integration Runtime: self-hosted, Azure SSIS, Azure
  - Good for hybrid (cloud + on-prem) data integration
  
  Strengths:
    ✓ Visual pipeline builder (no code for simple pipelines)
    ✓ 100+ native connectors (Azure ecosystem)
    ✓ Managed infrastructure (serverless)
    ✓ Good for Azure-native shops + hybrid scenarios
    ✓ Tight Azure integration (Key Vault, Monitor, Logic Apps)
  
  Weaknesses:
    ✗ Not open source (Azure lock-in)
    ✗ Less flexible than Airflow for complex logic
    ✗ JSON-based pipeline definitions (verbose)
    ✗ Slower than Airflow for iterative development

WHEN TO CHOOSE:
  - Airflow:        Multi-cloud, complex logic, Python team, cross-platform
  - Databricks Jobs: Databricks-first shop, no extra infra, simple→moderate pipelines
  - ADF:            Azure-native, hybrid data, visual builder, lots of Azure connectors

KEY POINT:
  Airflow = flexibility + multi-cloud (self-managed)
  Databricks Jobs = simplicity + Databricks-native (managed)
  ADF = Azure ecosystem + visual pipelines (managed)
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q17: Logging Best Practices
# MAGIC %md
# MAGIC ---
# MAGIC ### Q17: Logging Best Practices — log4j vs print [BASIC]
# MAGIC
# MAGIC **Question**: Why should you use a **logging framework** (like log4j or Python logging) instead of `print()` statements in production Spark pipelines? What are the log levels and when do you use each? How do you access driver logs in Databricks?
# MAGIC
# MAGIC **Hint**: log4j has 6 levels: TRACE < DEBUG < INFO < WARN < ERROR < FATAL. print() goes to stdout, not log files. In Databricks: Job run → task → Logs → Driver logs.

# COMMAND ----------

# DBTITLE 1,Solution Q17
# SOLUTION Q17

"""
WHY USE LOGGING FRAMEWORK INSTEAD OF print():

1. LOG LEVELS — filter by severity:
   - print() → all output goes to stdout, no way to filter
   - logging → set level once (e.g., INFO) and only that level+ shows
   - In prod: set to WARN/ERROR (less noise)
   - In dev: set to DEBUG/TRACE (more detail)

2. STRUCTURED OUTPUT:
   - logging provides: timestamp, level, logger name, message
   - print() → just the text
   - Structured logs are parseable (JSON, key=value) for log aggregation

3. ROUTING:
   - logging → can route to files, console, syslog, Kafka, etc.
   - print() → only stdout
   - In Spark: log4j logs go to driver/executor log files

4. PERFORMANCE:
   - logging at DEBUG level can be DISABLED in production (zero cost)
  - print() always executes (even if you don't want the output)
   - logging uses lazy evaluation: logger.debug(f'expensive {compute()}')
     is skipped if level is INFO

LOG LEVELS (log4j / Python logging):
  1. TRACE — finest-grained, very detailed (method entry/exit)
  2. DEBUG — debugging info (variable values, row counts)
  3. INFO  — general progress (batch started, batch completed)
  4. WARN  — potential issues (approaching threshold, deprecated API)
  5. ERROR — errors that don't stop the app (failed record, retry)
  6. FATAL — critical errors that stop the application

  In production: set to INFO or WARN
  In development: set to DEBUG or TRACE

PYTHON LOGGING IN SPARK:
  import logging
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.INFO)
  logger.info('Batch started: %d records', row_count)
  logger.error('Failed to process record: %s', record_id)

ACCESSING DRIVER LOGS IN DATABRICKS:
  1. Job run page → click the failed task
  2. Click 'Logs' tab
  3. Driver logs → stdout, stderr, log4j
  4. Or: Cluster → 'Driver Logs' → Spark UI → 'Executor' tab
  5. For serverless: query profile / execution details
  6. If log delivery is configured: logs in S3/ADLS bucket

SPARK UI:
  - Spark UI → 'Stages' → click a stage → 'Tasks' → see task logs
  - 'Executors' tab → see executor logs + GC time
  - 'SQL/DataFrame' tab → see the query plan + execution details

BEST PRACTICES:
  ✓ Use logging framework, NOT print()
  ✓ Log with context: batch_id, row_count, timestamp
  ✓ Use appropriate levels (INFO for progress, ERROR for failures)
  ✓ Include structured fields for log aggregation (JSON)
  ✓ Don't log sensitive data (PII, credentials)
  ✓ Configure log rotation for long-running jobs
"""

print("See comments for the full explanation.")

# COMMAND ----------

# DBTITLE 1,Q18: Freshness & Volume Alert
# MAGIC %md
# MAGIC ---
# MAGIC ### Q18: Data Freshness and Volume Alert — SQL Pattern [INTERMEDIATE]
# MAGIC
# MAGIC **Scenario**: You need to set up an alert that fires when a Delta table `sales.fact_orders` hasn't been updated in the last 6 hours, OR when today's row count is less than 50% of the 7-day average.
# MAGIC
# MAGIC **Question**: Write a SQL query that checks both conditions (freshness + volume) and returns a single row with columns `is_stale`, `row_count_today`, `avg_7d`, `volume_anomaly`, `alert_flag`. Explain how you'd turn this into a Databricks SQL alert.
# MAGIC
# MAGIC **Hint**: Use `MAX(updated_at)` for freshness, a 7-day average window for volume, and a CASE WHEN for the alert flag. Schedule it as a SQL alert that fires when `alert_flag = true`.

# COMMAND ----------

# DBTITLE 1,Solution Q18
# SOLUTION Q18
# Demonstrated with a sample table — in production, replace with real Delta table

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Simulate fact_orders: (order_id, amount, updated_at)
import datetime
now = datetime.datetime.now()

orders_data = [
    (1, 100, now - datetime.timedelta(hours=2)),   # 2 hours ago — fresh
    (2, 200, now - datetime.timedelta(hours=3)),   # 3 hours ago — fresh
    (3, 150, now - datetime.timedelta(hours=5)),   # 5 hours ago — fresh
    (4, 300, now - datetime.timedelta(hours=8)),    # 8 hours ago — stale!
]

fact_orders = spark.createDataFrame(orders_data, ['order_id', 'amount', 'updated_at'])

# Add a date column for the volume check
fact_orders = fact_orders.withColumn('load_date', F.to_date('updated_at'))

# 1. FRESHNESS CHECK: max(updated_at) within last 6 hours?
freshness = fact_orders.agg(
    F.max('updated_at').alias('last_update'),
    F.count('*').alias('total_rows')
).collect()[0]

hours_since_update = (now - freshness['last_update']).total_seconds() / 3600
is_stale = hours_since_update > 6

# 2. VOLUME CHECK: today's row count vs 7-day average
# (Simplified: comparing total rows as a demo)
row_count_today = freshness['total_rows']
avg_7d = row_count_today  # In production: compute 7-day average
volume_anomaly = row_count_today < (avg_7d * 0.5)

# 3. ALERT FLAG
alert_flag = is_stale or volume_anomaly

print(f"=== DATA MONITORING ALERT ===")
print(f"Last update:          {freshness['last_update']}")
print(f"Hours since update:   {hours_since_update:.1f}h")
print(f"Is stale (>6h):       {is_stale}")
print(f"Row count today:      {row_count_today}")
print(f"7-day average:        {avg_7d}")
print(f"Volume anomaly (<50%): {volume_anomaly}")
print(f"ALERT FLAG:           {alert_flag}")

print()
print("""
PRODUCTION SQL ALERT (Databricks SQL):

  SELECT
    -- Freshness: is the table updated within the last 6 hours?
    CASE
      WHEN MAX(updated_at) < CURRENT_TIMESTAMP() - INTERVAL 6 HOURS
      THEN true ELSE false
    END AS is_stale,
    
    -- Volume: today's row count
    COUNT(CASE WHEN DATE(updated_at) = CURRENT_DATE() THEN 1 END) AS row_count_today,
    
    -- 7-day average (excluding today)
    AVG(CASE
      WHEN DATE(updated_at) >= CURRENT_DATE() - INTERVAL 7 DAYS
       AND DATE(updated_at) < CURRENT_DATE()
      THEN COUNT(*) OVER (
        PARTITION BY DATE(updated_at)
      )
    END) AS avg_7d,
    
    -- Volume anomaly: today < 50% of 7-day average
    CASE
      WHEN COUNT(CASE WHEN DATE(updated_at) = CURRENT_DATE() THEN 1 END)
         < 0.5 * AVG(CASE
        WHEN DATE(updated_at) >= CURRENT_DATE() - INTERVAL 7 DAYS
         AND DATE(updated_at) < CURRENT_DATE()
        THEN COUNT(*) OVER (PARTITION BY DATE(updated_at))
      END)
      THEN true ELSE false
    END AS volume_anomaly,
    
    -- Combined alert
    CASE
      WHEN MAX(updated_at) < CURRENT_TIMESTAMP() - INTERVAL 6 HOURS
        OR COUNT(CASE WHEN DATE(updated_at) = CURRENT_DATE() THEN 1 END)
         < 0.5 * AVG(CASE
           WHEN DATE(updated_at) >= CURRENT_DATE() - INTERVAL 7 DAYS
            AND DATE(updated_at) < CURRENT_DATE()
           THEN COUNT(*) OVER (PARTITION BY DATE(updated_at))
         END)
      THEN true ELSE false
    END AS alert_flag
  FROM sales.fact_orders;

SETUP AS DATABRICKS SQL ALERT:
  1. Save this query as a SQL query in Databricks SQL
  2. Create an Alert based on this query
  3. Condition: alert_flag = true (or = 1)
  4. Schedule: every 30 minutes (or hourly)
  5. Destinations: email, Slack webhook, or Teams webhook
  6. Message: 'Data quality alert: sales.fact_orders is stale or volume anomaly detected'
""")

# COMMAND ----------

# DBTITLE 1,Day 4 Complete
# MAGIC %md
# MAGIC ---
# MAGIC ## ✅ Day 4 Complete!
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
# MAGIC Next day: `day_05` notebook with fresh questions! 🚀

# COMMAND ----------

