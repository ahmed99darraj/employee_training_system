from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    )
    
    national_id = models.CharField(max_length=10, unique=True, validators=[
        RegexValidator(regex='^[0-9]{10}$', message='National ID must be 10 digits')
    ], verbose_name="رقم الهوية")
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="الجنس")
    
    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['email', 'phone_number', 'gender', 'username']

    def __str__(self):
        return self.username

class Office(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المكتب")
    location = models.CharField(max_length=200, verbose_name="الموقع")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مكتب"
        verbose_name_plural = "المكاتب"

class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم القاعة")
    capacity = models.IntegerField(verbose_name="السعة")
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name="المكتب")

    def __str__(self):
        return f"{self.name} - {self.office.name}"

    class Meta:
        verbose_name = "قاعة"
        verbose_name_plural = "القاعات"

class Instructor(models.Model):
    name = models.CharField(max_length=100, verbose_name="الاسم")
    specialization = models.CharField(max_length=100, verbose_name="التخصص")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, verbose_name="المكتب")
    bio = models.TextField(verbose_name="نبذة تعريفية")
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مدرب"
        verbose_name_plural = "المدربون"

class Course(models.Model):
    TYPE_CHOICES = (
        ('workshop', 'ورشة عمل'),
        ('course', 'دورة تدريبية'),
        ('program', 'برنامج تدريبي'),
    )
    
    PERIOD_CHOICES = (
        ('morning', 'صباحي'),
        ('evening', 'مسائي'),
    )
    
    TARGET_CHOICES = (
        ('principals', 'مديرو المدارس'),
        ('supervisors', 'المشرفون'),
        ('teachers', 'المعلمون'),
    )
    
    STATUS_CHOICES = (
        ('completed', 'منفذ'),
        ('confirmed', 'مثبت'),
        ('in_progress', 'جاري'),
        ('postponed', 'مؤجل'),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='course', verbose_name="النوع")
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='morning', verbose_name="الفترة")
    name = models.CharField(max_length=100, verbose_name="اسم البرنامج", default="دورة جديدة")
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المدرب")
    target_audience = models.CharField(max_length=20, choices=TARGET_CHOICES, default='teachers', verbose_name="المستهدفون")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="القاعة")
    supervising_office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='supervised_courses', verbose_name="الجهة المشرفة")
    days = models.CharField(max_length=100, default="الأحد - الخميس", verbose_name="الأيام")
    start_date = models.DateField(default=timezone.now, verbose_name="تاريخ البداية")
    end_date = models.DateField(default=timezone.now, verbose_name="تاريخ النهاية")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed', verbose_name="الحالة")
    description = models.TextField(blank=True, verbose_name="وصف الدورة")
    max_participants = models.IntegerField(default=20, verbose_name="العدد الأقصى للمشاركين")
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="إجمالي ساعات الدورة")
    syllabus = models.FileField(upload_to='courses/syllabi/', null=True, blank=True, verbose_name="المنهج الدراسي")
    course_material = models.FileField(upload_to='courses/materials/', null=True, blank=True, verbose_name="المواد التدريبية")
    presentation = models.FileField(upload_to='courses/presentations/', null=True, blank=True, verbose_name="العرض التقديمي")
    video = models.FileField(upload_to='courses/videos/', null=True, blank=True, verbose_name="فيديو تعريفي")
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"

    class Meta:
        verbose_name = "دورة تدريبية"
        verbose_name_plural = "الدورات التدريبية"

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('P', 'معلق'),
        ('A', 'مقبول'),
        ('R', 'مرفوض'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="الدورة")
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', verbose_name="الحالة")
    certificate_issued = models.BooleanField(default=False, verbose_name="تم إصدار الشهادة")
    certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "تسجيل"
        verbose_name_plural = "التسجيلات"

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المتدرب")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="الدورة")
    date = models.DateField(verbose_name="تاريخ الحضور")
    is_present = models.BooleanField(default=True, verbose_name="حاضر")
    hours_attended = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name="عدد ساعات الحضور")
    
    class Meta:
        verbose_name = "سجل الحضور"
        verbose_name_plural = "سجلات الحضور"
        unique_together = ['user', 'course', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.course.name} - {self.date}"

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المتدرب")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="الدورة")
    issue_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الإصدار")
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="إجمالي الساعات")
    certificate_file = models.FileField(upload_to='certificates/', verbose_name="ملف الشهادة")
    
    class Meta:
        verbose_name = "شهادة"
        verbose_name_plural = "الشهادات"
        unique_together = ['user', 'course']

    def __str__(self):
        return f"شهادة {self.user.username} - {self.course.name}"
