from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_app import models
from .forms import ProfileUpdateForm
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone


# def logging(controller_func):
#     def wrapper(*args, **kwargs):
#         print(args, kwargs)
#         request: WSGIRequest = args[0]
#         print(request.META)
#
#         models.Logging.objects.create(
#             user=request.user,
#             method=request.method,
#             status=0,
#             url="",
#             description="init"
#         )
#         try:
#             response: HttpResponse = controller_func(*args, **kwargs)
#             if settings.DEBUG_LOG:
#                 models.Logging.objects.create(
#                     user=request.user,
#                     method=request.method,
#                     status=200,
#                     url="",
#                     description="Response: " + str(response.content)
#                 )
#             return response
#         except Exception as error:
#             models.Logging.objects.create(
#                 user=request.user,
#                 method=request.method,
#                 status=500,
#                 url="",
#                 description="Error: " + str(error)
#             )
#             context = {"detail": str(error)}
#             if str(error).find("query does not exist"):
#                 context["extra"] = "Такого объекта не существует"
#             return render(request, "components/error.html", context=context)
#
#     return wrapper


class CustomPaginator:
    @staticmethod
    def paginate(object_list: any, per_page=5, page_number=1):
        paginator_instance = Paginator(object_list=object_list, per_page=per_page)
        try:
            page = paginator_instance.page(number=page_number)
        except PageNotAnInteger:
            page = paginator_instance.page(number=1)
        except EmptyPage:
            page = paginator_instance.page(number=paginator_instance.num_pages)
        return page


class HomeView(View):  # TODO контроллер класс
    template_name = 'django_app/home.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'django_app/home.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, 'django_app/home.html', context=context)

# @logging
def home_view(request: HttpRequest) -> HttpResponse:  # TODO контроллер функция
    context = {}
    return render(request, 'django_app/home.html', context=context)


def home_main(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'django_app/home_main.html', context=context)

# @logging
def profile(request):
    return render(request, 'django_app/profile.html')

# @logging
def profileupdate(request):
    if request.method == 'POST':
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if pform.is_valid:
            pform.save()
            return render(request, 'django_app/profile.html')
    else:
        pform = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'django_app/profileupdate.html', {'pform': pform})

# @logging
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect(reverse('django_app:home', args=()))
    return render(request, 'django_app/register.html', context={})

# @logging
def login_(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('django_app:home_main', args=()))
        else:
            raise Exception("Логин или пароль не верны!")
    return render(request, 'django_app/login.html')

# @logging
def logout_f(request):
    logout(request)
    return redirect(reverse('django_app:login', args=()))

