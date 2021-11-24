from flask.templating import render_template
from flask import Flask, request, redirect, session, flash
from user import User
from task import Task
from flask_mysqldb import MySQL
from dao import TaskDao, UserDao

app = Flask(__name__)
app.secret_key='LOGIN'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'schedule'
app.config['MYSQL_PORT'] = 3306

database = MySQL(app)
user_dao = UserDao(database)
task_dao = TaskDao(database)

@app.route('/')
def index():
    if 'user' not in session or session['user'] == None:
         return redirect('/login')
    else:     
        user_name = session['name']
        find_tasks = task_dao.findTasks(session['user'])
        tasks=[]
        for task in find_tasks:
            tasks.append(Task(task[2],task[3],task[4],task[0],task[5]))

        return render_template('index.html', title = 'Tarefas de ' + user_name, tasks=tasks,)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    
    find_user = user_dao.findByEmail(request.form['email'])

    if(find_user):
        user = User(find_user[0],find_user[1],find_user[2],find_user[3])
        if(user._password == request.form['password']):
            flash('Bem-vindo ' + user._name + '!', 'message')
            session['user']=user._id
            session['name']=user._name
            return redirect('/')
        else:
            flash('Verifique seu e-mail ou senha.','error')
            return redirect('/login')
    else:
        flash('Verifique seu e-mail ou senha.','error')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session['user']=None
    session['name']=None
    flash('Até a proxima!','message')
    return redirect('/login')

@app.route('/create/user')
def create_user_render():
    return render_template('create-user.html')
    
@app.route('/create-user', methods=['POST'])
def create_user():
    if request.form['password'] != request.form['confirm-password']:
        flash('As senhas não conferem', 'error')
        return redirect('/create/user')
    else:
        user = User(None, request.form['name'], request.form['email'], request.form['password'])
        user_dao.save(user)
        return redirect('/login')

@app.route('/create/task')
def create_task_render():
    return render_template('create-task.html')
    
@app.route('/create-task', methods=['POST'])
def create_task():
    if(session['user']):
        task = Task(request.form['name'],request.form['description'],request.form['situation'])
        task_dao.save(task,session['user'])
        return redirect('/')
    else:
        flash('Sua sessão expirou!','warning')
        return redirect('/login')

@app.route('/situation/<int:id>')
def situation(id):
    if(session['user']):
        return render_template('update-situation.html', id=id)
    else:
        flash('Sua sessão expirou!','warning')
        return redirect('/login')

@app.route('/update-task', methods=['POST'])
def update():
    if(session['user']):
        task_dao.updateSituation(request.form['id'],request.form['situation'])
        return redirect('/')
    else:
        flash('Sua sessão expirou!','warning')
        return redirect('/login')

@app.route('/delete-task/<int:id>')
def delete_task(id):
    if(session['user']):
        task_dao.delete(id)
        return redirect('/')
    else:
        flash('Sua sessão expirou!','warning')
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=3000)