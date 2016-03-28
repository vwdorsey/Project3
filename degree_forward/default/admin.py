from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(DegreePlan)
class DegreePlanAdmin(admin.ModelAdmin):
    list_display = ['Major']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['Number', 'Term', 'Classes']

@admin.register(ClassListing)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'term', 'prereqs', 'coreqs', 'satisfies']