# @logging
def post_create(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {}
        return render(request, 'django_app/post_create.html', context=context)
    elif request.method == "POST":
        print("request: ", request)
        # print("request.data: ", request.data)
        print("request.POST: ", request.POST)
        print("request.GET: ", request.GET)
        print("request.META: ", request.META)

        title = request.POST.get('title', None)
        description = request.POST.get('description', "")
        post = models.Post.objects.create(
            title=title,
            description=description,
        )
        return redirect(reverse('django_app:post_list', args=()))

# @logging
def post_list(request: HttpRequest) -> HttpResponse:
    posts = models.Post.objects.all()

    selected_page_number_posts = request.GET.get('page', 1)
    selected_limit_objects_per_page_posts = request.GET.get('limit', 3)
    if request.method == "POST":
        selected_page_number_posts = 1
        selected_limit_objects_per_page_posts = 9999
        search_by_title_posts = request.POST.get('search', None)
        if search_by_title_posts is not None:
            posts = posts.filter(title__contains=str(search_by_title_posts))
        filter_by_user_posts = request.POST.get('filter', None)
        if filter_by_user_posts is not None:
            posts = posts.filter(user=User.objects.get(username=filter_by_user_posts))
    page_posts = CustomPaginator.paginate(
        object_list=posts, per_page=selected_limit_objects_per_page_posts, page_number=selected_page_number_posts
    )

    context = {"page_posts": page_posts, "users": User.objects.all()}
    return render(request, 'django_app/post_list.html', context=context)

# @logging
def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = models.Post.objects.get(id=pk)
    post_comment = models.PostComment.objects.filter(article=post)
    context = {"post": post,
               "comments": post_comment
               }
    return render(request, 'django_app/post_detail.html', context=context)

# @logging
def post_delete(request: HttpRequest, pk: int) -> HttpResponse:
    post = models.Post.objects.get(id=pk)
    post.delete()
    return redirect(reverse('django_app:post_list', args=()))


def post_pk_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "GET":
        context = {}
        return render(request, 'django_app/post_detail.html', context=context)
    context = {}
    return render(request, 'django_app/post_list.html', context=context)


def post_ph(request, post_id=None):
    print(post_id)
    post_new = models.Post.objects.get(id=post_id)
    comment_new = models.PostComment.objects.filter(article=post_new)
    print(comment_new)
    context = {
        "post": post_new,
        'comments': comment_new
    }
    return render(request, 'django_app/post_detail.html', context)


# @logging
def post_comment_create(request, pk):
    models.PostComment.objects.create(
        article=models.Post.objects.get(id=pk),
        author=request.user,
        description=request.POST.get("description", ""),
    )

    return redirect(reverse('django_app:post_detail', args=(pk,)))

    if request.method == "POST":
        pass
    if request.method == "GET":
        pass

    pass


def post_comment_delete(request: HttpRequest, pk: int) -> HttpResponse:
    comment = models.PostComment.objects.get(id=pk)
    pk = comment.article.id
    comment.delete()
    return redirect(reverse('django_app:post_detail', args=(pk,)))


def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        models.Todo.objects.create(
            author=User.objects.get(id=1),
            title=title,
            description=description,
            is_completed=False,
        )
        return redirect(reverse('django_app:todo_read_list', args=()))
    context = {
    }
    return render(request, 'django_app/todo_create.html', context)


def todo_read(request, todo_id=None):
    todo = models.Todo.objects.get(id=todo_id)
    context = {
        "todo": todo
    }
    return render(request, 'django_app/todo_detail.html', context)


def todo_read_list(request):

    is_detail_view = request.GET.get("is_detail_view", True)
    if is_detail_view == "False":
        is_detail_view = False
    elif is_detail_view == "True":
        is_detail_view = True
    todo_list = models.Todo.objects.all()

    def paginate(objects, num_page):
        paginator = Paginator(objects, num_page)
        pages = request.GET.get('page')
        try:
            local_page = paginator.page(pages)
        except PageNotAnInteger:
            local_page = paginator.page(1)
        except EmptyPage:
            local_page = paginator.page(paginator.num_pages)
        return local_page

    page = paginate(objects=todo_list, num_page=3)
    context = {
        "page": page,
        "is_detail_view": is_detail_view
    }
    return render(request, 'django_app/todo_list.html', context)


def todo_update(request, todo_id=None):
    if request.method == 'POST':
        todo = models.Todo.objects.get(id=todo_id)
        is_completed = request.POST.get("is_completed", "")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        if is_completed:
            if is_completed == "False":
                todo.is_completed = False
            elif is_completed == "True":
                todo.is_completed = True
        if title and title != todo.title:
            todo.title = title
        if description and description != todo.description:
            todo.description = description
        todo.updated = timezone.now()
        todo.save()
        return redirect(reverse('django_app:todo_read_list', args=()))
    todo = models.Todo.objects.get(id=todo_id)
    context = {
        "todo": todo
    }
    return render(request, 'django_app/todo_change.html', context)


def todo_delete(request, todo_id=None):
    models.Todo.objects.get(id=todo_id).delete()
    return redirect(reverse('django_app:todo_read_list', args=()))
