from flask import Flask, render_template, request, redirect, flash, url_for, g
import os
import psycopg2

app = Flask(__name__)

app.secret_key = 'Tavora'

app.config['FLASH_MESSAGES'] = [
    {'category': 'success', 'duration': 3000},  
    {'category': 'error', 'duration': 3000}    
]

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

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('password')
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Login WHERE usuario = %s AND senha = %s;', (user, senha))
        login = cur.fetchone()
        cur.close()
        if login is None:
            print('Login inválido')
            flash('Login inválido', 'error') 
            return render_template('index.html')
        else:
            print('Login válido')
            flash('Login bem-sucedido', 'success')
            return redirect('/admin/op_admin')
    else:
        return render_template('admin.html')
    
@app.route('/admin/op_admin')
def admin_op():
    return render_template('op_admin.html')

@app.route('/admin/op_admin/cadastra_aluno', methods=['POST', 'GET'])
def cadastra_aluno():
    if request.method == 'POST':
        nome = request.form.get('aluno')
        materia = request.form.get('materia')
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO aluno (nome, materia) VALUES (%s, %s);', (nome, materia))
        conn.commit()
        cur.close()
        print(nome, materia)
        flash('Aluno cadastrado com sucesso', 'success')
        return redirect('/admin/op_admin')
    else:
        flash('Aluno nao cadastrado, erro!', 'error')
        return render_template('cadastra_aluno.html')
    
@app.route('/admin/op_admin/cadastra_admin', methods=['POST', 'GET'])
def cadastra_admin():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO login VALUES (%s, %s);', (usuario, password))
        conn.commit()
        cur.close()
        print(usuario, password)
        flash('Admin cadastrado com sucesso', 'success')
        return redirect('/admin/op_admin')
    else:
        flash('Admin nao cadastrado, erro!', 'error')
        return render_template('cadastra_Admin.html')
    
@app.route('/admin/op_admin/cadastra_professor', methods=['POST', 'GET'])
def cadastra_prof():
    if request.method == 'POST':
        nome = request.form.get('professor')
        materia = request.form.get('materia')
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO professor (nome, materia) VALUES (%s, %s);', (nome, materia))
        conn.commit()
        cur.close()
        print(nome, materia)
        flash('Professor cadastrado com sucesso', 'success')
        return redirect('/admin/op_admin')
    else:
        flash('Professor nao cadastrado, erro!', 'error')
        return render_template('cadastra_professor.html')
    
@app.route('/admin/op_admin/cadastra_disciplina', methods=['POST', 'GET'])
def cadastra_dis():
    if request.method == 'POST':
        nome = request.form.get('materia')
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO disciplina (nome) VALUES (%s);', (nome,))
        conn.commit()
        cur.close()
        print(nome)
        flash('Disciplina cadastrada com sucesso', 'success')
        return redirect('/admin/op_admin')
    else:
        flash('Disciplina nao cadastrada, erro!', 'error')
        return render_template('cadastra_disciplina.html')

    
if __name__ == '__main__':
    app.run(debug=True)
