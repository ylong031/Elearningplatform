from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import api
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.department_list, name='index'),
    path('courses/<int:department_id>/', views.course_list, name='course_list'),
    path('content/<int:course_id>/', views.content_list, name='content_list'),
    path('feedback/<int:course_id>/', views.feedback_list, name='feedback_list'),
    path('create_course/<int:department_id>',views.coursecreate.as_view(), name='create_course'),
    path('create_content/<int:course_id>',views.contentcreate.as_view(), name='create_content'),
    path('create_feedback/<int:course_id>',views.feedbackcreate.as_view(), name='create_feedback'),
    path('update/course/<int:course_id>', views.updatecourse.as_view(), name='update_course'),
    path('delete/course/<int:course_id>', views.deletecourse.as_view(),name='delete'),
    path('update/content/<int:content_id>', views.updatecontent.as_view(), name='update_course'),
    path('delete/content/<int:content_id>', views.deletecontent.as_view(),name='delete_content'),
    
    path('api/courses', api.CourseList.as_view(),name='courses_api'),
    path('api/students', api.StudentList.as_view(),name='student_api'),
    path('api/teachers', api.TeacherList.as_view(),name='teacher_api'),
    path('api/course/<int:pk>/', api.CourseDetails.as_view(),name='course_api'),
    
    path('chat', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login_page'),
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/', views.user_profile, name='profile'),
    path('allUsers/', views.allUsers, name='allUsers'),
    path('enrol/course/<int:course_id>', views.enrolcourse, name='enrol'),
    path('studentsEnrolled/<int:course_id>', views.studentsEnrolled, name='studentsEnrolled'),
    path('update/status/<int:user_id>', views.statusUpdate.as_view(), name='statusUpdate'),
   path('remove/student/<int:student_id>/<int:course_id>/', views.removeStudent, name='removeStudent')

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)