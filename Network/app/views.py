from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import post,profile,Comment
from .form import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def home(request):
    if request.method=="POST" :
        if request.user.is_authenticated:
            post.objects.create(
                author=request.user,
                content=request.POST.get("Post")
            )
            return redirect('home')
        else:
            return redirect('login')
    else:
        allCom=Comment.objects.all()
        allPost=post.objects.all().order_by('-created')
        paginator=Paginator(allPost,2)
        page_number=request.GET.get('page')
        finalPost = paginator.get_page(page_number)  # return totalpost in one page with page number and some other function
        totalpages=finalPost.paginator.num_pages  #gives total number of pages
        totalpagelist = [n+1 for n in range(totalpages)]
        context={
            'allPost': finalPost,
            'totalpagelist':totalpagelist,
            'allCom':allCom
        }
        return render(request,'home.html',context)

def likePost(request,pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            posts= get_object_or_404(post,id=request.POST.get('postId'))
            if posts.likes.filter(id=request.user.id).exists():
                posts.likes.remove(request.user)
            else:
                posts.likes.add(request.user)
     
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request,'home.html')
            
def login_view(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist()")
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is incorrect")
    context = {
        'page':page
    }
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    page = 'register'
    form = UserForm()
    if request.method == "POST":
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            profile.objects.create(
                user=user
            )
            login(request, user)
            return redirect('home')
    context={
        'form':form,
        'page':page

    }
    return render(request,'login.html',context)
def profileView(request,pk):
    human=profile.objects.get(id=pk)
    print(pk)
    posts= post.objects.filter(author= human.user)
    context={
        'human':human,
        'posts':posts
    }
    return render(request,'profile.html',context)

@login_required(login_url='/login')
def follow(request,pk):
    prof=profile.objects.get(id=pk)
    curr_user=profile.objects.get(id=request.user.id)
    if prof !=curr_user:
        if prof.followers.filter(id=request.user.id).exists():
            prof.followers.remove(request.user)
            curr_user.following.remove(prof.user)
        else:
            prof.followers.add(request.user)
            curr_user.following.add(prof.user)

    return redirect('profile',pk)

@login_required(login_url='/login')
def following(request):
    curr_user=profile.objects.get(id=request.user.id)
    userFollowers = curr_user.following.all()
    posts = post.objects.filter(author__in=userFollowers)
    allCom=Comment.objects.all()
    paginator=Paginator(posts,2)
    page_number=request.GET.get('page')
    finalPost = paginator.get_page(page_number)  # return totalpost in one page with page number and some other function
    totalpages=finalPost.paginator.num_pages  #gives total number of pages
    totalpagelist = [n+1 for n in range(totalpages)]
    context={
        'posts':finalPost ,
        'allCom':allCom,
        'totalpagelist':totalpagelist,
    }
    return render(request,'following.html',context)

@login_required(login_url='/login')
def edit(request,pk):
    selectPost=post.objects.filter(id=pk)
    if request.method =="POST":
        res=request.POST.get("Post")
        selectPost.update(content=res)
        return redirect('home')
    else:
        return render(request,'edit.html')

@login_required(login_url='/login')
def commentHandle(request,pk):
    if request.method == "POST":
        curr_post=post.objects.get(id=pk)
        comm= request.POST.get('comment')
        Comment.objects.create(
            text=comm,
            author=request.user,
            post=curr_post
        )
        return redirect('home')
    else:
        return render(request,'home.html')

