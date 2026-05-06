from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


#  Conexão com banco / Connection with the bank
def get_db_connection():
    conn = sqlite3.connect("books.db")
    conn.row_factory = sqlite3.Row
    return conn


#  Criar tabela automaticamente / Create table automatically
def init_db():
    conn = sqlite3.connect("books.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.close()


init_db()


#  Página principal / Home page
@app.route("/")
def index():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("index.html", books=books)


#  Adicionar livro / Add book
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        status = request.form["status"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO books (title, author, status) VALUES (?, ?, ?)",
            (title, author, status)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")


#  Deletar livro / Delete book
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


#  Rodar servidor / Run server
if __name__ == "__main__":
    app.run(debug=True)
