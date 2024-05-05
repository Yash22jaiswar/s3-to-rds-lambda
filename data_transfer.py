import boto3
import pymysql
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define AWS credentials and regions
AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 's3-to-rds-lambda'
S3_FILE_KEY = 'data/sampledata.csv'  # Update with the correct file key
RDS_ENDPOINT = 'database-1.ctecq26gecpb.us-east-1.rds.amazonaws.com'
RDS_PORT = 3306
RDS_USER = 'admin'
RDS_PASSWORD = 'admin1234'
RDS_DB_NAME = 'database-1'
RDS_TABLE_NAME = 'sample'
RDS_TABLE_COLUMNS = 'id, name, age'

def read_data_from_s3(bucket_name, key):
    # Code to read data from S3 bucket
    try:
        s3 = boto3.client('s3', region_name=AWS_REGION)
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        data = obj['Body'].read().decode('utf-8')
        return data
    except Exception as e:
        logger.error(f"Error reading data from S3: {e}")
        raise

def push_data_to_rds(data):
    # Code to push data to RDS
    try:
        conn = pymysql.connect(host=RDS_ENDPOINT,
                               port=RDS_PORT,
                               user=RDS_USER,
                               password=RDS_PASSWORD,
                               database=RDS_DB_NAME)
        cursor = conn.cursor()
        sql = f"INSERT INTO {RDS_TABLE_NAME} ({RDS_TABLE_COLUMNS}) VALUES (%s, %s, %s)"
        # Parse CSV data and insert into RDS
        data_rows = data.split('\n')
        for row in data_rows[1:]:  # Skip header row
            columns = row.split(',')
            if len(columns) == 3:
                cursor.execute(sql, (columns[0], columns[1], columns[2]))
        conn.commit()
        conn.close()
        logger.info("Data successfully inserted into RDS")
    except Exception as e:
        logger.error(f"Error pushing data to RDS: {e}")
        raise

def push_data_to_glue(data):
    # Code to push data to Glue Database
    pass

if __name__ == "__main__":
    # Main logic to orchestrate the data transfer process
    try:
        data = read_data_from_s3(S3_BUCKET_NAME, S3_FILE_KEY)
        push_data_to_rds(data)
    except Exception as e:
        logger.error(f"Data transfer process failed: {e}")
        # Optionally, handle failure by pushing data to Glue Database
        # push_data_to_glue(data)

