from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(DegreePlanTemplate)
class DegreePlanAdmin(admin.ModelAdmin):
    list_display = ['Major']


@admin.register(SemesterTemplate)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['Classes']

@admin.register(ClassListing)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'term', 'prereqs', 'coreqs', 'satisfies']

@admin.register(UserSemester)
class SemAdmin(admin.ModelAdmin):
    list_display = ['pk']

@admin.register(UserDegreePlan)
class DegPlan(admin.ModelAdmin):
    list_display = ['pk', 'Major', 'LinkedUser']