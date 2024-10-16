from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Task
from app import mysql  # Agora o mysql será importado corretamente, sem circularidade

# Definindo um Blueprint chamado 'main'
main = Blueprint('main', __name__)


# Send Email

from flask_mail import Message
from app import mail

def send_task_reminder(user_email, task_description):
    msg = Message("Lembrete de Tarefa", sender="seuemail@dominio.com", recipients=[user_email])
    msg.body = f"Não se esqueça de completar sua tarefa: {task_description}"
    mail.send(msg)



#Profile

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        User.update_profile(current_user.id, new_username, new_password)
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('main.profile'))

    return render_template('profile.html', user=current_user)


# Rota de registro
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('main.login'))
    return render_template('register.html')

# Rota de login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user_by_username(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.tasks'))
        else:
            flash('Credenciais incorretas!', 'danger')  # Notificação se as credenciais estiverem incorretas
    return render_template('login.html')

# Rota de logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você foi desconectado!", "info")  # Notificação ao fazer logout
    return redirect(url_for('main.login'))

# Rota para listar e adicionar tarefas
@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task_description = request.form['description']
        Task.create_task(task_description, current_user.id)
        flash("Tarefa adicionada com sucesso!", "success")
    
    # Paginação
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Defina quantas tarefas serão exibidas por página
    search = request.args.get('search')

    if search:
        tasks = Task.search_tasks_by_user(current_user.id, search, page, per_page)
    else:
        tasks = Task.get_paginated_tasks_by_user(current_user.id, page, per_page)

    return render_template('tasks.html', tasks=tasks, page=page)

# Rota para remover tarefas
@main.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    Task.delete_task(task_id)
    flash("Tarefa removida com sucesso!", "danger")  # Notificação após remover tarefa
    return redirect(url_for('main.tasks'))

@main.route('/tasks/confirm_delete/<int:task_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete_task(task_id):
    # Exibir a tarefa antes de confirmar a exclusão
    task = Task.get_task_by_id(task_id)
    
    if request.method == 'POST':
        Task.delete_task(task_id)
        flash("Tarefa removida com sucesso!", "danger")  # Notificação após remover tarefa
        return redirect(url_for('main.tasks'))

    return render_template('confirm_delete.html', task=task)


# Rota para alternar o status de uma tarefa (completa/não completa)
@main.route('/tasks/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    Task.toggle_task_completion(task_id)
    flash("Status da tarefa atualizado com sucesso!", "info")  # Notificação após alternar status
    return redirect(url_for('main.tasks'))



# Modo escuro

from flask import make_response

@main.route('/toggle_theme')
def toggle_theme():
    theme = request.cookies.get('theme', 'light')
    new_theme = 'dark' if theme == 'light' else 'light'
    resp = make_response(redirect(url_for('main.tasks')))
    resp.set_cookie('theme', new_theme)
    return resp



# Rota para o index (página inicial)
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.tasks'))
    return render_template('index.html')
