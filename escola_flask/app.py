from flask import Flask, render_template, request, redirect, flash, url_for, g
import os
import psycopg2

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        # Estabelece uma nova conexão com o banco de dados
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        g.db = conn
    return g.db

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disciplinas')
def disciplinas():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Disciplina;')
    disciplinas = cur.fetchall()
    cur.close()
    print(disciplinas)
    return render_template('disciplinas.html', disciplinas=disciplinas)

if __name__ == '__main__':
    app.run(debug=True)
