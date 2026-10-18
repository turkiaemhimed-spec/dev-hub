import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)


def init_db():
    print("Database initialization running...")

    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question_text TEXT NOT NULL,
            sample_answer TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM Questions")

    if cursor.fetchone()[0] == 0:
        questions = [
            (
                "SQL",
                "Medium",
                "What is the difference between an INNER JOIN and a LEFT JOIN?",
                "INNER JOIN returns matching rows from both tables. LEFT JOIN returns all rows from the left table and matching rows from the right table."
            ),
            (
                "Python",
                "Easy",
                "How does memory management work in Python?",
                "Python uses automatic memory management and garbage collection."
            ),
            (
                "C Programming",
                "Hard",
                "What is a dangling pointer and how do you prevent it?",
                "A dangling pointer points to memory that has already been freed. Set pointers to NULL after freeing memory."
            )
        ]

        cursor.executemany(
            """
            INSERT INTO Questions
            (language, difficulty, question_text, sample_answer)
            VALUES (?, ?, ?, ?)
            """,
            questions
        )

    conn.commit()
    conn.close()


@app.route("/")
def dashboard():

    selected_lang = request.args.get("language", "All")

    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    if selected_lang == "All":
        cursor.execute("""
            SELECT language, difficulty, question_text, sample_answer
            FROM Questions
        """)
    else:
        cursor.execute("""
            SELECT language, difficulty, question_text, sample_answer
            FROM Questions
            WHERE language = ?
        """, (selected_lang,))

    records = cursor.fetchall()
    conn.close()

    questions_list = []

    for r in records:
        questions_list.append({
            "language": r[0],
            "difficulty": r[1],
            "question": r[2],
            "answer": r[3]
        })

    with open("index.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    return render_template_string(
        html_template,
        questions=questions_list,
        selected_lang=selected_lang
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8000)