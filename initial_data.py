from training.models import Office

offices = [
    {'name': 'صبيا', 'location': 'صبيا'},
    {'name': 'الدائر', 'location': 'الدائر'},
    {'name': 'بيش', 'location': 'بيش'},
    {'name': 'الدرب', 'location': 'الدرب'},
    {'name': 'العيدابي', 'location': 'العيدابي'},
    {'name': 'المقر المركزي', 'location': 'صبيا'},
    {'name': 'مدارس التعليم الأهلية', 'location': 'صبيا'},
]

for office_data in offices:
    Office.objects.get_or_create(
        name=office_data['name'],
        defaults={'location': office_data['location']}
    )
