from django.shortcuts import render,redirect
from .models import Register
from django.db import connection
import pymysql
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
import json


def home(request):
    return render(request,"index.html")

def successfull(request):
    return render(request,"sucesssell.html")

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
            return redirect(main)
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
            cursor1.execute('select username,password from register where username=%s and password=%s ',
            (username,password))
            connection.commit()
            msg="Logged in Succesfully"
            user=dictfetchall(cursor1)
            return redirect(main)
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

def buy(request):
    return render(request,"buy.html")

def buybooks(request):
    cursor3=connection.cursor()
    try:
        cursor3.execute(f"""select * from product where type='Books' and quantity>0""",
        )
        connection.commit()
        #row=cursor3.fetchall()
        results = dictfetchall(cursor3)
        print(results)
        return render(request,"buybooks.html",{'products':results})
    except Exception as e:
        print(e)
        msg="No Products Available Under this Section"
        return render(request,"buybooks.html",{'msg':msg})
    return render(request,"buy.html",{'msg':msg})

def buycalculator(request):
    cursor4=connection.cursor()
    try:
        cursor4.execute(f"""select * from product where type='Calculator' and quantity>0""",
        )
        connection.commit()
        #row=cursor3.fetchall()
        results = dictfetchall(cursor4)
        print(results)
        return render(request,"buycalculator.html",{'products':results})
    except Exception as e:
        print(e)
        msg="No Products Available Under this Section"
        return render(request,"buycalculator.html",{'msg':msg})
    return render(request,"buy.html",{'msg':msg})

def buydrafters(request):
    cursor5=connection.cursor()
    try:
        cursor5.execute(f"""select * from product where type='Drafter' and quantity>0""",
        )
        connection.commit()
        #row=cursor3.fetchall()
        results = dictfetchall(cursor5)
        print(results)
        return render(request,"buydrafter.html",{'products':results})
    except Exception as e:
        print(e)
        msg="No Products Available Under this Section"
        return render(request,"buydrafter.html",{'msg':msg})
    return render(request,"buy.html",{'msg':msg})


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(name, photo):
    try:
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO product
                          (name, photo) VALUES (%s,%s)"""

        empPicture = photo

        # Convert data into tuple format
        insert_blob_tuple = (name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        #print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except:
        print("Failed inserting BLOB data into MySQL table {}")

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def sell(request):
    if request.method=='POST':
        cursor6=connection.cursor()
        productname=request.POST.get('name')
        Type=request.POST.get('Type')
        price=int(request.POST.get('Price'))
        edition=request.POST.get('edition')
        image=request.FILES['image'].read()
        #print(image)
        insertBLOB(productname,image)
        cursor6.close()
    return render(request,"sell.html")

def addtocart(request):
    if request.method=='GET':
        cid=request.GET.get('id')
        qty=request.GET.get('quantity')
        cursor7=connection.cursor()
        cursor7.execute(f"""select * from product where id=%s and quantity>0""",
        (cid,))
        connection.commit()
        results = dictfetchall(cursor7)
        #print(results)
        cursor8=connection.cursor()
        cursor8.execute(f"""insert into cart values (%s,%s,%s,%s) """,
        (results[0]['id'],results[0]['product_name'],results[0]['price'],results[0]['quantity']))
        connection.commit()
        

    return redirect(cart)

def cart(request):
    cursor9=connection.cursor()
    cursor9.execute(f"""select * from cart""")
    results = dictfetchall(cursor9)
    total=0
    for i in results:
        total=total+int(i['qty'])*int(i['price'])
    return render(request,"addtocart.html",{'results':results ,'total':total})

def main(request):
    return render(request,"home.html")
