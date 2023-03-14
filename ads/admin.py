from django.contrib import admin
from ads import models


class AdsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
    )
    list_display_links = (
        'title',
    )
    list_editable = (
        'description',
    )
    list_filter = (
        'title',
        'description',
    )
    search_fields = (
        'title',
        'description',
    )
    fieldsets = (
        ("Основное", {"fields": ('title',)}),
        ("Дополнительное", {"fields": ('description',)}),
    )


admin.site.register(models.Ad)