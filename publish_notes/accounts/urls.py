from django.urls import path
from . import views

urlpatterns = [
    path("teacher/signup/", views.teacher_signup, name="teacher_signup"),
    path("student/signup/", views.student_signup, name="student_signup"),
    path( "login/", views.login_view, name="login"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path( "teacher/publish-note/", views.publish_note, name="publish_note"),
    path("student/notes/",views.student_notes, name="student_notes"),
    path("teacher/note/<int:note_id>/edit/",views.edit_note,name="edit_note"),
    path("teacher/note/<int:note_id>/delete/", views.delete_note, name="delete_note"),
    path("teacher/create-announcement/",views.create_announcement, name="create_announcement"),
    path( "student/announcements/",  views.student_announcements, name="student_announcements"),
    path( "teacher/create-assignment/",views.create_assignment, name="create_assignment"),
    path( "student/assignments/", views.student_assignments, name="student_assignments"),
    path( "student/assignments/<int:assignment_id>/submit/", views.submit_assignment,name="submit_assignment"),

]



    