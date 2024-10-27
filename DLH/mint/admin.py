from django.contrib import admin
from .models import Student,Meetup,Registration, Comment
# Register your models here.

admin.site.register(Student)
admin.site.register(Meetup)
admin.site.register(Registration)
admin.site.register(Comment)

