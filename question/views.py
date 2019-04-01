
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from .forms import UserForm
from .models import Questions, AboutQuestion
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
import random


def home(request):
    return render(request, 'question/index.html')
def about(request):
    return render(request, 'question/about.html')
def help(request):
    return render(request, 'question/help.html')

class IndexView(generic.ListView):
    template_name = 'question/index.html'
    context_object_name = 'all_question'
    def get_queryset(self):
        return Questions.objects.all()

class DetailView(generic.DetailView):
    model = Questions
    template_name = 'question/detail.html'


class QuestionListView(ListView):
    model = Questions
    template_name = 'question/detail.html'
    ordering = ['pk']
    queryset = Questions.objects.all()



class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Questions
    fields = ['subject', 'marks', 'access_modifier', 'question_text', 'is_covered']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Questions
    fields = ['author', 'subject', 'marks', 'access_modifier', 'question_text', 'is_covered']
    #template_name = 'question/questions_confirm_delete.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Questions
    success_url = reverse_lazy('question:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'question/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('question:index')

        return render(request, self.template_name, {'form':form})








class MakeQuestion(generic.ListView):
    template_name = 'question/invoice.html'
    context_object_name = 'all_question'
    def get_queryset(self):
        return Questions.objects.all()



def setQ(request):
    return render(request, 'question/questionabout.html')


class GeneratePdf(LoginRequiredMixin, View, Questions):
    def get(self, request, *args, **kwargs):

        curr_question = list(Questions.objects.filter(access_modifier='PUBLIC', subject=request.GET.get('course_title', False)) )
        author_question = list(Questions.objects.filter(author=request.user))
        #curr_question = list(Questions.objects.filte('course_no',request.GET.get('course_number', False)))



        for i in author_question:
                curr_question.append(i)

        my_set = set(curr_question)
        curr_question = list(my_set)
        temp_question = []
        sum  = 0
        tot = int(request.GET.get('marks'))
        i = 0
        n = len(curr_question)
        cur_sum = 0
        while i < n and sum < tot:
            cur_sum += int(curr_question[i].marks)
            if cur_sum > tot:
                cur_sum -= int(curr_question[i].marks)
                i += 1
                continue
            else:
                temp_question.append(curr_question[i])
                sum += int(curr_question[i].marks)
                i += 1


        need = tot - sum
        print("SUM= " + str(sum))

        if need > 0:
            for k in curr_question:
                if k not in temp_question and need >= k.marks:
                    temp_question.append(k)
                    sum += k.marks
                    need -= k.marks
                if need == 0:
                    break



       # print("sum= " + str(sum))

        random.shuffle(temp_question)

        random.shuffle(curr_question)





        data = {
            'temp_question':temp_question,
            'all_question': curr_question,
            'author_question':author_question,
            'instituion_name':request.GET.get('institution_name', False),
            'department_name':request.GET.get('department_name', False),
            'exam_name':request.GET.get('exam_name', False),
            'course_title':request.GET.get('course_title', False),
            'course_code':request.GET.get('course_code', False),
            'marks_answered':request.GET.get('marks_answered', False),
            'time':request.GET.get('time', False),
            'total_questions':request.GET.get('total_questions', False),
            'to_be_answerd':request.GET.get('to_be_answerd', False),

        }

        pdf = render_to_pdf('question/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')















class GeneratePdfDownload(View):
    def get(self, request, *args, **kwargs):
        template = get_template('question/invoice.html')

        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('question/invoice.html', context, )
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")





class AboutQuestionCreate(LoginRequiredMixin, CreateView):
    model = AboutQuestion
    all_question = Questions.objects.all()
    template_name = 'question/questions_form.html'
    fields = ['institution_name', 'subject', 'course_number', 'marks', 'time', 'total_questions', 'to_be_answerd']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def post(self, request, *args, **kwargs):
        #return render(request, "question/invoice.html", {} )
        return redirect('question:q-pdf')







