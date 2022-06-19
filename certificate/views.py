from inspect import Parameter
from django.db.models import Count
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student,Student_subject, Term,University
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import datetime
from django.db.models import Sum
# Create your views here.
def home(request):
    return render(request,'home.html')
@login_required
def students(request):
    students = Student.objects.all()
    context = {'students':students,}
    return render(request,'students.html',context=context)

@login_required
def main(request):
    if request.user.is_superuser:
        students = Student.objects.all()
        context = {'students':students,}
        return render(request,'students.html',context=context)
    else:
        if(request.method == "POST" and request.POST.get('term') != ''):
            term_id = request.POST.get('term')
            term = Term.objects.filter(id=term_id).get()
        else:
            term_id = 0 
            term = ''
        student = Student.objects.get(user__pk=request.user.id)
        terms_id = Student_subject.objects.filter(student__pk=student.pk).values_list('term', flat=True).distinct()
        terms = Term.objects.filter(pk__in=terms_id)
        marks = Student_subject.objects.filter(term__pk=term_id,student__pk=student.pk)
        context = {'student':student,'terms':terms,'marks':marks,'cterm':term,'term_id':term_id}
        return render(request,'student.html',context=context)
@login_required
def GeneratePDF(request,id):
    if(id>0):
        student = Student.objects.get(user__pk=request.user.id)
        term = Term.objects.filter(id=id).get()
        marks = Student_subject.objects.filter(term__pk=id,student__pk=student.pk)
        university = University.objects.first()
        total = 0
        grade = 0
        count = 0
        for mark in marks:
            count = count +1
            total = total + mark.mark
            grade = grade + ((mark.mark*2)/3)
        response = HttpResponse(content_type='application/pdf')
        grade = grade /count
        degree = ''
        if grade <= 100 and grade >= 90:
            degree = 'ممتاز'
        elif grade < 90 and grade >= 80:
            degree = 'جيدجدا'
        elif grade < 80 and grade >=70:
            degree = 'جيد'
        elif grade < 70 and grade >= 60:
            degree = 'ضعيف'
        elif grade < 60 and grade >=50:
            degree = 'مقبول'
        else:
            degree = 'راسب'

        response['Content-Disposition'] = 'inline; attachment; filename=invoice_'+ str(datetime.datetime.now())+'.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        html_string = render_to_string('certificate.html',{'student':student,'marks':marks,'term':term,'total':total,'grade':grade,'degree':degree,'university':university})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())

        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()

            output = open(output.name,'rb')
            response.write(output.read())
        return response
    else:
        return render(request,'error.html')
        