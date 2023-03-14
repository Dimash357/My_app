from django.urls import path, re_path
from django_app import views

app_name = 'django_app'
urlpatterns = [
    path('', views.home_view, name=''),
    path('index/', views.HomeView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('home_main/', views.home_main, name='home_main'),


    path('register/', views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_f, name='logout'),


    # path('post/ratings/', views.posts),
    path('post_list/', views.post_list, name='post_list'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/detail/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/delete/', views.post_comment_delete, name='post_comment_delete'),
    path('post_create/', views.post_create, name='post_create'),

    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profileupdate, name='profile_update'),

    path('post_comment_create/<int:pk>/', views.post_comment_create, name='post_comment_create'),

    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/<int:todo_id>/', views.todo_read, name='todo_read'),
    path('todo/list/', views.todo_read_list, name='todo_read_list'),
    path('todo/<int:todo_id>/update/', views.todo_update, name='todo_update'),
    re_path(r'^todo/(?P<todo_id>\d+)/delete/$', views.todo_delete, name='todo_delete'),

]