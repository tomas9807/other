from . import app
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
    posts = execute_sql_statement(operation='select id_user as author,title,content,date_posted from posts',to_return=True,dictionary=True,buffered=True)
    return render_template('index.html',**locals())

@app.route('/register',methods=['GET','POST'])
def register():
    title = 'register'
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        execute_sql_statement(
            operation = """insert into users(username,email,password,date_posted) values (%s,%s,%s,%s)""",
            params=  (username,email,password),
            message= f'Account created for {form.username.data}')

        return redirect(url_for('index'))   
    return render_template('register.html',**locals())

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
