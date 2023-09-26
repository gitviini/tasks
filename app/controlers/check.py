from hashlib import sha3_224

#CHECK

# verifica se já existe task pelo nome
def task_exists(name_task, banco):
    try:
        resp = False
        for name in banco:
            if name_task == name[0]:
                resp = True
            else: pass
            
        return resp
    except: pass

def cpf_exists(cpf, banco):
    try:
        resp = False
        for data in banco:
            resp = True if cpf == data[0] else ()
        return resp
    except: pass

def user_exists(user, banco):
    try:
        resp = False
        for data in banco:
            if user == data[1] or user == data[2]:
                resp = True
        return resp
    except: pass

def hash_transform(value=''):
    try:
        value = bytes(value, 'utf-8')
        resp = sha3_224()
        resp.update(value)
        return resp.hexdigest()
    except Exception as erro: print(erro)

def password_check(password='',request_password=''):
    try:
        password = hash_transform(password)

        return True if password == request_password else False
    except Exception as erro: print(erro)
