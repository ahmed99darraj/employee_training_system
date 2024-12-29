from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course, Enrollment, Instructor, Room, Office

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'national_id', 'phone_number', 'gender', 'is_staff']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'national_id': 'رقم الهوية',
            'phone_number': 'رقم الهاتف',
            'gender': 'الجنس',
            'is_staff': 'مشرف نظام',
        }

class UserRegistrationForm(UserCreationForm):
    national_id = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'national_id', 'phone_number', 'password1', 'password2')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'type', 'period', 'name', 'instructor', 'target_audience', 'room',
            'supervising_office', 'days', 'start_date', 'end_date', 'status',
            'description', 'max_participants', 'syllabus', 'course_material',
            'presentation', 'video'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'type': 'النوع',
            'period': 'الفترة',
            'name': 'اسم البرنامج',
            'instructor': 'المدرب',
            'target_audience': 'المستهدفون',
            'room': 'القاعة',
            'supervising_office': 'الجهة المشرفة',
            'days': 'الأيام',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'status': 'الحالة',
            'description': 'وصف الدورة',
            'max_participants': 'العدد الأقصى للمشاركين',
            'syllabus': 'المنهج الدراسي',
            'course_material': 'المواد التدريبية',
            'presentation': 'العرض التقديمي',
            'video': 'فيديو تعريفي'
        }

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['name', 'specialization', 'email', 'phone_number', 'office', 'bio', 'is_active']
        labels = {
            'name': 'الاسم',
            'specialization': 'التخصص',
            'email': 'البريد الإلكتروني',
            'phone_number': 'رقم الهاتف',
            'office': 'المكتب',
            'bio': 'نبذة تعريفية',
            'is_active': 'نشط'
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'office']
        labels = {
            'name': 'اسم القاعة',
            'capacity': 'السعة',
            'office': 'المكتب',
        }

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['name', 'location']
        labels = {
            'name': 'اسم المكتب',
            'location': 'الموقع',
        }
