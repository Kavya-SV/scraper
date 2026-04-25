from database.db import get_connection

def insert_products(products):
    conn=get_connection()
    cursor=conn.cursor()
    # redeploy trigger
    
    query="""
    INSERT INTO products (title,price,rating)
    VALUES (%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        price = VALUES(price),
        rating= VALUES(rating)
    """

    for p in products:
        cursor.execute(query,(p["title"],p["price"],p["rating"]))
    conn.commit()
    cursor.close()
    conn.close()