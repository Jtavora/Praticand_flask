import os
import psycopg2

conn = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    database=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD')
)

cur = conn.cursor()

#Criando tabelas
cur.execute('DROP TABLE IF EXISTS Aluno;')
cur.execute('DROP TABLE IF EXISTS Professor;')
cur.execute('DROP TABLE IF EXISTS Disciplina;')
cur.execute('create table Disciplina (id serial primary key, nome varchar(100));')
cur.execute('create table Professor (id serial primary key, nome varchar(100), materia integer references Disciplina(id));')
cur.execute('create table Aluno (id serial primary key, nome varchar(100), materia integer references Disciplina(id));')
cur.execute('create table Login (usuario varchar(100), senha varchar(100));')

#Inserindo dados
cur.execute('insert into Disciplina (nome) values (%s);', ('Matemática',))
cur.execute('insert into Disciplina (nome) values (%s);', ('Português',))
cur.execute('insert into Disciplina (nome) values (%s);', ('História',))
cur.execute('insert into Disciplina (nome) values (%s);', ('Geografia',))
cur.execute('insert into Disciplina (nome) values (%s);', ('Física',))
cur.execute('insert into Disciplina (nome) values (%s);', ('Química',))

cur.execute('insert into Professor (nome, materia) values (%s, %s);', ('João', 1))
cur.execute('insert into Professor (nome, materia) values (%s, %s);', ('Maria', 2))
cur.execute('insert into Professor (nome, materia) values (%s, %s);', ('José', 3))
cur.execute('insert into Professor (nome, materia) values (%s, %s);', ('Ana', 4))
cur.execute('insert into Professor (nome, materia) values (%s, %s);', ('Pedro', 5))
cur.execute('insert into Professor (nome, materia) values (%s, %s);', ('Paula', 6))

cur.execute('insert into Aluno (nome, materia) values (%s, %s);', ('Gustavo', 1))
cur.execute('insert into Aluno (nome, materia) values (%s, %s);', ('Flavio', 2))
cur.execute('insert into Aluno (nome, materia) values (%s, %s);', ('Augusto', 3))
cur.execute('insert into Aluno (nome, materia) values (%s, %s);', ('Rafael', 4))
cur.execute('insert into Aluno (nome, materia) values (%s, %s);', ('Henrique', 5))
cur.execute('insert into Aluno (nome, materia) values (%s, %s);', ('Paulo', 6))

cur.execute('insert into Login (usuario, senha) values (%s, %s);', ('Távora', 'admin'))

#Commitando alterações
conn.commit()
cur.close()
conn.close()

