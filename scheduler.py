from apscheduler.schedulers.background import BackgroundScheduler
from scraper.main import scrape_books
from database.insert import insert_products

def job():
    print("Running scraper job...")
    data=scrape_books()
    insert_products(data)
    print("Scraping completed!")
def start_scheduler():
    scheduler=BackgroundScheduler()
    scheduler.add_job(job, "interval", seconds=3600)
    scheduler.start()