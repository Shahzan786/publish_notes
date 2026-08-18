from django import forms
from school.models import Teacher,Student , Note , Announcement


class TeacherSignupForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    school_name = forms.CharField(max_length=200)
    school_address = forms.CharField(
        widget=forms.Textarea
    )

    class_name = forms.CharField(max_length=50)

    class Meta:
        model = Teacher
        fields = [
            "name",
            "employee_id",
        ]


class StudentSignupForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = Student
        fields = ["name", "roll_number", "student_class"]        


class LoginForm(forms.Form):

    username = forms.CharField(max_length=150)
    password = forms.CharField(
        widget=forms.PasswordInput
    )        

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ["title", "content", "file"]


class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ["title", "message"]
