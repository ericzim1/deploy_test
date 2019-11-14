from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from datetime import date
import bcrypt

def index(request):
    
    return render(request, "app1/index.html")

def register(request):
    # check for post method
    if request.method == "POST":
    # if true
        # validate the user(in models)
        # check if any errors were return
        print("***"*40)
        print(request.POST)
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],birthdate=request.POST['birthdate'], email=request.POST['email'],password=pw_hash)
            request.session['userid']=User.objects.last().id
            return redirect('/books')
    else:
        return redirect('/')

        # if true
            # hash the password
            # create the user
            # saving the user's id in session(user_id)
            # redirect to welcome/success page
        # else
            # display errors (django messages -> from django.contrib import messages)
            # redirect to "/" index route
    # else
        # redirect to "/" index route

def login(request):
    # check for post method
    if request.method == "POST":

    # if true
        # query db with email
        user=User.objects.filter(email=request.POST['email'])
        # check the query
        if user:
        # if query true
            # found a user
            logged_user=user[0]
            # verify password from form data matches the password in db
            if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
                request.session['userid']=logged_user.id
                return redirect('/books')
            else:
                messages.warning(request, 'Invalid password/email combination.')
                return redirect('/')
            # if true
                # user is who they say they are
                # save the user_id in session
                # redirect to "/books" book index route
            # else
                # error message, invalid password/email combinations
                # redirect to "/" index route
        # else
            # email doesnt exist
            # send message to register email
            # redirect to "/" index route
        else:
            print("Email doesn't exist; re-enter email or register")
            return redirect('/')

    # false
        # redirect to "/" index route
    else:
        return redirect('/')

def books(request):
    if 'userid' not in request.session:
        return redirect('/')
    else: 
        context = {
            "user_logged_name": User.objects.get(id=request.session['userid']).first_name,
            "this_user_id": User.objects.get(id=request.session['userid']),
            "all_books": Book.objects.all(),

        }
        return render(request, 'app1/books.html', context)

def logout(request):
    request.session.clear()

    return redirect('/')

def add_book(request):
    # check for post method
    if request.method == "POST":
    # if true
        # validate the user(in models)
        # check if any errors were return
        print("***"*40)
        print(request.POST)
        print(request.session)
        errors = Book.objects.book_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/books')
        else:
            this_user=User.objects.get(id=request.session['userid'])
            Book.objects.create(title=request.POST['new_title'],desc=request.POST['new_desc'], uploaded_by=this_user)
            Book.objects.last().users_who_like.add(this_user)
            return redirect('/books')
    else:
        return redirect('/books')

def book_one(request, book_id):
    if 'userid' not in request.session:
        return redirect('/')
    else: 
        x=Book.objects.get(id=book_id)
        context = {
            "user_logged_name": User.objects.get(id=request.session['userid']).first_name,
            "this_user_id": User.objects.get(id=request.session['userid']).id,
            "book_id": x.id,
            "book_title": x.title,
            "book_desc": x.desc,
            "book_updated": x.updated_at,
            "book_created": x.created_at,
            "book_addedby": x.uploaded_by.first_name + " " + x.uploaded_by.last_name,
            "book_likedby_userlist": x.users_who_like.all()
        }

        if request.session['userid']==x.uploaded_by.id:
            return render(request, "app1/book_one.html", context)
        else:
            return render(request, "app1/book_one_noedit.html", context)

def add_fav(request):

    this_user=User.objects.get(id=request.session['userid'])
    Book.objects.get(id=request.POST['book_id']).users_who_like.add(this_user)

    return redirect('/books')

def update_book(request, book_id):
    print("***"*40)
    print(request.POST)
    x=Book.objects.get(id=book_id)
    print(x.desc)
    x.desc=request.POST['new_desc']
    x.title=request.POST['new_title']
    print(x.desc)
    x.save()

    return redirect("/books")

def unfavorite(request):
    
    unfavorite_user=User.objects.get(id=request.POST['user_to_unfavorite'])
    Book.objects.get(id=request.POST['book_to_unfavorite']).users_who_like.remove(unfavorite_user)

    return redirect(f"/books/{request.POST['book_to_unfavorite']}")

def delete_book(request, book_id):

    x=Book.objects.get(id=book_id)
    print("***"*40)
    print(x.title)
    x.delete()

    return redirect("/books")
