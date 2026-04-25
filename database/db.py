import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="switchback.proxy.rlwy.net",
        port=50711,
        user="root",
        password="NpZcSTYealSIFuFQOObOxHtXCVPuvAIQ",
        database="railway"
    )