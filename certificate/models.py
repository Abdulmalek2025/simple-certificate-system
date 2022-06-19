from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
sex = (
    ("ذكر", "ذكر"),
    ("أنثى", "أنثى"),
)
nationals = (
    ('يمني','يمني'),
    ('سعودي','سعودي'),
)
status_choices = (
    ('مقيد','مقيد'),
    ('تخرج','متخرج'),
)
levels = (
    ('الأول','الأول'),
    ('الثاني','الثاني'),
    ('الثالث','الثالث'),
    ('الرابع','الرابع'),
)
terms = (
    ('الأول','الأول'),
    ('الثاني','الثاني'),
)
class University(models.Model):
    university_stamp = models.ImageField(null=True, blank=True)
    register_stamp = models.ImageField(null=True, blank=True)
class Term(models.Model):
    name = models.CharField(max_length=20,choices=terms,default="الأول")
    level = models.CharField(max_length=20,choices=levels,default="الأول")
    year = models.CharField(max_length=50,default=0)
    def __str__(self) -> str:
        return 'المستوى: '+self.level +'|الفصل: '+self.name+'|'+self.year
class Collage(models.Model):
    name = models.CharField(max_length=50,null=False)
    def __str__(self):
        return self.name
class Part(models.Model):
    name = models.CharField(max_length=50,null=False)
    collage = models.ForeignKey(Collage,on_delete=models.CASCADE,related_name='collage')
    def __str__(self):
        return self.name

class Major(models.Model):
    name = models.CharField(max_length=50,null=False)
    part = models.ForeignKey(Part,on_delete=models.CASCADE,related_name='part')
    def __str__(self):
        return self.name

class Student(models.Model):
    st_id = models.CharField(max_length=20,null=False)
    name = models.CharField(max_length=100,null=False)
    gender = models.CharField(max_length=9,
                  choices=sex,
                  default="ذكر")
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=100)
    national = models.CharField(max_length=20,choices=nationals,default='يمني')
    status = models.CharField(max_length=20,choices=status_choices,default='Active')
    start_date = models.CharField(max_length=50,default=0)
    current_level = models.CharField(max_length=20,choices=levels,default="First")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    major = models.ForeignKey(Major,on_delete=models.CASCADE,related_name='major')
    image = models.ImageField(null=True,blank=True)
    certificate = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
class Subject(models.Model):
    name = models.CharField('الاسم',max_length=50,null=False)
    high_mark = models.FloatField('الدرجة النهائية',null=True, blank=True)
    models.ManyToManyField(Student, related_name = 'student', through='student_subjects')
    def __str__(self):
        return self.name
class Student_subject(models.Model):
    term = models.ForeignKey(Term,on_delete=models.CASCADE,related_name='term')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subject')
    mark = models.FloatField(default=0.0)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student')
    note = models.CharField(max_length=100,default="....",null=True,blank=True)
    def __str__(self)->str:
        return self.student.name + '( ' + self.term.name+' - ' + self.subject.name+')'
    def degree(self):
        if(self.subject.high_mark == 150):
            grade = ((self.mark *2)/3)
        elif(self.subject.high_mark == 100):
            grade = self.mark
        else: grade = 150
        if (grade <= 100 and grade >= 90):
            return 'ممتاز'
        elif(grade < 90 and grade >= 80):
            return 'جيد جدا'
        elif(grade < 80 and grade >= 70):
            return 'جيد'
        elif(grade < 70 and grade >= 60):
            return 'ضعيف'
        elif(grade < 60 and grade >= 50):
            return 'مقبول'
        else:
            return 'راسب'
        

