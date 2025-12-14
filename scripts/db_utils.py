import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost", user="root", password="aira", database="t_iq_hr"
    )


def insert_resume(file_name, file_path):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO resumes (file_name, file_path)
        VALUES (%s, %s)
        """,
        (file_name, file_path),
    )

    conn.commit()
    resume_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return resume_id


def insert_prediction(resume_id, prob, label):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (resume_id, fake_probability, predicted_label)
        VALUES (%s, %s, %s)
        """,
        (resume_id, prob, label),
    )

    conn.commit()
    cursor.close()
    conn.close()
