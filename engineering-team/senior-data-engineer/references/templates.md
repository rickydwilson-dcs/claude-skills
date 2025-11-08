# Data Engineering Templates & Code Examples

Production-ready templates for data pipelines, ETL workflows, SQL queries, and infrastructure code.

## Table of Contents

1. [Airflow DAG Templates](#airflow-dag-templates)
2. [Spark Job Templates](#spark-job-templates)
3. [dbt Model Templates](#dbt-model-templates)
4. [SQL Query Patterns](#sql-query-patterns)
5. [Python Pipeline Templates](#python-pipeline-templates)
6. [Docker & Deployment](#docker--deployment)
7. [Configuration Files](#configuration-files)
8. [Testing Templates](#testing-templates)

---

## Airflow DAG Templates

### Complete ETL DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import logging

# Default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['data-alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(hours=1)
}

# DAG definition
dag = DAG(
    dag_id='sales_etl_pipeline',
    default_args=default_args,
    description='Daily sales data ETL pipeline',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['sales', 'etl', 'production']
)

def extract_from_source(**context):
    """
    Extract data from source system
    """
    from sqlalchemy import create_engine
    import pandas as pd

    execution_date = context['ds']
    logging.info(f"Extracting data for {execution_date}")

    # Database connection
    engine = create_engine(context['var']['value']['source_db_url'])

    # Query with date filter
    query = f"""
    SELECT *
    FROM sales_transactions
    WHERE DATE(transaction_date) = '{execution_date}'
    """

    df = pd.read_sql(query, engine)
    logging.info(f"Extracted {len(df)} rows")

    # Save to staging
    staging_path = f"s3://bucket/staging/sales/{execution_date}.parquet"
    df.to_parquet(staging_path, index=False)

    # Pass metadata to XCom
    return {
        'row_count': len(df),
        'staging_path': staging_path
    }

def transform_data(**context):
    """
    Transform and clean data
    """
    import pandas as pd

    # Get staging path from XCom
    task_instance = context['task_instance']
    extract_result = task_instance.xcom_pull(task_ids='extract_task')
    staging_path = extract_result['staging_path']

    logging.info(f"Transforming data from {staging_path}")

    # Load data
    df = pd.read_parquet(staging_path)

    # Data cleaning
    df = df.dropna(subset=['transaction_id', 'customer_id'])
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['amount'] = df['amount'].astype(float)

    # Business logic transformations
    df['revenue'] = df['amount'] - df['discount']
    df['profit'] = df['revenue'] - df['cost']
    df['profit_margin'] = (df['profit'] / df['revenue'] * 100).round(2)

    # Enrichment
    df['day_of_week'] = df['transaction_date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6])

    # Data quality checks
    assert df['amount'].min() >= 0, "Negative amounts detected"
    assert df['transaction_id'].is_unique, "Duplicate transaction IDs"

    # Save transformed data
    execution_date = context['ds']
    transformed_path = f"s3://bucket/transformed/sales/{execution_date}.parquet"
    df.to_parquet(transformed_path, index=False)

    return {
        'row_count': len(df),
        'transformed_path': transformed_path
    }

def load_to_warehouse(**context):
    """
    Load data to data warehouse
    """
    from snowflake.connector import connect

    task_instance = context['task_instance']
    transform_result = task_instance.xcom_pull(task_ids='transform_task')
    transformed_path = transform_result['transformed_path']

    logging.info(f"Loading data from {transformed_path}")

    # Snowflake connection
    conn = connect(
        user=context['var']['value']['snowflake_user'],
        password=context['var']['value']['snowflake_password'],
        account=context['var']['value']['snowflake_account'],
        warehouse='COMPUTE_WH',
        database='ANALYTICS',
        schema='SALES'
    )

    # Create stage if not exists
    conn.cursor().execute("""
        CREATE STAGE IF NOT EXISTS sales_stage
        URL = 's3://bucket/transformed/sales/'
        CREDENTIALS = (AWS_KEY_ID = '...' AWS_SECRET_KEY = '...')
        FILE_FORMAT = (TYPE = PARQUET)
    """)

    # Copy into table
    execution_date = context['ds']
    conn.cursor().execute(f"""
        COPY INTO sales_fact
        FROM @sales_stage/{execution_date}.parquet
        FILE_FORMAT = (TYPE = PARQUET)
        MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
        ON_ERROR = ABORT_STATEMENT
    """)

    conn.close()
    logging.info("Load completed successfully")

def run_quality_checks(**context):
    """
    Run data quality checks on loaded data
    """
    from snowflake.connector import connect

    execution_date = context['ds']
    conn = connect(...)

    # Row count validation
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM sales_fact
        WHERE DATE(transaction_date) = '{execution_date}'
    """)
    row_count = cursor.fetchone()[0]

    # Get expected count from XCom
    task_instance = context['task_instance']
    extract_result = task_instance.xcom_pull(task_ids='extract_task')
    expected_count = extract_result['row_count']

    # Validate
    assert row_count == expected_count, \
        f"Row count mismatch: expected {expected_count}, got {row_count}"

    # Aggregate validation
    cursor.execute(f"""
        SELECT
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM sales_fact
        WHERE DATE(transaction_date) = '{execution_date}'
    """)
    metrics = cursor.fetchone()

    logging.info(f"Quality checks passed: {metrics}")
    conn.close()

# Task definitions
with dag:
    start = BashOperator(
        task_id='start',
        bash_command='echo "Starting sales ETL pipeline"'
    )

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_from_source,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_to_warehouse,
        provide_context=True
    )

    quality_check_task = PythonOperator(
        task_id='quality_check_task',
        python_callable=run_quality_checks,
        provide_context=True
    )

    end = BashOperator(
        task_id='end',
        bash_command='echo "Pipeline completed successfully"'
    )

    # Task dependencies
    start >> extract_task >> transform_task >> load_task >> quality_check_task >> end
```

### Incremental Load DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def incremental_etl(**context):
    """
    Incremental data loading with watermark tracking
    """
    import pandas as pd
    from sqlalchemy import create_engine

    # Get last watermark
    watermark_query = """
    SELECT MAX(updated_at) as last_updated
    FROM staging.watermarks
    WHERE table_name = 'sales_transactions'
    """

    engine = create_engine(...)
    last_updated = pd.read_sql(watermark_query, engine)['last_updated'][0]

    # Extract incremental changes
    incremental_query = f"""
    SELECT *
    FROM sales_transactions
    WHERE updated_at > '{last_updated}'
    ORDER BY updated_at
    """

    df = pd.read_sql(incremental_query, engine)

    if len(df) == 0:
        logging.info("No new data to process")
        return

    # Transform
    df = transform_sales_data(df)

    # Upsert to target
    df.to_sql(
        name='sales_fact',
        con=engine,
        schema='analytics',
        if_exists='append',
        index=False,
        method='multi',
        chunksize=10000
    )

    # Update watermark
    new_watermark = df['updated_at'].max()
    engine.execute(f"""
        UPDATE staging.watermarks
        SET last_updated = '{new_watermark}',
            updated_at = CURRENT_TIMESTAMP
        WHERE table_name = 'sales_transactions'
    """)

    logging.info(f"Processed {len(df)} rows, new watermark: {new_watermark}")

dag = DAG(
    dag_id='incremental_sales_etl',
    schedule_interval='*/15 * * * *',  # Every 15 minutes
    start_date=datetime(2025, 1, 1),
    catchup=False
)

task = PythonOperator(
    task_id='incremental_load',
    python_callable=incremental_etl,
    provide_context=True,
    dag=dag
)
```

### Dynamic Task Generation DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime

# Get list of tables to process from Airflow Variables
tables_config = Variable.get("etl_tables", deserialize_json=True)

dag = DAG(
    dag_id='multi_table_etl',
    schedule_interval='0 3 * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False
)

def process_table(table_name, **context):
    """Generic table processing function"""
    logging.info(f"Processing table: {table_name}")

    # Extract
    df = extract_table(table_name)

    # Transform
    df = apply_transformations(df, table_name)

    # Load
    load_to_warehouse(df, table_name)

# Dynamically create tasks for each table
for table_config in tables_config:
    table_name = table_config['name']
    dependencies = table_config.get('depends_on', [])

    task = PythonOperator(
        task_id=f'process_{table_name}',
        python_callable=process_table,
        op_kwargs={'table_name': table_name},
        provide_context=True,
        dag=dag
    )
```

---

## Spark Job Templates

### Batch Processing Job

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import sys

def create_spark_session(app_name):
    """Create Spark session with optimized configuration"""
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "200") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .getOrCreate()

def transform_sales_data(spark, input_path, output_path, date):
    """
    Process sales data with complex transformations
    """

    # Read data
    df = spark.read.parquet(input_path)

    # Filter by date
    df = df.filter(col("transaction_date") == date)

    # Data cleaning
    df = df.dropna(subset=["transaction_id", "customer_id"]) \
           .dropDuplicates(["transaction_id"])

    # Type casting
    df = df.withColumn("amount", col("amount").cast("double")) \
           .withColumn("quantity", col("quantity").cast("int"))

    # Business logic transformations
    df = df.withColumn("revenue", col("amount") - col("discount")) \
           .withColumn("profit", col("revenue") - col("cost")) \
           .withColumn("profit_margin",
                      round((col("profit") / col("revenue")) * 100, 2))

    # Date features
    df = df.withColumn("year", year("transaction_date")) \
           .withColumn("month", month("transaction_date")) \
           .withColumn("day_of_week", dayofweek("transaction_date")) \
           .withColumn("is_weekend",
                      when(col("day_of_week").isin([1, 7]), True).otherwise(False))

    # Window functions - customer metrics
    customer_window = Window.partitionBy("customer_id").orderBy("transaction_date")

    df = df.withColumn("customer_transaction_number",
                      row_number().over(customer_window)) \
           .withColumn("customer_lifetime_value",
                      sum("revenue").over(customer_window.rowsBetween(Window.unboundedPreceding, 0))) \
           .withColumn("days_since_last_purchase",
                      datediff(col("transaction_date"),
                              lag("transaction_date").over(customer_window)))

    # Aggregations
    product_agg = df.groupBy("product_id") \
        .agg(
            count("*").alias("transaction_count"),
            sum("quantity").alias("total_quantity"),
            sum("revenue").alias("total_revenue"),
            avg("amount").alias("avg_transaction_value")
        )

    # Join back aggregated metrics
    df = df.join(
        product_agg.withColumnRenamed("product_id", "prod_id"),
        col("product_id") == col("prod_id"),
        "left"
    ).drop("prod_id")

    # Data quality checks
    assert df.filter(col("amount") < 0).count() == 0, "Negative amounts detected"
    assert df.filter(col("transaction_id").isNull()).count() == 0, "Null transaction IDs"

    # Write output partitioned by date
    df.write \
        .mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(output_path)

    # Log metrics
    total_records = df.count()
    total_revenue = df.agg(sum("revenue")).collect()[0][0]

    print(f"Processed {total_records} records")
    print(f"Total revenue: ${total_revenue:,.2f}")

    return total_records, total_revenue

def main():
    """Main execution"""
    if len(sys.argv) < 4:
        print("Usage: spark-submit job.py <input_path> <output_path> <date>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    date = sys.argv[3]

    spark = create_spark_session("Sales Data Processing")

    try:
        transform_sales_data(spark, input_path, output_path, date)
        print("Job completed successfully")
    except Exception as e:
        print(f"Job failed: {str(e)}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

### Streaming Job

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def create_streaming_session():
    return SparkSession.builder \
        .appName("Real-Time Event Processing") \
        .config("spark.sql.streaming.checkpointLocation", "s3://bucket/checkpoints/") \
        .getOrCreate()

def process_event_stream(spark):
    """
    Process real-time events from Kafka
    """

    # Define schema
    event_schema = StructType([
        StructField("event_id", StringType(), False),
        StructField("user_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("timestamp", TimestampType(), False),
        StructField("properties", MapType(StringType(), StringType()), True)
    ])

    # Read from Kafka
    events_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "user_events") \
        .option("startingOffsets", "latest") \
        .load()

    # Parse JSON
    parsed_df = events_df \
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp") \
        .select(
            col("key").alias("partition_key"),
            from_json(col("value"), event_schema).alias("data"),
            col("timestamp").alias("kafka_timestamp")
        ) \
        .select("partition_key", "data.*", "kafka_timestamp")

    # Transformations
    enriched_df = parsed_df \
        .withColumn("processing_timestamp", current_timestamp()) \
        .withColumn("date", to_date("timestamp")) \
        .withColumn("hour", hour("timestamp"))

    # Windowed aggregations
    metrics_df = enriched_df \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
            window("timestamp", "1 minute", "30 seconds"),
            "event_type"
        ) \
        .agg(
            count("*").alias("event_count"),
            countDistinct("user_id").alias("unique_users")
        )

    # Write to Parquet (for batch analytics)
    parquet_query = enriched_df.writeStream \
        .format("parquet") \
        .option("path", "s3://bucket/events/") \
        .option("checkpointLocation", "s3://bucket/checkpoints/events/") \
        .partitionBy("date", "hour") \
        .outputMode("append") \
        .trigger(processingTime="1 minute") \
        .start()

    # Write metrics to console (monitoring)
    console_query = metrics_df.writeStream \
        .format("console") \
        .outputMode("update") \
        .trigger(processingTime="30 seconds") \
        .start()

    # Wait for termination
    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    spark = create_streaming_session()
    process_event_stream(spark)
```

---

## dbt Model Templates

### Staging Model

```sql
-- models/staging/stg_sales_transactions.sql
{{
    config(
        materialized='view',
        tags=['staging', 'sales']
    )
}}

WITH source AS (
    SELECT * FROM {{ source('raw', 'sales_transactions') }}
),

renamed AS (
    SELECT
        -- Primary key
        transaction_id,

        -- Foreign keys
        customer_id,
        product_id,
        store_id,

        -- Timestamps
        transaction_date::timestamp AS transaction_timestamp,
        DATE(transaction_date) AS transaction_date,

        -- Measures
        quantity::int AS quantity,
        unit_price::decimal(10,2) AS unit_price,
        amount::decimal(10,2) AS amount,
        discount::decimal(10,2) AS discount,
        cost::decimal(10,2) AS cost,

        -- Metadata
        _loaded_at
    FROM source
),

validated AS (
    SELECT
        *,
        -- Data quality flags
        CASE
            WHEN amount < 0 THEN 'negative_amount'
            WHEN quantity <= 0 THEN 'invalid_quantity'
            WHEN unit_price <= 0 THEN 'invalid_price'
            ELSE NULL
        END AS quality_flag
    FROM renamed
)

SELECT * FROM validated
WHERE quality_flag IS NULL  -- Filter out bad data

-- dbt will track this lineage automatically
```

### Intermediate Model

```sql
-- models/intermediate/int_sales_enriched.sql
{{
    config(
        materialized='ephemeral',
        tags=['intermediate', 'sales']
    )
}}

WITH transactions AS (
    SELECT * FROM {{ ref('stg_sales_transactions') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

enriched AS (
    SELECT
        -- Transaction info
        t.transaction_id,
        t.transaction_date,
        t.transaction_timestamp,

        -- Customer info
        c.customer_id,
        c.customer_name,
        c.customer_segment,
        c.customer_lifetime_value,

        -- Product info
        p.product_id,
        p.product_name,
        p.category,
        p.subcategory,
        p.brand,

        -- Measures
        t.quantity,
        t.unit_price,
        t.amount,
        t.discount,
        t.cost,

        -- Calculated metrics
        t.amount - t.discount AS revenue,
        (t.amount - t.discount) - t.cost AS profit,
        ROUND(((t.amount - t.discount) - t.cost) / (t.amount - t.discount) * 100, 2) AS profit_margin_pct

    FROM transactions t
    LEFT JOIN customers c ON t.customer_id = c.customer_id
    LEFT JOIN products p ON t.product_id = p.product_id
)

SELECT * FROM enriched
```

### Fact Table Model

```sql
-- models/marts/fct_sales.sql
{{
    config(
        materialized='incremental',
        unique_key='transaction_id',
        partition_by={
            'field': 'transaction_date',
            'data_type': 'date',
            'granularity': 'day'
        },
        cluster_by=['customer_id', 'product_id'],
        tags=['marts', 'sales', 'fact']
    )
}}

WITH enriched_sales AS (
    SELECT * FROM {{ ref('int_sales_enriched') }}

    {% if is_incremental() %}
        -- Incremental load: only process new data
        WHERE transaction_timestamp > (SELECT MAX(transaction_timestamp) FROM {{ this }})
    {% endif %}
),

with_metrics AS (
    SELECT
        *,
        -- Window functions for customer metrics
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY transaction_timestamp
        ) AS customer_transaction_sequence,

        LAG(transaction_date) OVER (
            PARTITION BY customer_id
            ORDER BY transaction_timestamp
        ) AS previous_transaction_date,

        -- Days since last purchase
        DATEDIFF('day',
            LAG(transaction_date) OVER (
                PARTITION BY customer_id
                ORDER BY transaction_timestamp
            ),
            transaction_date
        ) AS days_since_last_purchase

    FROM enriched_sales
)

SELECT * FROM with_metrics
```

### Dimension Model with SCD Type 2

```sql
-- models/marts/dim_product.sql
{{
    config(
        materialized='table',
        tags=['marts', 'dimension', 'scd2']
    )
}}

WITH source AS (
    SELECT * FROM {{ ref('stg_products') }}
),

scd_logic AS (
    SELECT
        -- Natural key
        product_id,

        -- Attributes
        product_name,
        category,
        subcategory,
        brand,
        unit_cost,
        is_active,

        -- SCD Type 2 columns
        _loaded_at AS effective_date,
        COALESCE(
            LEAD(_loaded_at) OVER (PARTITION BY product_id ORDER BY _loaded_at),
            '9999-12-31'::date
        ) AS expiry_date,
        CASE
            WHEN LEAD(_loaded_at) OVER (PARTITION BY product_id ORDER BY _loaded_at) IS NULL
            THEN TRUE
            ELSE FALSE
        END AS is_current

    FROM source
)

SELECT
    -- Surrogate key
    {{ dbt_utils.generate_surrogate_key(['product_id', 'effective_date']) }} AS product_key,
    *
FROM scd_logic
```

---

## SQL Query Patterns

### Incremental Merge (Upsert)

```sql
-- Snowflake MERGE syntax
MERGE INTO target_table AS target
USING (
    SELECT
        id,
        name,
        value,
        updated_at
    FROM staging_table
    WHERE updated_at > (SELECT MAX(updated_at) FROM target_table)
) AS source
ON target.id = source.id

-- Update existing records
WHEN MATCHED AND source.updated_at > target.updated_at THEN
    UPDATE SET
        target.name = source.name,
        target.value = source.value,
        target.updated_at = source.updated_at

-- Insert new records
WHEN NOT MATCHED THEN
    INSERT (id, name, value, updated_at)
    VALUES (source.id, source.name, source.value, source.updated_at);
```

### Slowly Changing Dimension Type 2

```sql
-- Expire old records
UPDATE dim_customer
SET
    is_current = FALSE,
    expiry_date = CURRENT_TIMESTAMP
WHERE customer_id IN (
    SELECT customer_id
    FROM staging_customer_updates
)
AND is_current = TRUE;

-- Insert new versions
INSERT INTO dim_customer (
    customer_id,
    first_name,
    last_name,
    email,
    segment,
    effective_date,
    expiry_date,
    is_current
)
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    segment,
    CURRENT_TIMESTAMP AS effective_date,
    '9999-12-31'::date AS expiry_date,
    TRUE AS is_current
FROM staging_customer_updates;
```

### Deduplication with Row Number

```sql
-- Remove duplicates, keeping latest record
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY transaction_id
            ORDER BY updated_at DESC, loaded_at DESC
        ) AS rn
    FROM raw_transactions
)
SELECT *
FROM ranked
WHERE rn = 1;
```

### Date Spine for Gap Filling

```sql
-- Generate date series
WITH date_spine AS (
    SELECT
        DATEADD(day, seq4(), '2025-01-01'::date) AS date
    FROM TABLE(GENERATOR(ROWCOUNT => 365))
),

sales_with_gaps AS (
    SELECT
        DATE(transaction_date) AS date,
        SUM(amount) AS total_sales
    FROM sales_transactions
    GROUP BY 1
)

-- Fill gaps with 0
SELECT
    ds.date,
    COALESCE(s.total_sales, 0) AS total_sales
FROM date_spine ds
LEFT JOIN sales_with_gaps s ON ds.date = s.date
ORDER BY ds.date;
```

---

## Python Pipeline Templates

### Data Quality Validation Class

```python
from typing import List, Dict, Any
import pandas as pd
import logging

class DataQualityValidator:
    """
    Comprehensive data quality validation framework
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.checks = []

    def check_completeness(self, columns: List[str], threshold: float = 0.95):
        """Check for null values in required columns"""
        for col in columns:
            non_null_pct = self.df[col].notna().mean()
            self.checks.append({
                'dimension': 'completeness',
                'check': f'{col}_not_null',
                'passed': non_null_pct >= threshold,
                'value': non_null_pct,
                'threshold': threshold
            })
        return self

    def check_uniqueness(self, columns: List[str]):
        """Check for duplicate values"""
        for col in columns:
            is_unique = self.df[col].is_unique
            duplicate_count = self.df[col].duplicated().sum()
            self.checks.append({
                'dimension': 'uniqueness',
                'check': f'{col}_unique',
                'passed': is_unique,
                'value': len(self.df) - duplicate_count,
                'duplicates': duplicate_count
            })
        return self

    def check_range(self, column: str, min_val: float = None, max_val: float = None):
        """Check numeric ranges"""
        if min_val is not None:
            min_check = (self.df[column] >= min_val).all()
            self.checks.append({
                'dimension': 'accuracy',
                'check': f'{column}_min',
                'passed': min_check,
                'value': self.df[column].min()
            })

        if max_val is not None:
            max_check = (self.df[column] <= max_val).all()
            self.checks.append({
                'dimension': 'accuracy',
                'check': f'{column}_max',
                'passed': max_check,
                'value': self.df[column].max()
            })
        return self

    def check_format(self, column: str, regex: str):
        """Check string format with regex"""
        valid_format = self.df[column].str.match(regex)
        valid_pct = valid_format.mean()
        self.checks.append({
            'dimension': 'accuracy',
            'check': f'{column}_format',
            'passed': valid_pct >= 0.99,
            'value': valid_pct
        })
        return self

    def check_referential_integrity(self, column: str, reference_values: set):
        """Check foreign key integrity"""
        valid_refs = self.df[column].isin(reference_values)
        valid_pct = valid_refs.mean()
        self.checks.append({
            'dimension': 'consistency',
            'check': f'{column}_referential_integrity',
            'passed': valid_pct >= 0.99,
            'value': valid_pct
        })
        return self

    def get_results(self) -> Dict[str, Any]:
        """Get validation results"""
        failed_checks = [c for c in self.checks if not c['passed']]
        return {
            'total_checks': len(self.checks),
            'passed_checks': len(self.checks) - len(failed_checks),
            'failed_checks': len(failed_checks),
            'all_passed': len(failed_checks) == 0,
            'checks': self.checks,
            'failures': failed_checks
        }

    def raise_on_failure(self):
        """Raise exception if any checks failed"""
        results = self.get_results()
        if not results['all_passed']:
            failures = '\n'.join([
                f"- {c['check']}: {c.get('value')}"
                for c in results['failures']
            ])
            raise ValueError(f"Data quality checks failed:\n{failures}")

# Usage example
validator = DataQualityValidator(df)
results = validator \
    .check_completeness(['transaction_id', 'customer_id']) \
    .check_uniqueness(['transaction_id']) \
    .check_range('amount', min_val=0, max_val=1000000) \
    .check_format('email', r'^[\w\.-]+@[\w\.-]+\.\w+$') \
    .get_results()

if not results['all_passed']:
    logging.error(f"Quality checks failed: {results['failures']}")
```

### Retry Decorator with Exponential Backoff

```python
import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Retry decorator with exponential backoff
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        logging.error(f"Max retries ({max_retries}) exceeded")
                        raise

                    logging.warning(
                        f"Attempt {attempt + 1} failed: {str(e)}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    delay *= backoff_factor

        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3, initial_delay=2, backoff_factor=2)
def extract_from_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

---

## Docker & Deployment

### Dockerfile for Data Pipeline

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run pipeline
CMD ["python", "scripts/run_pipeline.py"]
```

### Docker Compose for Local Development

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: datauser
      POSTGRES_PASSWORD: datapass
      POSTGRES_DB: analytics
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  airflow-webserver:
    image: apache/airflow:2.7.0
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://datauser:datapass@postgres/analytics
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
    ports:
      - "8080:8080"
    command: webserver

  spark-master:
    image: bitnami/spark:3.4
    environment:
      - SPARK_MODE=master
    ports:
      - "8081:8080"
      - "7077:7077"

  spark-worker:
    image: bitnami/spark:3.4
    depends_on:
      - spark-master
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077

volumes:
  postgres_data:
```

---

## Configuration Files

### dbt project.yml

```yaml
name: 'analytics'
version: '1.0.0'
config-version: 2

profile: 'analytics'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  analytics:
    staging:
      +materialized: view
      +tags: ['staging']

    intermediate:
      +materialized: ephemeral
      +tags: ['intermediate']

    marts:
      +materialized: table
      +tags: ['marts']

      sales:
        +schema: sales
        +tags: ['sales']

      customers:
        +schema: customers
        +tags: ['customers']

seeds:
  +quote_columns: false

snapshots:
  +target_schema: snapshots
```

### Spark Configuration

```conf
# spark-defaults.conf

# Memory settings
spark.driver.memory=4g
spark.executor.memory=8g
spark.executor.cores=4

# Shuffle settings
spark.sql.shuffle.partitions=200
spark.shuffle.service.enabled=true

# Adaptive query execution
spark.sql.adaptive.enabled=true
spark.sql.adaptive.coalescePartitions.enabled=true

# Dynamic allocation
spark.dynamicAllocation.enabled=true
spark.dynamicAllocation.minExecutors=2
spark.dynamicAllocation.maxExecutors=10

# Serialization
spark.serializer=org.apache.spark.serializer.KryoSerializer

# S3 settings
spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem
spark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.DefaultAWSCredentialsProviderChain
```

---

## Testing Templates

### pytest Fixtures

```python
import pytest
import pandas as pd
from sqlalchemy import create_engine

@pytest.fixture
def sample_sales_data():
    """Sample sales data for testing"""
    return pd.DataFrame({
        'transaction_id': ['T1', 'T2', 'T3'],
        'customer_id': ['C1', 'C2', 'C1'],
        'amount': [100.0, 200.0, 150.0],
        'transaction_date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03'])
    })

@pytest.fixture
def test_db_engine():
    """Test database engine"""
    engine = create_engine('sqlite:///:memory:')
    yield engine
    engine.dispose()

def test_transform_sales_data(sample_sales_data):
    """Test sales data transformation"""
    result = transform_sales_data(sample_sales_data)

    assert len(result) == 3
    assert 'revenue' in result.columns
    assert result['revenue'].sum() == 450.0

def test_data_quality_checks(sample_sales_data):
    """Test data quality validation"""
    validator = DataQualityValidator(sample_sales_data)
    results = validator \
        .check_completeness(['transaction_id', 'customer_id']) \
        .check_uniqueness(['transaction_id']) \
        .get_results()

    assert results['all_passed'] is True
```

---

**Last Updated:** 2025-11-08
**Version:** 1.0.0
