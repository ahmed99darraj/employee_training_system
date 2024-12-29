from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime, date
import os
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import CourseForm, InstructorForm, RoomForm, UserForm, OfficeForm, UserRegistrationForm
from .models import Course, Enrollment, Office, Instructor, Room, User, Attendance, Certificate

def is_admin(user):
    return user.is_staff or user.is_superuser

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إنشاء حسابك بنجاح! يمكنك الآن تسجيل الدخول.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'training/register.html', {'form': form})

@login_required
def dashboard(request):
    user_enrollments = Enrollment.objects.filter(user=request.user)
    available_courses = Course.objects.all().exclude(
        enrollment__user=request.user
    )
    return render(request, 'training/dashboard.html', {
        'enrollments': user_enrollments,
        'available_courses': available_courses
    })

def office_courses(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    courses = Course.objects.filter(office=office)
    return render(request, 'training/office_courses.html', {
        'office': office,
        'courses': courses
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        if Enrollment.objects.filter(course=course).count() >= course.capacity:
            messages.error(request, 'This course is already full.')
            return redirect('dashboard')
        
        if course.gender_specific != request.user.gender:
            messages.error(request, 'This course is not available for your gender.')
            return redirect('dashboard')
        
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f'Successfully enrolled in {course.title}')
        return redirect('dashboard')
    
    return render(request, 'training/enroll_course.html', {'course': course})

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'training/my_courses.html', {'enrollments': enrollments})

def office_list(request):
    offices = Office.objects.all()
    return render(request, 'training/office_list.html', {'offices': offices})

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    context = {
        'instructors_count': Instructor.objects.count(),
        'users_count': User.objects.count(),
        'courses_count': Course.objects.count(),
        'offices_count': Office.objects.count(),
        'rooms_count': Room.objects.count(),
    }
    return render(request, 'training/admin/panel.html', context)

@login_required
@user_passes_test(is_admin)
def manage_instructors(request):
    instructors = Instructor.objects.all()
    return render(request, 'training/admin/instructors.html', {'instructors': instructors})

@login_required
@user_passes_test(is_admin)
def add_instructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة المدرب بنجاح')
            return redirect('manage_instructors')
    else:
        form = InstructorForm()
    
    return render(request, 'training/admin/instructor_form.html', {'form': form, 'title': 'إضافة مدرب'})

@login_required
@user_passes_test(is_admin)
def edit_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المدرب بنجاح')
            return redirect('manage_instructors')
    else:
        form = InstructorForm(instance=instructor)
    
    return render(request, 'training/admin/instructor_form.html', {'form': form, 'title': 'تعديل المدرب'})

@login_required
@user_passes_test(is_admin)
def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == 'POST':
        instructor.delete()
        messages.success(request, 'تم حذف المدرب بنجاح')
        return redirect('manage_instructors')
    
    return render(request, 'training/admin/confirm_delete.html', {
        'title': 'حذف المدرب',
        'message': f'هل أنت متأكد من حذف المدرب {instructor.name}؟'
    })

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'training/admin/users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المستخدم بنجاح')
            return redirect('manage_users')
    else:
        form = UserForm(instance=user)
    
    return render(request, 'training/admin/user_form.html', {'form': form, 'title': 'تعديل المستخدم'})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'تم حذف المستخدم بنجاح')
        return redirect('manage_users')
    
    return render(request, 'training/admin/confirm_delete.html', {
        'title': 'حذف المستخدم',
        'message': f'هل أنت متأكد من حذف المستخدم {user.username}؟'
    })

@login_required
@user_passes_test(is_admin)
def manage_offices(request):
    offices = Office.objects.all()
    return render(request, 'training/admin/offices.html', {'offices': offices})

@login_required
@user_passes_test(is_admin)
def add_office(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة المكتب بنجاح')
            return redirect('manage_offices')
    else:
        form = OfficeForm()
    
    return render(request, 'training/admin/office_form.html', {'form': form, 'title': 'إضافة مكتب'})

@login_required
@user_passes_test(is_admin)
def edit_office(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل المكتب بنجاح')
            return redirect('manage_offices')
    else:
        form = OfficeForm(instance=office)
    
    return render(request, 'training/admin/office_form.html', {'form': form, 'title': 'تعديل المكتب'})

@login_required
@user_passes_test(is_admin)
def delete_office(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    if request.method == 'POST':
        office.delete()
        messages.success(request, 'تم حذف المكتب بنجاح')
        return redirect('manage_offices')
    
    return render(request, 'training/admin/confirm_delete.html', {
        'title': 'حذف المكتب',
        'message': f'هل أنت متأكد من حذف المكتب {office.name}؟'
    })

@login_required
@user_passes_test(is_admin)
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'training/admin/courses.html', {'courses': courses})

@login_required
@user_passes_test(is_admin)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة الدورة بنجاح')
            return redirect('manage_courses')
    else:
        form = CourseForm()
    
    return render(request, 'training/admin/course_form.html', {'form': form, 'title': 'إضافة دورة'})

@login_required
@user_passes_test(is_admin)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل الدورة بنجاح')
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'training/admin/course_form.html', {'form': form, 'title': 'تعديل الدورة'})

@login_required
@user_passes_test(is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'تم حذف الدورة بنجاح')
        return redirect('manage_courses')
    
    return render(request, 'training/admin/confirm_delete.html', {
        'title': 'حذف الدورة',
        'message': f'هل أنت متأكد من حذف الدورة {course.name}؟'
    })

@login_required
@user_passes_test(is_admin)
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # حساب نسبة التقدم في الدورة
    total_hours = Attendance.objects.filter(
        user=request.user,
        course=course,
        is_present=True
    ).aggregate(total=Sum('hours_attended'))['total'] or 0
    
    progress = (total_hours / course.total_hours * 100) if course.total_hours else 0
    progress = min(progress, 100)  # لا تتجاوز 100%
    
    context = {
        'course': course,
        'progress': progress,
    }
    
    return render(request, 'training/course_detail.html', context)

@login_required
@user_passes_test(is_admin)
def manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'training/admin/rooms.html', {'rooms': rooms})

