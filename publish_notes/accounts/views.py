from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from .forms import (
    TeacherSignupForm,
    LoginForm,
    StudentSignupForm,
    NoteForm,
    AnnouncementForm,
)

from school.models import School, Class , Note


def teacher_signup(request):

    if request.method == "POST":

        form = TeacherSignupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            school_name = form.cleaned_data["school_name"]
            school_address = form.cleaned_data["school_address"]

            class_name = form.cleaned_data["class_name"]

            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create Teacher
            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()

            # Create or get School
            school, created = School.objects.get_or_create(
                name=school_name,
                defaults={
                    "address": school_address
                }
            )

            # Create Class
            Class.objects.create(
                name=class_name,
                school=school,
                teacher=teacher
            )

            return redirect("login")

    else:
        form = TeacherSignupForm()

    return render(
        request,
        "accounts/teacher_signup.html",
        {"form": form}
    )


def student_signup(request):

    if request.method == "POST":
        form = StudentSignupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            student = form.save(commit=False)
            student.user = user
            student.save()

            return redirect("login")

    else:
        form = StudentSignupForm()

    return render(
        request,
        "accounts/student_signup.html",
        {"form": form}
    )

def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                if hasattr(user, "teacher_profile"):
                    return redirect("teacher_dashboard")

                if hasattr(user, "student_profile"):
                    return redirect("student_dashboard")

                form.add_error(
                    None,
                    "Your account is not linked to a teacher or student profile."
                )

            else:
                form.add_error(
                    None,
                    "Invalid username or password."
                )

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )

def student_dashboard(request):

    student = request.user.student_profile

    return render(
        request,
        "accounts/student_dashboard.html",
        {"student": student}
    )

def teacher_dashboard(request):

    teacher = request.user.teacher_profile
    class_obj = teacher.assigned_class
    students = class_obj.students.all()

    return render(
        request,
        "accounts/teacher_dashboard.html",
        {
            "teacher": teacher,
            "class_obj": class_obj,
            "students": students,
        }
    )

def publish_note(request):

    teacher = request.user.teacher_profile
    class_obj = teacher.assigned_class

    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)

        if form.is_valid():
            note = form.save(commit=False)

            note.class_obj = class_obj

            note.save()

            return redirect("teacher_dashboard")

    else:
        form = NoteForm()

    return render(
        request,
        "accounts/publish_note.html",
        {
            "form": form,
            "class_obj": class_obj,
        }
    )

def student_notes(request):

    student = request.user.student_profile

    notes = student.student_class.notes.all()

    return render(
        request,
        "accounts/student_notes.html",
        {
            "student": student,
            "notes": notes,
        }
    )

def edit_note(request, note_id):

    teacher = request.user.teacher_profile
    class_obj = teacher.assigned_class

    note = get_object_or_404(
        Note,
        id=note_id,
        class_obj=class_obj
    )

    if request.method == "POST":
        form = NoteForm(
            request.POST,
            request.FILES,
            instance=note
        )

        if form.is_valid():
            form.save()

            return redirect("teacher_dashboard")

    else:
        form = NoteForm(instance=note)

    return render(
        request,
        "accounts/edit_note.html",
        {
            "form": form,
            "note": note
        }
    )

def delete_note(request, note_id):

    teacher = request.user.teacher_profile
    class_obj = teacher.assigned_class

    note = get_object_or_404(
        Note,
        id=note_id,
        class_obj=class_obj
    )

    if request.method == "POST":
        note.delete()
        return redirect("teacher_dashboard")

    return render(
        request,
        "accounts/delete_note.html",
        {
            "note": note
        }
    )

def create_announcement(request):

    teacher = request.user.teacher_profile
    class_obj = teacher.assigned_class

    if request.method == "POST":

        form = AnnouncementForm(request.POST)

        if form.is_valid():

            announcement = form.save(commit=False)

            announcement.class_obj = class_obj

            announcement.save()

            return redirect("teacher_dashboard")

    else:
        form = AnnouncementForm()

    return render(
        request,
        "accounts/create_announcement.html",
        {
            "form": form,
            "class_obj": class_obj,
        }
    )

def student_announcements(request):

    student = request.user.student_profile

    announcements = student.student_class.announcements.all()

    return render(
        request,
        "accounts/student_announcements.html",
        {
            "student": student,
            "announcements": announcements,
        }
    )