import os, sqlite3

# verifica se há o database
if os.path.exists("banco.db") == True: pass
else:
	con = sqlite3.connect("banco.db")
	con.commit()

# cria conexão com o database
def connect():
	try:
		con = sqlite3.connect("banco.db")
		cur = con.cursor()
		return con, cur
	except: pass
	finally: con.commit()

#cria as tables
def create_table():
	try:
		con, cur = connect()
		cur.execute("""CREATE TABLE user(
			cpf_user TEXT NOT NULL PRIMARY KEY,
			name_user VARCHAR(20) NOT NULL,
			email_user VARCHAR(40) NOT NULL,
			password_user VARCHAR(20) NOT NULL
			)""")
		cur.execute("""CREATE TABLE task(
			cpf VARCHAR(20) NOT NULL,
			name_task TEXT NOT NULL,
			date TEXT,
			task TEXT
			)""")
		print("create table")
	except: pass
	finally: con.commit()


#USER

#inserir user
def insert_user(cpf,name,email,password):
	try:
		con, cur = connect()
		print(f"usuário {name} criado")
		cur.execute(f"INSERT INTO user(cpf_user,name_user,email_user,password_user) VALUES('{cpf}','{name}','{email}','{password}')")
	except: pass
	finally: con.commit()

#delete user
def delete_user(cpf):
	try:
		con, cur = connect()
		cur.execute(f"DELETE FROM user WHERE cpf_user = '{cpf}'")
	except: pass
	finally: con.commit()

#retorna o cpf do user a partir do name
def get_cpf(name):
	try:
		con, cur = connect()
		cur.execute(f"SELECT cpf_user FROM user WHERE name_user = '{name}'")
		return cur.fetchall()[0][0]
	except: pass
	finally: con.commit()

#retorna a senha do user a partir do name
def get_password(name):
	try:
		con, cur = connect()
		cur.execute(f"SELECT password_user FROM user WHERE name_user = '{name}'")
		return cur.fetchone()[0]
	except: pass
	finally: con.commit()
#TASKS

# seleciona e retorna as informações do database
def select_all(mode, cpf='', name=''):
	try:
		con, cur = connect()
		match mode:
			case 0:
			#retorna os task do database
				cur.execute(f"SELECT name_task,date,task FROM task WHERE cpf = '{cpf}'")
				return cur.fetchall()
			case 1:
			#retorna uma lista formatada com as informações
				cur.execute(f"SELECT name_task,date,task FROM task WHERE cpf = '{cpf}'")
				list = []
				for task in cur.fetchall():
					list.append(' ') if task[0] == "" else list.append(task[0])
					list.append(' ') if task[1] == "" else list.append(task[1])
					list.append(' ') if task[2] == "" else list.append(task[2])
				return list
			case 2:
				cur.execute("SELECT * FROM user")
				return cur.fetchall()
			case 3:
				cur.execute('SELECT * FROM task')
				return cur.fetchall()
			case 4:
				cur.execute(f"SELECT * FROM user WHERE name_user = '{name}'")
				return cur.fetchone()
			case _:
				pass
	except Exception as erro: print(erro)
	finally: con.commit()

# inserir a task ao database
def insert_task(cpf_user,name_task,date,task):
	try:
		con, cur = connect()
		cur.execute(f"INSERT INTO task(cpf,name_task,date,task) VALUES('{cpf_user}','{name_task}','{date}','{task}')")
	except Exception as erro: print(erro)
	finally: con.commit()

# deleta a database (apenas linux)
def delete_arq():
    try:
        if os.path.exists("banco.db") == True and os.name != 'posix': pass
        else:
            os.system("rm -r banco.db")
    except: pass
        
#deletar table task
def delete_table_task():
	try:
		con, cur = connect()
		cur.execute('DELETE FROM task')
	except Exception as erro: print(erro)
	finally: con.commit()

#deletar table users
def delete_table_user():
	try:
		con, cur = connect()
		cur.execute('DELETE FROM user')
	except: pass
	finally: con.commit()