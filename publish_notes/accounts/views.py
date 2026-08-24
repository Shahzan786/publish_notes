from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db import transaction
from functools import wraps

from .forms import (
    TeacherSignupForm,
    LoginForm,
    StudentSignupForm,
    NoteForm,
    AnnouncementForm,
    AssignmentForm,
    SubmissionForm,
    Submission,
)

from school.models import School, Class, Note, Assignment


# ============================================================
# ROLE DECORATORS
# ============================================================

def teacher_required(view_func):

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if not hasattr(request.user, "teacher_profile"):
            return HttpResponseForbidden(
                "You are not authorized to access this teacher page."
            )

        return view_func(request, *args, **kwargs)

    return wrapper


def student_required(view_func):

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if not hasattr(request.user, "student_profile"):
            return HttpResponseForbidden(
                "You are not authorized to access this student page."
            )

        return view_func(request, *args, **kwargs)

    return wrapper


# ============================================================
# TEACHER SIGNUP
# ============================================================

@transaction.atomic
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

            # Create Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create Teacher profile
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
        {
            "form": form
        }
    )


# ============================================================
# STUDENT SIGNUP
# ============================================================

@transaction.atomic
def student_signup(request):

    if request.method == "POST":

        form = StudentSignupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Create Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create Student profile
            student = form.save(commit=False)

            student.user = user

            student.save()

            return redirect("login")

    else:

        form = StudentSignupForm()

    return render(
        request,
        "accounts/student_signup.html",
        {
            "form": form
        }
    )


# ============================================================
# LOGIN
# ============================================================

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

                # Teacher
                if hasattr(user, "teacher_profile"):
                    return redirect("teacher_dashboard")

                # Student
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
        {
            "form": form
        }
    )


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@student_required
def student_dashboard(request):

    student = request.user.student_profile

    return render(
        request,
        "accounts/student_dashboard.html",
        {
            "student": student
        }
    )


# ============================================================
# TEACHER DASHBOARD
# ============================================================

@teacher_required
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


# ============================================================
# TEACHER - PUBLISH NOTE
# ============================================================

@teacher_required
def publish_note(request):

    teacher = request.user.teacher_profile

    class_obj = teacher.assigned_class

    if request.method == "POST":

        form = NoteForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            note = form.save(commit=False)

            # Automatically attach teacher's class
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


# ============================================================
# STUDENT - NOTES
# ============================================================

@student_required
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


# ============================================================
# TEACHER - EDIT NOTE
# ============================================================

@teacher_required
def edit_note(request, note_id):

    teacher = request.user.teacher_profile

    class_obj = teacher.assigned_class

    # Security:
    # Note must belong to teacher's class
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

        form = NoteForm(
            instance=note
        )

    return render(
        request,
        "accounts/edit_note.html",
        {
            "form": form,
            "note": note
        }
    )


# ============================================================
# TEACHER - DELETE NOTE
# ============================================================

@teacher_required
def delete_note(request, note_id):

    teacher = request.user.teacher_profile

    class_obj = teacher.assigned_class

    # Security:
    # Note must belong to teacher's class
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


# ============================================================
# TEACHER - CREATE ANNOUNCEMENT
# ============================================================

@teacher_required
def create_announcement(request):

    teacher = request.user.teacher_profile

    class_obj = teacher.assigned_class

    if request.method == "POST":

        form = AnnouncementForm(
            request.POST
        )

        if form.is_valid():

            announcement = form.save(
                commit=False
            )

            # Automatically attach class
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


# ============================================================
# STUDENT - ANNOUNCEMENTS
# ============================================================

@student_required
def student_announcements(request):

    student = request.user.student_profile

    announcements = (
        student.student_class.announcements.all()
    )

    return render(
        request,
        "accounts/student_announcements.html",
        {
            "student": student,
            "announcements": announcements,
        }
    )


# ============================================================
# TEACHER - CREATE ASSIGNMENT
# ============================================================

@teacher_required
def create_assignment(request):

    teacher = request.user.teacher_profile

    class_obj = teacher.assigned_class

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            assignment = form.save(
                commit=False
            )

            # Automatically attach teacher's class
            assignment.class_obj = class_obj

            assignment.save()

            return redirect("teacher_dashboard")

    else:

        form = AssignmentForm()

    return render(
        request,
        "accounts/create_assignment.html",
        {
            "form": form,
            "class_obj": class_obj,
        }
    )


