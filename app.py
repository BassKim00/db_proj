from flask import Flask, request, session, redirect, url_for, render_template, flash
from forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm


import pymysql
import json
import os


SECRET_KEY = os.urandom(32)
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = SECRET_KEY

# DATABASE SET
db = pymysql.connect(host='skkeam.catfginrtsc0.ap-northeast-2.rds.amazonaws.com',
                     port=3306,
                     user='operat93',
                     passwd='rlaalsdud1!',
                     db='innodb',
                     charset='utf8')


# Main Index
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    if 'current_user' in session:
        data = get_user_info(session['current_user'])

        return render_template('/index.html', data=data)
    else:
        return redirect(url_for('login', _method='GET'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit() or request.method == 'POST':
        cursor = db.cursor()
        sql = """SELECT * FROM USER WHERE U_id = '%s'""" % (form.user_id.data)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        # ID Chcek
        if len(result) is 0:
            flash("Unknown ID. Check Your ID")
            return render_template('/login.html', form=form)

        # Password Check
        if result[0][1] == form.password.data:
            session['current_user'] = form.user_id.data
            return redirect(url_for('index', _method='GET'))
        else:
            flash("Unknown Password. Check Your Password")
            return render_template('/login.html', form=form)
    else:
        return render_template('/login.html', form=form)


# Register
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit() or request.method == 'POST':
        if form.password1.data == form.password2.data:
            # ask is there an ID
            cursor = db.cursor()
            sql = """SELECT * FROM USER WHERE U_id = '%s'""" % (form.user_id.data)
            cursor.execute(sql)
            result = cursor.fetchall()

            # ID Chcek
            if len(result) is not 0:
                flash("ID is already use. please in another ID.")
                return render_template('/register.html', form=form)
            else:
                sql = """INSERT INTO USER VALUES ('%s', '%s', '%s', '%s', 1, 0)""" \
                      % (form.user_id.data, form.password1.data, form.email.data, form.phone.data)
                cursor.execute(sql)
                db.commit()
                cursor.close()

                return render_template('/login.html', form=LoginForm())
        else:
            flash("Password, Password Confirm is not same. Check Your Password")
            return render_template('/register.html', form=form)

    return render_template('register.html', form=form)


# Logout
@app.route("/logout")
def logout():
    del session['current_user']
    return redirect(url_for('login'))


# Forgot Password
@app.route("/forgot", methods=['GET', 'POST'])
def forgot():
    form = ForgotPasswordForm()
    if form.validate_on_submit() or request.method == 'POST':
        cursor = db.cursor()
        sql = """SELECT * FROM USER WHERE U_id = '%s' AND Email = '%s'""" \
              % (form.user_id.data, form.email.data)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        # ID Chcek
        if len(result) is 1:
            session['forgot_user'] = form.user_id.data
            return redirect(url_for('reset'))

    return render_template('forgot.html', form=form)


# Reset Password
@app.route("/reset", methods=['GET', 'POST'])
def reset():
    form = ResetPasswordForm()
    if form.validate_on_submit() or request.method == 'POST':
        cursor = db.cursor()
        sql = """SELECT * FROM USER WHERE U_id = '%s'""" % (session['forgot_user'])
        cursor.execute(sql)
        result = cursor.fetchall()

        # ID Chcek
        if len(result) is 1:
            sql = """UPDATE USER SET PW = '%s' WHERE U_id = '%s'"""\
                  % (session['forgot_user'], form.password1.data)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            return redirect(url_for('login'))

    return render_template('reset.html', form=form)


#Page Friend
@app.route("/friend", methods=['GET', 'POST'])
def friend():
    data=None
    if 'current_user' in session:
        data = get_user_info(session['current_user'])

        return render_template('/page_friend.html', data=data)

    return render_template('/page_friend.html', data=data)


# Page Library
@app.route("/library", methods=['GET','POST'])
def library():
    data=None
    if 'current_user' in session:
        data = get_user_info(session['current_user'])

        return render_template('/page_library.html', data=data)

    return render_template('/page_library.html', data=data)


# Page Pocket
@app.route("/pocket", methods=['GET','POST'])
def pocket():
    data=None
    form = LoginForm()
    if 'current_user' in session:
        data = get_user_info(session['current_user'])

        return render_template('/page_pocket.html', data=data)

    return render_template('/login.html', form=form)

@app.route("/purchase",methods=['GET','POST'])
def purchase():
    data=get_user_info(session['current_user'])
    cursor = db.cursor()
    if request.args['G_id'] is None:
        return render_template('/page_pocket.html', data=data)
    else:
        sql = """INSERT INTO LIBRARY VALUES('%s','%s');""" % (session['current_user'],request.args['G_id'])
        cursor.execute(sql)
        db.commit()
        sql = """DELETE FROM POCKET WHERE U_id='%s' and G_id='%s';""" % (session['current_user'],request.args['G_id'])
        cursor.execute(sql)
        db.commit()
        cursor.close()
        data = get_user_info(session['current_user'])
        return render_template('/page_pocket.html', data=data)

@app.route("/purchase2",methods=['GET','POST'])
def purchase2():
    data=get_user_info(session['current_user'])
    cursor = db.cursor()
    if request.args['G_id'] is None:
        return render_template('/index.html', data=data)
    else:
        sql = """INSERT INTO LIBRARY VALUES('%s','%s');""" % (session['current_user'],request.args['G_id'])
        cursor.execute(sql)
        db.commit()
        cursor.close()
        data = get_user_info(session['current_user'])
        return render_template('/index.html', data=data)


@app.route("/putin",methods=['GET','POST'])
def putin():
    data=get_user_info(session['current_user'])
    cursor = db.cursor()
    if request.args['G_id'] is None:
        return render_template('/index.html', data=data)
    else:
        sql = """INSERT INTO POCKET VALUES('%s','%s');""" % (session['current_user'],request.args['G_id'])
        cursor.execute(sql)
        db.commit()
        cursor.close()
        data = get_user_info(session['current_user'])
        return render_template('/index.html', data=data)



# Get Index Data
def get_user_info(user_id):

    cursor = db.cursor()
    # get user data
    sql = """SELECT * FROM USER WHERE U_id = '%s'""" % (user_id)
    cursor.execute(sql)
    user_data = cursor.fetchall()

    # get library data
    sql = """select L.G_id, G.production, G.category, G.gerne
             from USER U,LIBRARY L, GAME G
             where U.U_id = '%s' and U.U_id = L.U_id and L.G_id = G.title
            """ % (user_id)
    cursor.execute(sql)
    lib_data = cursor.fetchall()

    # get friends data
    sql = """SELECT * FROM FRIENDS WHERE U_id = '%s'""" % (user_id)
    cursor.execute(sql)
    friend_data = cursor.fetchall()

    #get pocket data
    sql = """select P.G_id, G.production, G.category, G.gerne, G.price
             from USER U,POCKET P, GAME G
             where U.U_id = '%s' and U.U_id = P.U_id and P.G_id = G.title
             """ % (user_id)
    cursor.execute(sql)
    pocket_data = cursor.fetchall()

    # get game data
    sql = """SELECT * FROM GAME"""
    cursor.execute(sql)
    game_data = cursor.fetchall()

    result = {'user_data': {'cash': user_data[0][5]}, 'lib_data': {'count': len(lib_data), 'data': lib_data},'friend_data': {'count': len(friend_data), 'data':friend_data},
              'pocket_data': {'count': len(pocket_data), 'data': pocket_data}, 'game_data': {'data': game_data}}
    cursor.close()
    return result


if __name__ == '__main__':
    app.run(debug=True)
