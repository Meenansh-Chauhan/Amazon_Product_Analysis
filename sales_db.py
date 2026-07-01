import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname='your_db',
    user='your_user',
    password='your_pass',
    host='your_host',
    port='your_port'
)

cursor = conn.cursor()

df= pd.read_csv('amazon.csv')

df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

df= df.where(pd.notnull(df),None)

create_table_query = """
CREATE TABLE products
(
    product_id VARCHAR(50) PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    Discount_Price NUMERIC,
    Actual__Price NUMERIC,
    discount_percentage NUMERIC,
    rating NUMERIC,
    rating_count NUMERIC,
    about_product TEXT,
    user_id TEXT,
    user_name TEXT,
    review_id TEXT,
    review_title TEXT,
    review_content TEXT,
    img_link TEXT,
    product_link TEXT,
    revenue NUMERIC,
    profit NUMERIC
);
"""

cursor.execute(create_table_query)
conn.commit()

insert_query = """
INSERT INTO products (
    product_id, product_name, category, Discount_Price, Actual__Price, 
    discount_percentage, rating, rating_count, about_product, user_id, 
    user_name, review_id, review_title, review_content, img_link, product_link,
    revenue, profit
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (product_id) DO NOTHING;
"""

print("Starting to load data into PostgreSQL...")

for index, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))

conn.commit()

cursor.close()
conn.close() 


print("Success! All 18 columns have been loaded into the database.")
