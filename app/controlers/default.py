import os
from app.__init__ import app, render_template, request, session, redirect, url_for, make_response, abort, flash
from app.models.banco import *
from app.controlers.check import *

#TASKS

print("create table")

#verificação

() if os.path.exists('banco.db') == True else create_table()

#GET

@app.route("/")
def tasks():
    name = request.cookies.get('name')

    print(name)

    if name in ('',None):
        return redirect('/login')
    else:
        return render_template("tasks.html", tasks=select_all(1,hash_transform(get_cpf(name))), name = name)

#NEW TASK

@app.route("/new_task", methods=('GET','POST'))
def new_task():
    msg = ''
    if request.method == 'POST':
        name_task = request.form["name_task"]       
        cpf = hash_transform(get_cpf(request.cookies.get('name')))
        if task_exists(name_task, select_all(0, cpf)) == True:
            msg = 'task já existe'
        else:
            date = request.form["date"]
            task = request.form["task"]
            insert_task(cpf,name_task,date,task)
            return redirect('/')
    return render_template("new_task.html", msg=msg)

#LOGIN

@app.route("/login", methods=('GET','POST'))
def login():
    if not request.cookies.get('name') in ('',None):
        return redirect('/')
    else:
        msg = ''
        print(request.cookies.get('name'))
        if request.method == 'POST':
            name_email = request.form['name_email']
            password = request.form['password']
            if user_exists(name_email, select_all(2)) == True:
                pas = get_password(name_email)
                if password_check(password,pas) == True:
                    resp = make_response(redirect('/'))
                    resp.set_cookie('name', name_email)
                    return resp
                else: msg = 'name/email ou senha incorretos'
            else: msg = 'não cadastrado'

        return render_template('login.html', msg=msg)


@app.route('/<name>')
def perfil(name):
    if request.cookies.get('name') == name:
        return render_template('perfil.html', data_user=select_all(4,name=name))
    elif user_exists(name, select_all(2)):
        return render_template('perfil.html',data_user=select_all(4,name=name))
    else: return render_template('perfil.html',data_user=None)
            


#NEW USER
@app.route("/new_user", methods=('GET','POST'))
def new_user():
    if not request.cookies.get('name') in ('',None):
        return redirect('/')
    else:
        msg = ''
        if request.method == 'POST':
            if request.cookies.get('name') in ('', None):
                cpf = hash_transform(request.form['cpf'])
                if cpf_exists(cpf, select_all(2)) == True:
                    msg = 'usuário já existente'
                else:
                    name = request.form['name']
                    email = request.form['email']
                    password = hash_transform(request.form['password'])
                    insert_user(cpf,name,email,password)
                    return redirect('/login')
        return render_template('new_user.html',msg=msg)

#EXIT USER
@app.route("/pop")
def pop_user():
    resp = make_response(render_template('login.html'))
    resp.set_cookie('name', '')
    return resp

#DELETE BANCO
@app.route("/delete_banco")
def delete_banco():
    delete_table_task()
    delete_table_user()
    create_table()
    return redirect('/admin')

#UPLOAD DE FOTOS
@app.route('/upload')
def upload():
    return """
    <form enctype='multipart/form-data' action='/upload' method='POST'>
    <input type='file' name='file'><br>
    <button>>></button>
    </form>
    """


#ADMIN

@app.route('/admin')
def admin():
    return f"""
    <header>
        <nav>
            <ul style="list-style: none;">
                <li><a href="/"><strong>TASKS</strong></a></li>
                <li><a href="/delete_banco">deletar</a></li>
                <li><a href="/pop">sair</a></li>
            </ul>
        </nav>
    </header>
    tasks
    {select_all(3)}
    users
    {select_all(2)}
    """