from django import forms
from .models import Notice
from django import forms
from .models import CustomUser

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['notice_subject', 'display_category', 'message', 'file_upload', 'thumbnail']
        labels = {
            'notice_subject': 'Notice Title',
            'display_category': 'Notice Type',
            'message': 'Description',
            'file_upload': 'Attachment (Optional)',
            'thumbnail': 'Thumbnail Image (Optional)'
        }



# STUDENT
class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'admission_no', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # 🔥 WAIT FOR ADMIN APPROVAL
        if commit:
            user.save()
        return user


# HOD
class HodRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('admission_no', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'hod'
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        return user


# OFFICE STAFF
class StaffRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('department', None)
        self.fields.pop('admission_no', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'staff'
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['photo', 'address', 'phone', 'university_reg_no']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # 🔥 Remove university_reg_no for HOD & Staff
        if user and user.user_type != 'student':
            self.fields.pop('university_reg_no')