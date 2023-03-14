from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from . import models
from .models import Ad
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse


class CustomPaginator:
    @staticmethod
    def paginate(object_list: any, per_page=9, page_number=1):
        paginator_instance = Paginator(object_list=object_list, per_page=per_page)
        try:
            page = paginator_instance.page(number=page_number)
        except PageNotAnInteger:
            page = paginator_instance.page(number=1)
        except EmptyPage:
            page = paginator_instance.page(number=paginator_instance.num_pages)
        return page


def ad_list(request: HttpRequest) -> HttpResponse:
    ads = models.Ad.objects.all()
    selected_page_number_ads = request.GET.get('page', 1)
    selected_limit_objects_per_page_ads = request.GET.get('limit', 9)
    if request.method == "POST":
        selected_page_number_ads = 1
        selected_limit_objects_per_page_ads = 9999
        search_by_title_ads = request.POST.get('search', None)
        if search_by_title_ads is not None:
            ads = ads.filter(title__contains=str(search_by_title_ads))
        filter_by_user_ads = request.POST.get('filter', None)
        if filter_by_user_ads is not None:
            ads = ads.filter(user=User.objects.get(username=filter_by_user_ads))
    page_ads = CustomPaginator.paginate(
        object_list=ads, per_page=selected_limit_objects_per_page_ads, page_number=selected_page_number_ads
    )

    context = {"page_ads": page_ads, "users": User.objects.all()}
    return render(request, 'ads/ad_list.html', context=context)


def ad_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        Ad.objects.create(title=title, description=description, price=price)
        return redirect('ad_list')
    else:
        return render(request, 'ads/ad_create.html')


def ad_delete(request: HttpRequest, pk: int) -> HttpResponse:
    ad = models.Ad.objects.get(id=pk)
    ad.delete()
    return redirect(reverse('ad_list', args=()))