# ============================================================
# STUDENT - ASSIGNMENTS
# ============================================================

@student_required
def student_assignments(request):

    student = request.user.student_profile

    assignments = (
        student.student_class.assignments.all()
    )

    for assignment in assignments:

        assignment.my_submission = (
            Submission.objects.filter(
                assignment=assignment,
                student=student
            ).first()
        )

    return render(
        request,
        "accounts/student_assignments.html",
        {
            "student": student,
            "assignments": assignments,
        }
    )


# ============================================================
# STUDENT - SUBMIT ASSIGNMENT
# ============================================================

@student_required
def submit_assignment(request, assignment_id):

    student = request.user.student_profile

    # Security:
    # Assignment must belong to student's class
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        class_obj=student.student_class
    )

    # If already submitted, don't create duplicate
    existing_submission = Submission.objects.filter(
        assignment=assignment,
        student=student
    ).first()

    if existing_submission:

        return redirect(
            "view_submission",
            assignment_id=assignment.id
        )

    if request.method == "POST":

        form = SubmissionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            submission = form.save(
                commit=False
            )

            # Automatically attach assignment
            submission.assignment = assignment

            # Automatically attach logged-in student
            submission.student = student

            submission.save()

            return redirect(
                "student_assignments"
            )

    else:

        form = SubmissionForm()

    return render(
        request,
        "accounts/submit_assignment.html",
        {
            "form": form,
            "assignment": assignment,
        }
    )


# ============================================================
# STUDENT - VIEW SUBMISSION
# ============================================================

@student_required
def view_submission(request, assignment_id):

    student = request.user.student_profile

    # Assignment must belong to student's class
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        class_obj=student.student_class
    )

    # Submission must belong to logged-in student
    submission = get_object_or_404(
        Submission,
        assignment=assignment,
        student=student
    )

    return render(
        request,
        "accounts/view_submission.html",
        {
            "assignment": assignment,
            "submission": submission,
        }
    )


# ============================================================
# STUDENT - UPDATE SUBMISSION
# ============================================================

@student_required
def update_submission(request, submission_id):

    student = request.user.student_profile

    # Security:
    # Submission must belong to logged-in student
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        student=student
    )

    if request.method == "POST":

        form = SubmissionForm(
            request.POST,
            request.FILES,
            instance=submission
        )

        if form.is_valid():

            form.save()

            return redirect(
                "view_submission",
                assignment_id=submission.assignment.id
            )

    else:

        form = SubmissionForm(
            instance=submission
        )

    return render(
        request,
        "accounts/update_submission.html",
        {
            "form": form,
            "submission": submission,
        }
    )


# ============================================================
# STUDENT - DELETE SUBMISSION
# ============================================================

@student_required
def delete_submission(request, submission_id):

    student = request.user.student_profile

    # Security:
    # Submission must belong to logged-in student
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        student=student
    )

    if request.method == "POST":

        submission.delete()

        return redirect(
            "student_assignments"
        )

    return render(
        request,
        "accounts/delete_submission.html",
        {
            "submission": submission,
        }
    )


# ============================================================
# TEACHER - VIEW SUBMISSIONS
# ============================================================

@teacher_required
def teacher_submissions(request, assignment_id):

    teacher = request.user.teacher_profile

    class_obj = teacher.assigned_class

    # Security:
    # Assignment must belong to teacher's class
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        class_obj=class_obj
    )

    students = class_obj.students.all()

    submissions = Submission.objects.filter(
        assignment=assignment
    )

    submission_map = {
        submission.student_id: submission
        for submission in submissions
    }

    student_data = []

    for student in students:

        submission = submission_map.get(
            student.id
        )

        student_data.append(
            {
                "student": student,
                "submission": submission,
            }
        )

    return render(
        request,
        "accounts/teacher_submissions.html",
        {
            "assignment": assignment,
            "student_data": student_data,
        }
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def user_logout(request):

    logout(request)

    return redirect("login")


# ============================================================
# HOMEPAGE
# ============================================================

def home(request):

    return render(
        request,
        "accounts/home.html"
    )