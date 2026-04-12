from django.contrib import admin
from .models import Complaint

admin.site.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = ('title','status','created_by','created_at')