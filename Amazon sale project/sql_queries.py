
import psycopg2
import pandas as pd

# Connect to our database
conn = psycopg2.connect(
    dbname='your_db',
    user='your_user',
    password='your_pass',
    host='your_host',
    port='your_port'
)

# --- QUERY : add main_category column to products table
cursor = conn.cursor()
cursor.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS main_category TEXT;")
cursor.execute("UPDATE products SET main_category = TRIM(SPLIT_PART(category, '|', 1)||'|'||SPLIT_PART(category, '|', 2));")
conn.commit()
cursor.close()

# --- QUERY : Total Revenue By category Products ---
df= pd.read_sql ("SELECT * FROM products", conn)
sd= df.groupby("category")["revenue"].sum().sort_values(ascending=False)
se= df.groupby("category")["rating"].mean().sort_values
print(sd,se)



# A function that takes raw SQL, runs it, and returns a Pandas table
def run_query(sql_query, description):
    print(f"\n--- {description} ---")
    
    cursor = conn.cursor()
    cursor.execute(sql_query)
    
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    df = pd.DataFrame(rows, columns=columns)
    
    print(df)
    cursor.close()


# --- QUERY : Top 5 Most Profitable Products ---
query_profit = """
SELECT product_name, category, profit 
FROM products 
ORDER BY profit DESC NULLS LAST 
LIMIT 5;
"""
run_query(query_profit, "TOP 5 MOST PROFITABLE PRODUCTS")


# --- QUERY : The 5 Highest Rated Categories ---
query_categories = """
SELECT category, ROUND(AVG(rating), 2) as average_rating, COUNT(*) as total_products
FROM products 
GROUP BY category 
ORDER BY average_rating DESC NULLS LAST 
LIMIT 5;
"""
run_query(query_categories, "TOP 5 HIGHEST RATED CATEGORIES")


# --- QUERY : The Biggest Discounts Configured ---
query_discounts = """
SELECT product_name, Discount_Price, Actual__Price, discount_percentage 
FROM products 
ORDER BY discount_percentage DESC NULLS LAST 
LIMIT 5;
"""
run_query(query_discounts, "PRODUCTS WITH THE ABSOLUTE BIGGEST DISCOUNTS")


conn.close()
