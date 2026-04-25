from scheduler import start_scheduler
from fastapi import FastAPI
from database.db import get_connection
from fastapi import HTTPException, Query

# start_scheduler()

app=FastAPI()

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/run-scraper")
def run_scraper():
    from scraper.main import scrape_books
    from database.insert import insert_products

    data = scrape_books()
    insert_products(data)

    return {"message": "Scraper executed", "count": len(data)}
@app.get("/")
def home():
    return {"message": "API is Running"}
@app.get("/products")
def get_products(
    min_price: float=0,
    max_price: float=1000,
    search: str=None,
    rating: str=None,
    sort: str="id",
    order: str="asc",
    limit: int= Query(10,ge=1, le=100),
    offset: int= Query(0,ge=0)
):
    conn=None
    cursor=None
    
    try:
        conn=get_connection()
        cursor=conn.cursor(dictionary=True)

        allowed_sort=["id","price","rating","title"]
        if sort not in allowed_sort:
            sort = "id"
        order=order.lower()
        if order not in ("asc","desc"):
            order="asc"

        query_total="SELECT COUNT(*) as total FROM products WHERE price BETWEEN %s AND %s"
        params_total=[min_price,max_price]

        if rating:
            query_total+= " AND rating =%s"
            params_total.append(rating)
        
        if search:
            query_total+=" AND title LIKE %s"
            params_total.append(f"%{search}%")

        cursor.execute(query_total,params_total)
        total=cursor.fetchone()["total"]

        
        query= "SELECT * from products WHERE price BETWEEN %s AND %s"
        params= [min_price, max_price]
        
        if rating:
            query+= " AND rating =%s"
            params.append(rating)
        
        if search:
            query+=" AND title LIKE %s"
            params.append(f"%{search}%")

        query+= f" ORDER BY {sort} {order} LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(query,params)
        data=cursor.fetchall()

        return {
        "total": total,
        "count": len(data),
        "limit": limit,
        "offset": offset,
        "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()   

@app.get("/products_paginated")
def get_products_paginated(limit: int=Query(10, ge=1, le=100), offset: int =Query(0, ge=0)):
    conn = None
    cursor = None

    try:
        conn=get_connection()
        cursor=conn.cursor(dictionary=True)
        query_total="SELECT COUNT(*) as total from products"
        query="SELECT * from products LIMIT %s OFFSET %s"
        cursor.execute(query, (limit,offset))   

        data=cursor.fetchall()

        cursor.execute(query_total)
        total = cursor.fetchone()["total"]
        return {
        "Total":total,
        "count": len(data),
        "limit": limit,
        "offset": offset,
        "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    