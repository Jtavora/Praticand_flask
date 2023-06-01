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
def disciplina():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Disciplina;')
    disciplinas = cur.fetchall()
    cur.close()
    print(disciplinas)
    return render_template('disciplinas.html', disciplinas=disciplinas)

@app.route('/professor')
def professor():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Professor;')
    professores = cur.fetchall()
    cur.close()
    print(professores)
    return render_template('professor.html', professores=professores)

@app.route('/aluno')
def aluno():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM aluno;')
    alunos = cur.fetchall()
    cur.close()
    print(alunos)
    return render_template('aluno.html', alunos=alunos)

@app.route('/login')
def login():
    user = request.form['usuario']
    senha = request.form['senha']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Login WHERE usuario = %s AND senha = %s;', (user, senha))
    login = cur.fetchone()
    cur.close()
    if login is None:
        return render_template('index.html')
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
