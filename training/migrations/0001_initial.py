# Generated by Django 5.0 on 2024-12-28 20:08

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='اسم المكتب')),
                ('location', models.CharField(max_length=200, verbose_name='الموقع')),
            ],
            options={
                'verbose_name': 'مكتب',
                'verbose_name_plural': 'المكاتب',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('national_id', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='National ID must be 10 digits', regex='^[0-9]{10}$')], verbose_name='رقم الهوية')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, verbose_name='رقم الهاتف')),
                ('gender', models.CharField(choices=[('M', 'ذكر'), ('F', 'أنثى')], max_length=1, verbose_name='الجنس')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='الاسم')),
                ('specialization', models.CharField(max_length=100, verbose_name='التخصص')),
                ('phone_number', models.CharField(max_length=20, verbose_name='رقم الهاتف')),
                ('email', models.EmailField(max_length=254, verbose_name='البريد الإلكتروني')),
                ('bio', models.TextField(verbose_name='نبذة تعريفية')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='training.office', verbose_name='المكتب')),
            ],
            options={
                'verbose_name': 'مدرب',
                'verbose_name_plural': 'المدربون',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='اسم القاعة')),
                ('capacity', models.IntegerField(verbose_name='السعة')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.office', verbose_name='المكتب')),
            ],
            options={
                'verbose_name': 'قاعة',
                'verbose_name_plural': 'القاعات',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('workshop', 'ورشة عمل'), ('course', 'دورة تدريبية'), ('program', 'برنامج تدريبي')], default='course', max_length=20, verbose_name='النوع')),
                ('period', models.CharField(choices=[('morning', 'صباحي'), ('evening', 'مسائي')], default='morning', max_length=20, verbose_name='الفترة')),
                ('name', models.CharField(default='دورة جديدة', max_length=100, verbose_name='اسم البرنامج')),
                ('target_audience', models.CharField(choices=[('principals', 'مديرو المدارس'), ('supervisors', 'المشرفون'), ('teachers', 'المعلمون')], default='teachers', max_length=20, verbose_name='المستهدفون')),
                ('days', models.CharField(default='الأحد - الخميس', max_length=100, verbose_name='الأيام')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ البداية')),
                ('end_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ النهاية')),
                ('status', models.CharField(choices=[('completed', 'منفذ'), ('confirmed', 'مثبت'), ('in_progress', 'جاري'), ('postponed', 'مؤجل')], default='confirmed', max_length=20, verbose_name='الحالة')),
                ('description', models.TextField(blank=True, verbose_name='وصف الدورة')),
                ('max_participants', models.IntegerField(default=20, verbose_name='العدد الأقصى للمشاركين')),
                ('syllabus', models.FileField(blank=True, null=True, upload_to='courses/syllabi/', verbose_name='المنهج الدراسي')),
                ('course_material', models.FileField(blank=True, null=True, upload_to='courses/materials/', verbose_name='المواد التدريبية')),
                ('presentation', models.FileField(blank=True, null=True, upload_to='courses/presentations/', verbose_name='العرض التقديمي')),
                ('video', models.FileField(blank=True, null=True, upload_to='courses/videos/', verbose_name='فيديو تعريفي')),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='training.instructor', verbose_name='المدرب')),
                ('supervising_office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervised_courses', to='training.office', verbose_name='الجهة المشرفة')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='training.room', verbose_name='القاعة')),
            ],
            options={
                'verbose_name': 'دورة تدريبية',
                'verbose_name_plural': 'الدورات التدريبية',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التسجيل')),
                ('status', models.CharField(choices=[('P', 'معلق'), ('A', 'مقبول'), ('R', 'مرفوض')], default='P', max_length=1, verbose_name='الحالة')),
                ('certificate_issued', models.BooleanField(default=False, verbose_name='تم إصدار الشهادة')),
                ('certificate_file', models.FileField(blank=True, null=True, upload_to='certificates/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.course', verbose_name='الدورة')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المستخدم')),
            ],
            options={
                'verbose_name': 'تسجيل',
                'verbose_name_plural': 'التسجيلات',
                'unique_together': {('user', 'course')},
            },
        ),
    ]