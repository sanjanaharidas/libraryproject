from django.shortcuts import render
from django.http import HttpResponse
from books.models import Book
from django.db.models import Q
from books.forms import Bookform
from django.contrib.auth.decorators import login_required
#Create your views here.
def home(request):
    return render(request, 'home.html')
@login_required
def bookdetail(request,p):
    b=Book.objects.get(id=p)
    return render(request,'book.html',{'b':b})
@login_required
def bookdelete(request,p):
    b=Book.objects.get(id=p)
    b.delete()
    return viewbook(request)
@login_required
def bookedit(request,p):
    b = Book.objects.get(id=p)
    if (request.method == "POST"):  # after submission
        form = Bookform(request.POST,request.FILES,instance=b)  # Creates form object initialised with values inside request.POST
        if form.is_valid():
            form.save()  # saves the form object inside Db table
        return viewbook(request)

    form=Bookform(instance=b)  #retrieved data will be filled
    return render(request,'edit.html',{'form':form})
@login_required
def search(request):
    query=""
    b=None
    if(request.method=="POST"):
        query=request.POST['q']
        if(query):
            b=Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

    return render(request,'search.html',{'query':query,'b':b})
@login_required
def addbook(request):#userdefined
    if(request.method=="POST"):
        t = request.POST['t']
        a = request.POST['a']
        p = request.POST['p']
        f = request.FILES['f']
        i = request.FILES['i']
        b = Book.objects.create(title=t,author=a,price=p,pdf=f,cover=i)
        b.save()
        return viewbook(request)
    return render(request, 'addbook.html')
@login_required
def addbooks1(request):#built in
    if(request.method=="POST"):#After form submission
        form=Bookform(request.POST)#creates form object initialized with values inside request.POST
        if form.is_valid():
            form.save()#saves the form object inside the DB table
        return viewbook(request)

    form=Bookform()#create empty form object with no values
    return render(request, 'addbooks1.html',{'form':form})

@login_required
def viewbook(request):
    k=Book.objects.all()
    return render(request, 'viewbook.html',{'b':k})
# @login_required
# def factorial(request):
#
#     if(request.method=="POST"):
#         num=int(request.POST['n'])
#         f=1
#         for i in range(1,num+1):
#             f=f*i
#         return render(request,'factorial.html',{'factorial':f})
#     return render(request,'factorial.html')