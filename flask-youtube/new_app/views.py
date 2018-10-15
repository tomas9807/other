from . import app,bcrypt,login_manager
from flask import render_template,redirect,url_for,request,flash
from datetime import date,timedelta
from .forms import RegistrationForm,LoginForm,NewPostForm
from mysql import connector
from contextlib import closing


def execute_sql_statement(*,operation,params=None,message=None,to_return=False,**cursor_kwargs):

    with closing(connector.connect(**app.config['MYSQL_CONFIG'])) as conn:
        cur = conn.cursor(**cursor_kwargs)
        
        try:
                cur.execute(
                    operation=operation,
                    params=params
                    )
                
                conn.commit()
                
                if to_return:
                    return cur.fetchall()
    
        except connector.Error as e:
            print(e)
            conn.rollback()
   
            if message:
                flash(f'Something went wrong with the operation {e}',category='danger')
        else:
            if message:
                flash(message,category='success')
        finally:
                cur.close()


@app.route('/')
def index():
    title = 'home'
    posts = execute_sql_statement(
    operation="""select users.username as author,posts.title,posts.content,posts.date_posted from posts
    inner join users on users.id=posts.id_user
    """,
    to_return=True,
    dictionary=True,
    buffered=True)
    return render_template('index.html',**locals())

@app.route('/register',methods=['GET','POST'])
def register():
    title = 'register'
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        hashed_passwd = bcrypt.generate_password_hash(password).decode('utf-8')
        execute_sql_statement(
            operation = """insert into users(username,email,password) values (%s,%s,%s)""",
            params=  (username,email,hashed_passwd),
            message= f'Account created for {form.username.data}')

        return redirect(url_for('index'))   
    return render_template('register.html',**locals())

@app.route('/login',methods=['GET','POST'])
def login():
    title = 'login'
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
     
        data = execute_sql_statement(
            operation = """select password from users where email=%s""",
            params=  (email,),
            to_return=True,
            buffered=True
            )
        if data and data[0]:
            user_passwd = data[0]
            if bcrypt.check_password_hash(user_passwd,password):
                return redirect(url_for('index'))   
    return render_template('login.html',**locals())

@app.route('/newpost',methods=['GET','POST'])
def newpost():
    title = 'new post'
    form = NewPostForm()
 
    if request.method=='POST' and form.validate_on_submit():
        post_title = form.title.data
        post_content = form.content.data
        post_date_posted = form.date_posted.data

        execute_sql_statement(
            operation = """insert into posts(id_user,title,content,date_posted) values(%s,%s,%s,%s)""",
             params=   (1,post_title,post_content,post_date_posted),
             message= 'Post succesfully created')
     
        return redirect(url_for('index'))
    return render_template('newpost.html',**locals())
