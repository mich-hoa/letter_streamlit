import os
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'ap-southeast-2')
)

def get_table(name):
    return dynamodb.Table(os.getenv(name))

# ── Letters ──────────────────────────────────────────────
def load_letters():
    try:
        return get_table('DYNAMODB_TABLE_NAME').scan().get('Items', [])
    except ClientError as e:
        st.error(f"DynamoDB error: {e}")
        return []

def save_letter(item):
    try:
        get_table('DYNAMODB_TABLE_NAME').put_item(Item=item)
    except ClientError as e:
        st.error(f"DynamoDB error: {e}")

# ── Memories ─────────────────────────────────────────────
def load_memories():
    try:
        return get_table('DYNAMODB_MEMORIES_TABLE').scan().get('Items', [])
    except ClientError as e:
        st.error(f"DynamoDB error: {e}")
        return []

def save_memory(item):
    try:
        get_table('DYNAMODB_MEMORIES_TABLE').put_item(Item=item)
    except ClientError as e:
        st.error(f"DynamoDB error: {e}")

# ── Dates ─────────────────────────────────────────────────
def load_dates():
    try:
        return get_table('DYNAMODB_DATES_TABLE').scan().get('Items', [])
    except ClientError as e:
        st.error(f"DynamoDB error: {e}")
        return []

def save_date(item):
    try:
        get_table('DYNAMODB_DATES_TABLE').put_item(Item=item)
    except ClientError as e:
        st.error(f"DynamoDB error: {e}")
