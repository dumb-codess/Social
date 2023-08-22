from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth.models import User
from .models import post,profile,Comment
from .form import UserForm
import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
def home(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            print("hello")
            post.objects.create(
                author=request.user,
                content=request.POST.get('Post')
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
    
@login_required(login_url='/login')
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        is_liked = request.POST.get('is_liked')
        try:
            posts = get_object_or_404(post, id=post_id)
            if is_liked == 'no':
                posts.likes.add(request.user)
                is_liked = 'yes'
            elif is_liked == 'yes':
                posts.likes.remove(request.user)
                is_liked = 'no'
            # posts.save()
            print("hello")
            return JsonResponse({'like_count': post.likes.through.objects.count(), 'is_liked': is_liked, "status": 201})
        except:
            logger = logging.getLogger(__name__)
            print("hello2")
            logger.exception("An exception occurred:")
            return JsonResponse({'error': "Post not founds", "status": 404})
    return JsonResponse({}, status=400)


            
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
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        login(request, user)
        return redirect('home')
    context={
        'page':page

    }
    return render(request,'login.html',context)
def profileView(request,pk):
    human=profile.objects.get(id=pk)
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
def edit(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new_post = request.POST.get('post')
        try:
            posts = post.objects.get(id=post_id)
            if posts.author == request.user:
                posts.text = new_post.strip()
                posts.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)

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

