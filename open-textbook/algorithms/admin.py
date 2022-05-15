from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from .models import Solution

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('__all__')

admin.site.register(Solution, PostAdmin)