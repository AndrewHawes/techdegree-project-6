# Generated by Django 2.2.3 on 2019-07-15 21:46
import sys

from django.db import migrations


def load_data(apps, schema_editor):
    import json
    with open('minerals/data/minerals.json') as file:
        data = json.load(file)

    Mineral = apps.get_model('minerals', 'Mineral')

    minerals = []
    names = []

    for entry in data:
        if entry['name'] in names:
            continue
        else:
            mineral = Mineral(**entry)
            names.append(mineral.name)
            minerals.append(mineral)

    try:
        Mineral.objects.bulk_create(minerals)
    except Exception as e:
        print("ERROR LOADING DATA:\n", e)


class Migration(migrations.Migration):

    dependencies = [
        ('minerals', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ] if 'test' not in sys.argv[1:] else []