@login_required
@user_passes_test(is_admin)
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة القاعة بنجاح')
            return redirect('manage_rooms')
    else:
        form = RoomForm()
    
    return render(request, 'training/admin/room_form.html', {'form': form, 'title': 'إضافة قاعة'})

@login_required
@user_passes_test(is_admin)
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل القاعة بنجاح')
            return redirect('manage_rooms')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'training/admin/room_form.html', {'form': form, 'title': 'تعديل القاعة'})

@login_required
@user_passes_test(is_admin)
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'تم حذف القاعة بنجاح')
        return redirect('manage_rooms')
    
    return render(request, 'training/admin/confirm_delete.html', {
        'title': 'حذف القاعة',
        'message': f'هل أنت متأكد من حذف القاعة {room.name}؟'
    })

@login_required
def office_list(request):
    offices = Office.objects.all()
    return render(request, 'training/office_list.html', {'offices': offices})

@login_required
def office_courses(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    courses = Course.objects.filter(office=office)
    return render(request, 'training/office_courses.html', {'office': office, 'courses': courses})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'أنت مسجل بالفعل في هذه الدورة')
    else:
        if course.enrollment_set.count() >= course.max_participants:
            messages.error(request, 'عذراً، الدورة مكتملة')
        else:
            Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, 'تم التسجيل في الدورة بنجاح')
    return redirect('office_courses', office_id=course.office.id)

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'training/my_courses.html', {'enrollments': enrollments})

@login_required
def course_list(request):
    # للمشرفين: عرض جميع الدورات
    if request.user.is_staff:
        courses = Course.objects.all()
    # للمتدربين: عرض الدورات المسجلين فيها فقط
    else:
        enrollments = Enrollment.objects.filter(user=request.user)
        courses = [enrollment.course for enrollment in enrollments]
    
    context = {
        'courses': courses,
        'title': 'قائمة الدورات'
    }
    return render(request, 'training/course_list.html', context)

@login_required
def mark_attendance(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        date_str = request.POST.get('date')
        hours = request.POST.get('hours')
        is_present = request.POST.get('is_present') == 'true'
        
        attendance = Attendance.objects.create(
            user=request.user,
            course=course,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            is_present=is_present,
            hours_attended=hours if is_present else 0
        )
        
        # التحقق من إمكانية إصدار الشهادة
        check_and_issue_certificate(request.user, course)
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def check_and_issue_certificate(user, course):
    # حساب إجمالي ساعات الحضور
    total_hours = Attendance.objects.filter(
        user=user,
        course=course,
        is_present=True
    ).aggregate(total=Sum('hours_attended'))['total'] or 0
    
    # التحقق من تجاوز الحد الأدنى المطلوب (مثلاً 80% من ساعات الدورة)
    required_hours = course.total_hours * 0.8
    
    if total_hours >= required_hours and not Certificate.objects.filter(user=user, course=course).exists():
        # إنشاء الشهادة
        certificate = generate_certificate(user, course, total_hours)
        
        # إرسال بريد إلكتروني للمتدرب
        send_certificate_email(user, certificate)

def generate_certificate(user, course, total_hours):
    # إنشاء ملف PDF للشهادة
    filename = f'certificate_{user.username}_{course.id}.pdf'
    filepath = os.path.join('media/certificates', filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # إضافة محتوى الشهادة
    c.setFont('Helvetica-Bold', 24)
    c.drawCentredString(width/2, height-100, "شهادة إتمام دورة تدريبية")
    
    c.setFont('Helvetica', 16)
    c.drawCentredString(width/2, height-150, f"نشهد أن المتدرب/ة: {user.get_full_name()}")
    c.drawCentredString(width/2, height-200, f"قد أتم/ت دورة: {course.name}")
    c.drawCentredString(width/2, height-250, f"بإجمالي ساعات: {total_hours}")
    c.drawCentredString(width/2, height-300, f"التاريخ: {date.today().strftime('%Y-%m-%d')}")
    
    c.save()
    
    # إنشاء سجل الشهادة
    certificate = Certificate.objects.create(
        user=user,
        course=course,
        total_hours=total_hours,
        certificate_file=f'certificates/{filename}'
    )
    
    return certificate

def send_certificate_email(user, certificate):
    subject = f'تهانينا! لقد أتممت دورة {certificate.course.name}'
    message = f'''تهانينا {user.get_full_name()}!
    
    لقد أتممت بنجاح دورة {certificate.course.name} بإجمالي ساعات {certificate.total_hours}.
    تجد مرفقاً شهادة إتمام الدورة.
    
    مع تحياتنا،
    فريق التدريب'''
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )
    
    # إرفاق الشهادة
    email.attach_file(certificate.certificate_file.path)
    email.send()

@login_required
def attendance_summary(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    attendance_records = Attendance.objects.filter(user=request.user, course=course)
    
    total_days = attendance_records.count()
    present_days = attendance_records.filter(is_present=True).count()
    absent_days = total_days - present_days
    total_hours = attendance_records.filter(is_present=True).aggregate(
        total=Sum('hours_attended'))['total'] or 0
    required_hours = course.total_hours
    
    context = {
        'course': course,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'total_hours': total_hours,
        'required_hours': required_hours,
        'progress_percentage': (total_hours / required_hours * 100) if required_hours else 0
    }
    
    return render(request, 'training/attendance_summary.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
