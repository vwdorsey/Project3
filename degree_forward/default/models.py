from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ClassListing(models.Model):
    CLASS_TERM_CHOICES = (
        ('F', 'Fall Only'),
        ('S', 'Spring Only'),
        ('FS', 'Fall/Spring'),
        ('FSS', 'Fall/Spring/Summer'),
    )
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    term = models.CharField(max_length=3, choices=CLASS_TERM_CHOICES, default='FS')
    credits = models.IntegerField()
    prereqs = models.TextField(default='NONE')
    coreqs = models.TextField(default='NONE')
    satisfies = models.TextField(default='NONE')


class SemesterTemplate(models.Model):
    Classes = models.TextField(null=True)


class DegreePlanTemplate(models.Model):
    Major = models.CharField(max_length=30, primary_key=True)
    Credits = models.IntegerField()
    Semester1 = models.ForeignKey(SemesterTemplate, related_name="sem1", null=True)
    Semester2 = models.ForeignKey(SemesterTemplate, related_name="sem2", null=True)
    Semester3 = models.ForeignKey(SemesterTemplate, related_name="sem3", null=True)
    Semester4 = models.ForeignKey(SemesterTemplate, related_name="sem4", null=True)
    Semester5 = models.ForeignKey(SemesterTemplate, related_name="sem5", null=True)
    Semester6 = models.ForeignKey(SemesterTemplate, related_name="sem6", null=True)
    Semester7 = models.ForeignKey(SemesterTemplate, related_name="sem7", null=True)
    Semester8 = models.ForeignKey(SemesterTemplate, related_name="sem8", null=True)

class UserDegreePlan(models.Model):
    ENTRY_TERM_CHOICES = (
        ('F', 'Fall'),
        ('S', 'Spring'),
    )
    LinkedUser = models.ForeignKey(User)
    Major = models.CharField(max_length=30, primary_key=True)
    Entry = models.CharField(max_length=1, choices=ENTRY_TERM_CHOICES, default='F"')
    CreditsRemaining = models.IntegerField()
    Semesters = models.TextField(null=False)

class UserSemester(models.Model):
    TERM_CHOICES = (
        ('F', 'Fall'),
        ('S', 'Spring'),
        ('SS', 'Summer'),
    )
    Number = models.IntegerField()
    Term = models.CharField(max_length=2, choices=TERM_CHOICES)
    Classes = models.TextField(null=True)
