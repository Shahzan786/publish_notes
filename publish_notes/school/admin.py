from django.contrib import admin

# Register your models here.
from .models import School, Teacher, Class, Student , Note , Announcement

admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Note)
admin.site.register(Announcement)