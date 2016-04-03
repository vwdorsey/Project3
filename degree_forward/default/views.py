from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *


def index(request):
    useplan = DegreePlan.objects.all()
    context = {
        'plans': useplan
    }
    return render(request, 'application.html', context)

# To be replaced by a new plan and prev plan function
def plan(request):
    requestedplan = request.POST.get("plan","")
    print(request)
    if requestedplan == '':
        requestedplan = 'NONE'
    useplan = DegreePlan.objects.get(Major=requestedplan)
    plans = DegreePlan.objects.all()
    classes = ClassListing.objects.all()
    ClassString = ""
    ClassCategories = []
    for c in classes:
        codes = c.code.split(' ');
        category = ""
        for item in codes:
            if not tryint(item):
                category += item + ' '
        if category not in ClassCategories:
            ClassCategories.append(category)
        ClassString += c.code
        ClassString += ';'

    categories = ""
    for c in ClassCategories:
        categories += c + ';'

    semesters = [useplan.Semester1, useplan.Semester2, useplan.Semester3, useplan.Semester4, useplan.Semester5,
                 useplan.Semester6, useplan.Semester7, useplan.Semester8]
    classlist = []
    semCredits = []

    for s in semesters:
        semlist = s.Classes.split(';')
        semesterlist = []
        scredits = 0
        for item in semlist:
            if len(item) > 0:
                thisclass = ClassListing.objects.get(code=item)
                scredits += thisclass.credits
                semesterlist.append(thisclass)
        classlist.append(semesterlist)
        semCredits.append(scredits)

    context = {
        'categories': categories,
        'classString': ClassString,
        'allplans': plans,
        'allclasses': classes,
        'plan' : requestedplan,
        'credits' : useplan.Credits,
        'classList': classlist,
        'semCredits': semCredits
    }

    return render(request, 'plan.html', context)


def tryint(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

def makeNewDegree(request):

def loadPrevDegree(request):

def expandDegree(request):

def saveSemChanges(request):

def saveSemOrder(request):

def login(request):