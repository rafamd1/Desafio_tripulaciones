import pymysql.cursors
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import os
from typing import Optional

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales desde las variables de entorno
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')

app = FastAPI()

def get_db_connection():
    try:
        db = pymysql.connect(**config)
        return db
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estadisticas/carrera")
def get_career_count():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT carrera, COUNT(*) as count FROM candidatos GROUP BY carrera')
        career_count = {row['carrera']: row['count'] for row in cursor.fetchall()}
        return career_count
    finally:
        cursor.close()
        db.close()

@app.get("/estadisticas/notas")
def get_average_grades():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT carrera, AVG(nota_media) as average FROM candidatos GROUP BY carrera')
        average_grades = {row['carrera']: row['average'] for row in cursor.fetchall()}
        return average_grades
    finally:
        cursor.close()
        db.close()

@app.get("/estadisticas/ingles")
def get_english_level_count():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT nivel_ingles, COUNT(*) as count FROM candidatos GROUP BY nivel_ingles')
        english_level_count = {row['nivel_ingles']: row['count'] for row in cursor.fetchall()}
        return english_level_count
    finally:
        cursor.close()
        db.close()

@app.get("/estadisticas/edad")
def get_age_distribution():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT edad, COUNT(*) as count FROM candidatos GROUP BY edad')
        age_distribution = {row['edad']: row['count'] for row in cursor.fetchall()}
        return age_distribution
    finally:
        cursor.close()
        db.close()

@app.get("/estadisticas/status")
def get_candidacy_status_count():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute('SELECT status, COUNT(*) as count FROM candidaturas GROUP BY status')
        candidacy_status_count = {row['status']: row['count'] for row in cursor.fetchall()}
        return candidacy_status_count
    finally:
        cursor.close()
        db.close()

# Ejecutar el servidor con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

