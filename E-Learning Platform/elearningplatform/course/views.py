from django.shortcuts import render
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .form import *


from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect

class mypermission(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        if self.request.user.appuser.is_teacher:
            return self.request.user.appuser.is_teacher

    def handle_no_permission(self):
       
        return render(self.request, 'course/error_page.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    allcourses = Course.objects.all()
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'course/login.html', {'allcourses': allcourses})




def register(request):
   

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST,files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'course/register.html',
                  {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered, })

def user_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'course/error_page.html')
    return render(request, 'course/profile.html')


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'course/error_page.html')
    return render(request, 'chat/index.html')

def room(request, room_name):
    if not request.user.is_authenticated:
        return render(request, 'course/error_page.html')
    return render(request, 'chat/room.html', {'room_name': room_name })

def department_list(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'course/department_list.html', context)

def course_list(request, department_id):
    department = Department.objects.get(id=department_id)
    courses = Course.objects.filter(department=department)
    context = {'department': department, 'courses': courses}
    return render(request, 'course/course_list.html', context)

def content_list(request, course_id):
    course = Course.objects.get(id=course_id)
    content = Content.objects.filter(course=course)
    context = {'course': course, 'content': content}
    return render(request, 'course/content_list.html', context)

def feedback_list(request, course_id):
    course = Course.objects.get(id=course_id)
    feedback = Feedback.objects.filter(course=course)
    context = {'course': course, 'feedback': feedback}
    return render(request, 'course/feedback_list.html', context)

def enrolcourse(request, course_id):
    if not request.user.is_authenticated:
        return render(request, 'course/error_page.html')
    
    course = Course.objects.get(id=course_id)
    request.user.appuser.courses_enrolled.add(course)
    course.students.add(request.user)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def studentsEnrolled(request, course_id):
    if not request.user.is_authenticated or not request.user.appuser.is_teacher:
        return render(request, 'course/error_page.html')
    
    course = Course.objects.get(id=course_id)
    students=course.students
    context = {'course': course, 'students':students}
    
    return render(request, 'course/studentsEnrolled.html', context)

def removeStudent(request, student_id,course_id):
    if not request.user.is_authenticated or not request.user.appuser.is_teacher:
        return render(request, 'course/error_page.html')
    
    course=Course.objects.get(id=course_id)
    student=AppUser.objects.get(id=student_id)
    student.courses_enrolled.remove(course)
    course.students.remove(student_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def allUsers(request):
    if not request.user.is_authenticated or not request.user.appuser.is_teacher:
        return render(request, 'course/error_page.html')
    
    allusers=AppUser.objects.all
    
    context = {'allusers': allusers}  
    
    return render(request, 'course/allUsers.html', context)
    

   



class deletecourse(mypermission,DeleteView):
    model = Course
    success_url = "/"
    pk_url_kwarg = 'course_id' 



#  def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['allcourse'] = Course.objects.all()
#     return context



class deletecontent(mypermission,DeleteView):
    model = Content
    success_url = "/"
    pk_url_kwarg = 'content_id' 



from django.shortcuts import get_object_or_404

class coursecreate(mypermission,CreateView):
    model = Course
    template_name = 'course/create_course.html'
    form_class = CourseForm
    success_url = "/"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, id=department_id)
        context['department'] = department
        return context
 
    def form_valid(self, form):
        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, id=department_id)
        course = form.save(commit=False)
        course.department = department
        course.user = self.request.user
        course.save()
        return super().form_valid(form)
    

class feedbackcreate(CreateView):
    model = Feedback
    template_name = 'course/create_feedback.html'
    form_class = FeedbackForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        context['course'] = course
        return context
    
    def form_valid(self, form):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        feedback = form.save(commit=False)
        feedback.course = course
        feedback.user = self.request.user
        feedback.save()
        return super().form_valid(form)
   
    

      

 
class contentcreate(mypermission,CreateView):
    model = Content
    template_name = 'course/create_content.html'
    form_class = ContentForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        context['course'] = course
        return context

    def form_valid(self, form):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        content = form.save(commit=False)
        content.course = course
        course.save()
        return super().form_valid(form)
 
    




class updatecourse(mypermission,UpdateView): 
    model=Course 
    fields=['department','title','description']
    template_name ='course/update_course.html' 
    pk_url_kwarg = 'course_id' 
    success_url = "/"

    

    

    

class updatecontent(mypermission,UpdateView): 
    model=Content 
    fields = [ 'course','title','description','file']
    template_name ='course/update_content.html' 
    pk_url_kwarg = 'content_id' 
    success_url = "/"

    def form_valid(self, form):
        new_file = self.request.FILES.get("file")
        if new_file:
            file_to_update = form.instance
            file_to_update.file = new_file
            file_to_update.save()
        return super().form_valid(form)

   
class statusUpdate(UpdateView): 
    model=AppUser 
    fields = [ 'status']
    template_name ='course/statusUpdate.html' 
    pk_url_kwarg = 'user_id' 
    success_url = "/"

   


 


    
   