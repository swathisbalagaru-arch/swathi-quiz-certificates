from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student_name", "category", "score", "total", "certificate_id", "created_at")
    search_fields = ("student_name", "certificate_id")
    list_filter = ("category",)
