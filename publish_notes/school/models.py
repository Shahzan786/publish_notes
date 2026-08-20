from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=50)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="classes"
    )
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name="assigned_class"
    )

    def __str__(self):
        return f"{self.name} - {self.school.name}"


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50)

    student_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="students"
    )

    def __str__(self):
        return f"{self.name} - {self.roll_number}"


class Note(models.Model):

    title = models.CharField(max_length=200)

    content = models.TextField()

    file = models.FileField(
        upload_to="notes/",
        blank=True,
        null=True
    )

    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title    

class Announcement(models.Model):

    title = models.CharField(max_length=200)

    message = models.TextField()

    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="announcements"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title    


class Assignment(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    due_date = models.DateTimeField()

    file = models.FileField(
        upload_to="assignments/",
        blank=True,
        null=True
    )

    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title    

class Submission(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    file = models.FileField(
        upload_to="submissions/"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    grade = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    feedback = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"    