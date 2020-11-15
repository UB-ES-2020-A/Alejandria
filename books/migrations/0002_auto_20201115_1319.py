# Generated by Django 3.1.2 on 2020-11-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='secondary_genre',
            field=models.CharField(blank=True, choices=[('FANT', 'Fantasy'), ('CRIM', 'Crime & Thriller'), ('FICT', 'Fiction'), ('SCFI', 'Science Fiction'), ('HORR', 'Horror'), ('ROMA', 'Romance'), ('TEEN', 'Teen & Young Adult'), ('KIDS', "Children's Books"), ('ANIM', 'Anime & Manga'), ('OTHR', 'Others')], max_length=4, null=True),
        ),
    ]
