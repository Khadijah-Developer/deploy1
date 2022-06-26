from multiprocessing import context
from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.urls import reverse
# Create your views here.


def index(request):
    return render(request,'main.html')



def register(request): 
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            newUser = User()
            newUser.name =  request.POST['name']
            newUser.username =  request.POST['username']
            newUser.date =  request.POST['date']
            password  = request.POST.get('pass')
            pwHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            newUser.password = pwHash
            newUser.save()
            messages.success(request, "You register successfully!!")
            request.session['loggedin'] = newUser.id
            return redirect('/home')
    
    return redirect('/')

def home(request):
    if 'loggedin' not in request.session:
        messages.error(request,'Please Login first')
        return redirect('/')
    logged_user = User.objects.get(id = request.session['loggedin'])
    this_item = logged_user.Items.all()
    # the idea is trying to apply m:m relation in exclude() so 1st create an empty list 
    #2nd create for loop move throw all the user favorite wish list via related name and all as objects.related_name.all() ex logged_user..fav_item.all()
    #3rd use id with double "_" and in = the list  and pass it to exclude()//id__in=my_fav_list
    my_fav_list=[]
    for wish in logged_user.fav_item.all():
        my_fav_list.append(wish.id) #  my_fav_list= [1,2,3 ] 

   
    context={
        "logged_user": logged_user,
        "user_item" : this_item,
        "other_user_list" : Item.objects.exclude(user=logged_user).exclude(id__in=my_fav_list)
        
    }
    
    return render(request, 'home.html', context)


def Add_Wish(request):
    ID = request.session['loggedin']
    this_user = User.objects.get(id =ID)
    itemId = request.POST['item_id']
    other_wish = Item.objects.get(id=itemId)
    this_user.fav_item.add(other_wish)
    
    return redirect('/home')

def show(request,itemId):
    
    ID = request.session['loggedin']
    this_user = User.objects.get(id =ID)
    item_displayed = Item.objects.get(id = itemId)
    context = {
        "item_displayed": item_displayed
    }
    return render(request, "show.html", context)

def Remove_Wish(request, itemId):
    ID = request.session['loggedin']
    this_user = User.objects.get(id =ID)
    item_Id = itemId
    other_wish = Item.objects.get(id=item_Id)
    this_user.fav_item.remove(other_wish)
    
    return redirect('/home')

def Delete_Wish(request, itemId):
    item_Id = itemId
    user_wish_delete = Item.objects.get(id=item_Id)
    user_wish_delete.delete()
     
    return redirect('/home')

def login(request):
    if request.method == 'POST':
        if not request.POST['username']:
             messages.error(request,'Please enter username')
        if len(request.POST['username']) < 3 and not request.POST['username'].isalpha():
            messages.error(request,'The username should be at least 3 characters and string')
        if len(request.POST["pass"]) < 8:
             messages.error(request,'Password should be at least 8 characters!')
        else:
            password = request.POST.get('pass')
            try:
                user = User.objects.get(username=request.POST['username'])
                if bcrypt.checkpw(password. encode (), user.password.encode()) :
                    request.session['loggedin'] = user.id
                    return redirect('/home')
                else:
                    messages.error(request,'Incorrect password')

            except User. DoesNotExist:
                messages.error(request, "This username is not in the DB, please try agin or  create an account ")
    return redirect('/')

def new(request, userId):
    
    context={
        'user_add':User.objects.get(id =userId)
    }
    return render(request, 'create.html', context)

def create(request):
    ID = request.session['loggedin']
    user = User.objects.get(id =ID)

    if request.method == 'POST':
        if not request.POST['item']:
            messages.error(request,'Please enter item')
        if len(request.POST['item']) < 3:
            messages.error(request,'The item should be at least 3 characters')
        else:
            item = request.POST['item']
            user = user
            newItem = Item.objects.create(item=item, user=user)
            
            # newItem.user_fav.add(user)
            return redirect('/home')
    return redirect(reverse('new',args(user.id) ))




def logout(request):
    if 'loggedin' in request.session:
            del request.session['loggedin']
    return redirect('/')

