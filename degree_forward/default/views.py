from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader
from .models import *


def index(request):
    if request.user.is_authenticated():
        return redirect('/landing/',request);
    else:
        return render(request, 'application.html')

def register(request):
    username = request.POST.get('username')
    password1 = request.POST.get('pass1')
    password2 = request.POST.get('pass2')
    if password1 == password2:
        User.objects.create_user(username=username, email=None, password=password1)
        return render(request, 'application.html')
    else:
        error = "The passwords you have entered don't match."
        context = {error}
        return render(request, 'application.html', context)

def auth(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/landing/', request)
        else :
            error = "Invalid Username or Password."
            context = {error}
            render(request, 'application.html', context)

def landing(request):
    if request.user.is_authenticated():
        udl = getUserDegreeList(request.user.id)
        dl = getTemplateList()
        context = {'uname': request.user.username,
                   'degList': udl,
                   'tempList': dl}

        return render(request, 'landing.html', context)
    else:
        return render(request, 'application.html')

def getUserDegreeList(id):
    planListings = []
    try:
        plans = UserDegreePlan.objects.get(LinkedUser=id);
        for plan in plans:
            planListings.append(plan.Major)
        return planListings
    except ObjectDoesNotExist as e:
        planListings.append("No Degrees Created.")
        return planListings


def getTemplateList():
    plans = DegreePlanTemplate.objects.all()
    templates = []
    for I in plans:
        templates.append(I.Major)

    if templates.count == 0:
        templates.append('No Degrees Available')

    return templates


# To be replaced by a new plan and prev plan function
def plan(request):
    requestedplan = request.POST.get("plan","")
    if requestedplan == '':
        requestedplan = 'NONE'
    useplan = DegreePlanTemplate.objects.get(Major=requestedplan)


def tryint(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

def makeNewDegree(request):
    requestedplan = request.POST.get("plan", "")
    if requestedplan == '':
        requestedplan = 'NONE'
    useplan = DegreePlanTemplate.objects.get(Major=requestedplan)
    newUserPlan = UserDegreePlan.objects.create()
    newUserPlan.Major = useplan.Major
    newUserPlan.CreditsRemaining = useplan.Credits
    newUserPlan.save()
    return expandDegree(newUserPlan)


def loadPrevDegree(request):
    requestedplan = request.POST.get("planID", "")
    if requestedplan == '':
        requestedplan = 'NONE'
    useplan = UserDegreePlan.objects.get(pk=requestedplan);
    if useplan.LinkedUser == request.user.id:
        expandDegree(useplan, request)
    else:
        error = "The degree you tried to load doesn't belong to you. If this is in error, please report to devs."
        context = { error }
        render(request, 'landing.html', context)


def expandDegree(useplan, request):
    plans = DegreePlanTemplate.objects.all()
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
        'plan': useplan,
        'credits': useplan.Credits,
        'classList': classlist,
        'semCredits': semCredits
    }

    return render(request, 'plan.html', context)

#def saveSemChanges(request):

#def saveSemOrder(request):
