from django.db import migrations

def create_initial_spaces(apps, schema_editor):
    Space = apps.get_model('app1', 'Space')
    spaces = [
        {'name': f'Single Office {i}', 'office_type': 'single', 'capacity': 1, 'amenities': 'WiFi, Desk, Chair', 'location': 'Floor 1, Room 101', 'price_per_hour': 10.00} for i in range(1, 6)
    ] + [
        {'name': f'Multiple Office {i}', 'office_type': 'multiple', 'capacity': 5, 'amenities': 'WiFi, Desks, Chairs', 'location': 'Floor 2, Room 201', 'price_per_hour': 25.00} for i in range(1, 6)
    ] + [
        {'name': f'Meeting Room {i}', 'office_type': 'meeting', 'capacity': 10, 'amenities': 'WiFi, Projector, Chairs, Table', 'location': 'Floor 3, Room 301', 'price_per_hour': 50.00} for i in range(1, 6)
    ] + [
        {'name': f'Lab with PCs {i}', 'office_type': 'lab', 'capacity': 8, 'amenities': 'WiFi, PCs, Desks, Chairs', 'location': 'Floor 4, Room 401', 'price_per_hour': 40.00} for i in range(1, 6)
    ] + [
        {'name': f'Private Office Suite {i}', 'office_type': 'suite', 'capacity': 3, 'amenities': 'WiFi, Desk, Chair, Private Bathroom', 'location': 'Floor 5, Room 501', 'price_per_hour': 60.00} for i in range(1, 6)
    ]
    for space in spaces:
        Space.objects.create(**space)

class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_spaces),
    ]
