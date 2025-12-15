import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "aira",
    "database": "t_iq_hr",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def insert_resume(file_name, file_path):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO resumes (file_name, file_path)
        VALUES (%s, %s)
    """
    cursor.execute(sql, (file_name, file_path))
    conn.commit()

    resume_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return resume_id


def insert_prediction(resume_id, fake_prob, label, model_version="v1_text"):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO predictions
        (resume_id, fake_probability, predicted_label, model_version)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (resume_id, fake_prob, label, model_version))
    conn.commit()

    cursor.close()
    conn.close()
