from django.shortcuts import render,redirect
from .models import Register
from django.db import connection
import pymysql
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse

def home(request):
    return render(request,"index.html")
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def register(request):
    if request.method=='POST':
        cursor=connection.cursor()
        username=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        contactno=int(request.POST.get('contactno'))

        try:
            cursor.execute('INSERT INTO register VALUES(%s, %s, %s , %s)',
            (username,password,email,contactno ))
            connection.commit()

            subject="Congratulations you have created an account succesfully"
            html_message = render_to_string('mail.html', {'user': username})
            plain_message = strip_tags(html_message)
            from_email = 'saitejach096@gmail.com'
            to =email
            send_mail(subject, plain_message, from_email, [to], html_message=html_message,fail_silently=False)
            msg="Succesfully Registered"
            return render(request,"register.html",{'msg':msg})
        except Exception as e:
            print(type(e),e)
            msg="Account already exists"
            return render(request,"register.html",{'msg':msg})
        finally:
            cursor.close()
    return render(request,"register.html")
def login(request):
    if request.method=='POST':
        cursor1=connection.cursor()
        username=request.POST.get('name')
        password=request.POST.get('password')
        try:
            cursor1.execute('select username,password from register where username=%s and password=%s',
            (username,password))
            connection.commit()
            msg="Logged in Succesfully"
            user=dictfetchall(cursor1)
            return render(request,"login.html",{'msg':msg})
        except:
            msg="Fail"
            return render(request,"login.html",{'msg':msg})
    return render(request,"login.html")
def forgetpassword(request):
    if request.method=='POST':
        cursor2=connection.cursor()
        username=request.POST.get('name')
        try:
            cursor2.execute(f"""select username,password,email from register where username like %s""",
            (username,))
            connection.commit()
            user=[i for i in cursor2.fetchall()]
            #print(user)
            subject="Forgotten Password "
            html_message = render_to_string('forgotpassword.html', {'user': user[0][0],'password': user[0][1]})
            plain_message = strip_tags(html_message)
            from_email = 'udaykiran9128@gmail.com'
            to =user[0][2]
            send_mail(subject, plain_message, from_email, [to], html_message=html_message,fail_silently=False)
            msg="Password sent to mail Succesfully"
            return render(request,"forgetpassword.html",{'msg':msg})
        except Exception as e:
            print(e,type(e))
            msg="Account doesnt exist with this email"
            return render(request,"forgetpassword.html",{'msg':msg})

    return render(request,"forgetpassword.html")
