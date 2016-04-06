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

def getUserDegreeList(uid):
    planList = []
    try:
        plans = UserDegreePlan.objects.filter(LinkedUser=uid)
        for plan in plans:
            planList.append(plan)
        return planList
    except ObjectDoesNotExist as e:
        planList.append("No Degrees Created.");
        return planList


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
    if (requestedplan == '') or (requestedplan == 'No Degrees Available'):
        error = 'You must select a degree.'
        context = {error}
        return render(request, 'landing.html', context)
    entry = request.POST.get("entry", "")
    if entry == '':
        error = 'You must select an entry semester.'
        context = {error}
        return render(request, 'landing.html', context)
    useplan = DegreePlanTemplate.objects.get(Major=requestedplan)
    semesters = []

    semesters.append(useplan.Semester1)
    semesters.append(useplan.Semester2)
    semesters.append(useplan.Semester3)
    semesters.append(useplan.Semester4)
    semesters.append(useplan.Semester5)
    semesters.append(useplan.Semester6)
    semesters.append(useplan.Semester7)
    semesters.append(useplan.Semester8)

    planEntry = ''
    idString = ''
    if entry == 'Fall':
        planEntry = 'F'
    else:
        planEntry = 'S'

    semEntry = planEntry
    for i in range(0, 8):
        newSem = UserSemester.objects.create()
        newSem.Number = i
        newSem.Term = semEntry
        newSem.Classes = semesters[i]
        newSem.save()
        idString += str(newSem.pk) + ';'
        if semEntry == 'S':
            semEntry = 'F'
        else:
            semEntry = 'S'

    newUserPlan = UserDegreePlan.objects.create(LinkedUser=request.user, Major=useplan.Major, Entry=planEntry,
                                                CreditsRemaining=useplan.Credits, Semesters=idString)
    newUserPlan.save()
    return expandDegree(newUserPlan, request)


def loadPrevDegree(request):
    requestedplan = request.POST.get("plan", "")
    if requestedplan == 'No Degrees Available':
        error = 'You have no degrees available to select.'
        context = {error}
        return render(request, 'landing.html', context)
    planNum = int(requestedplan)
    useplan = UserDegreePlan.objects.get(pk=planNum)
    if useplan.LinkedUser == request.user:
        return expandDegree(useplan, request)
    else:
        error = "The degree you tried to load doesn't belong to you. If this is in error, please report to devs."
        context = {error}
        return render(request, 'landing.html', context)


def expandDegree(useplan, request):
    #plans = DegreePlanTemplate.objects.all()
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
    ClassCategories.sort()
    categories = ""
    for c in ClassCategories:
        categories += c + ';'

    semesters = []
    semIdString = useplan.Semesters
    semIds = semIdString.split(';')
    for i in semIds:
        if i != '':
            semesters.append(UserSemester.objects.get(id=int(i)))

    classlist = []
    semCredits = []

    for s in semesters:
        semlist = s.Classes.split(';')
        semesterlist = []
        scredits = 0
        for item in semlist:
            if len(item) > 0 and item != 'NONE':
                thisclass = ClassListing.objects.get(code=item)
                scredits += thisclass.credits
                semesterlist.append(thisclass)
        classlist.append(semesterlist)
        semCredits.append(scredits)

    context = {
        'categories': categories,
        'classString': ClassString,
        'allclasses': classes,
        'plan': useplan,
        'credits': useplan.CreditsRemaining,
        'classList': classlist,
        'semCredits': semCredits
    }

    return render(request, 'plan.html', context)

def addClass(request):
    planID = request.POST.get("post","")
    semester = request.POST.get("semester","")
    classcode = request.POST.get("classcode","")
    plan = UserDegreePlan.objects.get(pk=planID)
    requestedclass = ClassListing.objects.get(code=classcode)
    destSemester = UserSemester.objects.get(pk=semester)
    status = 'OK'

    if destSemester.Credits == 21 or (destSemester.Credits + requestedclass.credits > 21):
        status = 'WARN-CROB'

    if requestedclass.prereqs is not None or requestedclass.coreqs is not None:
        sems = plan.Semesters.split(';')
        prereqs = ""
        coreqs = ""
        classCoReqs = requestedclass.prereqs.split(';')
        classPreReqs = requestedclass.coreqs.split(';')
        for i in range(0,destSemester):
            sem = UserSemester.objects.get(pk=sems[int(i)])
            if i <= destSemester-2:
                prereqs = sem.Classes
            if i <= destSemester-1:
                coreqs = sem.Classes

        for cc in classCoReqs:
            if cc not in coreqs:
                status = 'FAIL-COREQ-'+cc
                return status

        for cc in classPreReqs:
            if cc not in prereqs:
                status = 'FAIL-PREREQ-'+cc
                return status

    destSemester.Classes += requestedclass.code + ';'
    destSemester.Credits += int(requestedclass.credits)
    destSemester.save()
    return HttpResponse(status)

def removeClass(request):
    semester = request.POST.get("semester", "")
    classcode = request.POST.get("classcode", "")
    requestedclass = ClassListing.objects.get(code=classcode)
    destSemester = UserSemester.objects.get(pk=semester)
    status = 'OK'



#def saveSemChanges(request):

#def saveSemOrder(request):
