# Book Scraper API

A backend data pipeline that scrapes book data, stores it in a MySQL database, and exposes it via a FastAPI-based REST API with filtering, sorting, and pagination. The system is deployed on the cloud and supports automated data ingestion with deduplication.

---

## Overview

This project demonstrates an end-to-end backend system including data extraction, transformation, storage, and API exposure. It follows a modular architecture with separate components for scraping, database interaction, and API services.

---

## Features

- Web scraping using Requests and BeautifulSoup
- REST API built with FastAPI
- MySQL database hosted on Railway
- Data deduplication using UNIQUE constraints and upsert logic
- Filtering, searching, sorting, and pagination support
- Scheduler-based automated data updates
- Manual trigger endpoint for scraper execution
- Cloud deployment using Render

---

## Architecture

- Scraper Layer: Extracts book data from target website
- Database Layer: Handles insertion, updates, and querying of data
- API Layer: Provides endpoints for data retrieval and control operations
- Scheduler: Periodically triggers scraping jobs

---

## Tech Stack

- Language: Python
- Framework: FastAPI
- Database: MySQL (Railway)
- Scraping: Requests, BeautifulSoup
- Scheduler: APScheduler
- Deployment: Render

---

## API Endpoints

### Base URL
https://book-api-319w.onrender.com

---

### GET /

Health check endpoint to verify API status.

---

### GET /products

Fetch product data with filtering, searching, sorting, and pagination.

#### Query Parameters

- min_price (float): Minimum price filter
- max_price (float): Maximum price filter
- rating (string): Filter by rating (One, Two, Three, Four, Five)
- search (string): Case-insensitive title search
- sort (string): Sorting field (id, price, rating, title)
- order (string): Sorting order (asc, desc)
- limit (int): Number of records to return
- offset (int): Pagination offset

---

### GET /run-scraper

Manually triggers the scraping pipeline and inserts/updates data in the database.

---

### GET /products_paginated

Basic pagination endpoint using LIMIT and OFFSET.

---

## Database Design

Table: products

- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- title (VARCHAR, UNIQUE, NOT NULL)
- price (FLOAT)
- rating (VARCHAR)
- created_at (TIMESTAMP)

Indexes:
- Index on price
- Index on rating

Deduplication:
- UNIQUE constraint on title
- INSERT ... ON DUPLICATE KEY UPDATE used for idempotent writes

---

## Data Flow

1. Scraper fetches HTML pages from source website
2. Parses book title, price, and rating
3. Cleans and normalizes extracted data
4. Inserts into MySQL using upsert logic
5. API queries database and returns JSON responses

---

## Deployment

- API hosted on Render
- Database hosted on Railway
- Scheduler initialized on application startup

---

## URL (To Cheack)
Base URL:
https://book-api-319w.onrender.com

Health Check:
https://book-api-319w.onrender.com/

API Documentation (Swagger):
https://book-api-319w.onrender.com/docs

Get Products:
https://book-api-319w.onrender.com/products

Get Products (with filters example):
https://book-api-319w.onrender.com/products?min_price=20&max_price=60&sort=price&order=desc

Pagination Example:
https://book-api-319w.onrender.com/products_paginated?limit=10&offset=0

Run Scraper (manual trigger):
https://book-api-319w.onrender.com/run-scraper
## Limitations

- Scheduler reliability depends on Render uptime (free tier sleeps on inactivity)
- No distributed task queue (single-process scheduler)
- No caching layer for high-frequency queries

---

## Future Improvements

- Introduce Redis caching layer
- Implement asynchronous or parallel scraping
- Use background workers (Celery / RQ)
- Add authentication and rate limiting
- Improve search with full-text indexing
- Add monitoring and logging

---

## Author

Kavya SV