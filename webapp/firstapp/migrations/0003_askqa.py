# Generated by Django 5.0.6 on 2024-07-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_rename_tranking_tracking_tracking'),
    ]

    operations = [
        migrations.CreateModel(
            name='AskQA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='ชื่อติดต่อ')),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='email')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='หัวข้อ')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='รายละเอียด')),
            ],
        ),
    ]
