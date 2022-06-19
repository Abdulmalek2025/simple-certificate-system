from ast import Sub
from django.contrib import admin
from .models import Student, Student_subject,Major, Collage, Part, Subject, Term, University
#Register your models here.
class Student_subject_inline(admin.TabularInline):
    model = Student_subject
    extra = 1
class StudentAdmin(admin.ModelAdmin):
    inlines = (Student_subject_inline,)
class SubjectAdmin(admin.ModelAdmin):
    inlines = (Student_subject_inline,)
admin.site.register(Student,StudentAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Student_subject)
admin.site.register(Major)
admin.site.register(Collage)
admin.site.register(Part)
admin.site.register(Term)
admin.site.register(University)