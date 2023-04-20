import base64
import re
from types import new_class
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from .import db,mail
from .models import User,Data
import io
from distutils.log import debug
from email import message
from sre_constants import SUCCESS
from flask import Flask,render_template,request

from flask_mail import Mail,Message
def render_picture(data):
    render_pic=base64.b64encode(data).decode('ascii')
    return render_pic
views =Blueprint('views',__name__)
curuser = 0
@views.route("/login",methods=['GET','POST'])
def login():
        if request.method == 'POST':
              email = request.form.get('username')
              password = request.form.get('password')
              subject="ELECTRICTY BILL PAYEMENT"
              msg="You have been successfully logged in"
              from .models import User
              user =User.query.filter_by(email=email).first()
              if user:
                    if user.password==password:
                        flash('You are successfully logged in')
                        global curuser
                        curuser=user
                        message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[email])
                        message.body=msg
                        mail.send(message)
                        success ="message sent"
                        
                        return redirect(url_for('views.home',success=success))
                    else:
                        flash("Incorrect password")
              else:
                   flash('User does not exist')
        return render_template("login.html",user=curuser)
@views.route('/logout',methods=['GET','POST'])
def logout():
    global curuser
    curuser =0
    flash('You are logged out')
    return redirect(url_for('views.login'))

@views.route('/getinfo',methods=['GET','POST'])
def getinfo():
    if(request.method=='POST'):
        cusid=request.form.get('cusid')
        new_data =Data.query.filter_by(cusid=cusid).first()
        if new_data:
            return redirect(f'/payment/{cusid}')
        else:
            return render_template('get.html')
    return render_template('get.html')


@views.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        email =request.form.get('email')
        username=request.form.get('uname')
        firstname =request.form.get('fname')
        lastname=request.form.get('lname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        subject="ELECTRICITY BILL PAYEMENT"
        msg="Thank you for signing in"
        from .models import User
        user=User.query.filter_by(email=email).first()
        if (email==""  or username =="" or firstname==""  or lastname==""  or password1=="" or password2==""):
            flash("Enter the all valid  data")
        elif user:
            flash("Alredy you have signed in")
            print("already")

        elif password1 !=password2:
            flash("password does not match")
        else:
            from .import db 
            new_user =User(username=username,firstname=firstname,email=email,password=password1,lastname=lastname,user_type="test")
            db.session.add(new_user)
            db.session.commit()
            flash("You successfully signed up")
            message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[email])
            message.body=msg
            mail.send(message)
            success ="message send"
            return render_template("login.html",success=success)
    return render_template("signup.html",user=curuser)

@views.route('/home' ,methods=['GET','POST'])
def home():
    sites = [0]
    if(request.method =='POST'):
        d=request.form.get('val')
        c=request.form.get('pre')
        q=request.form.get('languages')
        if(q=="Tamilnadu"):
            d=int(d)
            c=int(c)
            w=d-c
            if(w<0):

                a="current should be greater than previous"

            elif(w<=100):
                a="free"
        
            elif(w>100 and w<=200):
                b=w-100
                a=(b*2.5)

        

            elif(w>200 and w<=350):
                b=w-100
                a=(b*2.5)
        
            elif(w>350 and w<=500):
               b=w-100
               a=b*5
        
            else:
               b=w-100
               a=(b*7)
        
            sites = [a]
        
            return render_template("home.html",sites=sites)
        elif(q=="kerala"):
            d=int(d)
            c=int(c)
            w=d-c
            if(w<0):
                 a="current should be greater than previous"

            elif(w<=50):
                a=w*3.15
        
            elif(w>51 and w<=100):
                a=(w*3.70)

        

            elif(w>=101 and w<=150):
                a=(w*4.80)
        
            elif(w>=151 and w<=200):
              a=w*6.40
        
            elif(w>=201 and w<=250):
                a=w*7.60
            else:
                a=(w*8.80)
        
            sites = [a]
        
            return render_template("home.html",sites=sites)
        else:
            d=int(d)
            c=int(c)
            w=d-c

            w=d-c
            if(w<0):
                 a="current should be greater than previous"

            elif(w<=50):
                a=w*3.50
        
            elif(w>=51 and w<=100):
                a=(w*3.90)

        

            elif(w>=101 and w<=150):
                a=(w*5.80)
        
            elif(w>=151 and w<=200):
              a=w*7.40
        
            elif(w>=201 and w<=250):
                a=w*8.60
            else:
                a=(w*9.80)
        
            sites = [a]
        
            return render_template("home.html",sites=sites)
            

            # if(w<0):
            #     a="current should be greater than previous"

            # elif(w<=100):
            #    a="free"
        
            # elif(w>100 and w<=200):
            #    b=w-100
            #    a=(b*2.5)

        

            # elif(w>200 and w<=350):
            #    b=w-100
            #    a=(b*2.5)
        
            # elif(w>350 and w<=500):
            #   b=w-100
            #   a=b*5
        
            # else:
            #   b=w-100
            #   a=(b*7)
        
            # sites = [a]
        
            # return render_template("home.html",sites=sites)


        


    if curuser != 0:
        return render_template('home.html',sites=sites)
    else:
        return redirect(url_for('views.login'))


@views.route('/data',methods=['GET','POST'])
def data():
    if request.method =='POST':
        cusid=request.form.get('cusid')
        username=request.form.get('uname')
        firstname =request.form.get('fname')
        address=request.form.get('address')
        amount=request.form.get('amount')
        houseno=request.form.get('houseno')
        file1 = request.files['image1']
        data1 = file1.read()
        render_file1 = render_picture(data1)

        from .models import Data
        data=Data.query.filter_by(cusid=cusid).first()
        if data:
            flash("alredy")
            print("already")
        
        else:
            from .import db 
            data =Data(cusid=cusid,username=username,firstname=firstname,houseno=houseno,address=address,amount=amount,data1 = data1, rendered_data1 = render_file1)
            db.session.add(data)
            db.session.commit()
            flash("Data is successfully added")
    return render_template("add.html")
@views.route('/data/<string:cusid>')
def RetrieveSingleEmployee(cusid):
    new_data =Data.query.filter_by(cusid=cusid).first()
    if new_data:
         return render_template('data.html', employee = new_data)
    else:
        return render_template('get.html')
    return f"Employee with cusid ={cusid} Doenst exist"

@views.route('/payment/<string:cusid>')
def pay(cusid):
    new_data =Data.query.filter_by(cusid=cusid).first()
    if new_data:
        return render_template('payment.html',new_data=new_data)
    
    else:
        return render_template('get.html',new_data=new_data)  
    
@views.route('/continue/<string:cusid>')
def cont(cusid):
    new_data =Data.query.filter_by(cusid=cusid).first()
    new_data.amount=0
    db.session.commit()
    return render_template("cont.html")
@views.route('/fail')
def fail():

    return render_template("fail.html")

