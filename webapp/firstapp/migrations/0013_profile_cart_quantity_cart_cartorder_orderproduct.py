# Generated by Django 5.0.6 on 2024-08-22 03:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0012_order_not_complete_order_tracking_number_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cart_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=14)),
                ('email', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('express', models.CharField(blank=True, max_length=100, null=True)),
                ('other', models.TextField(blank=True, null=True)),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('payment', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('slip', models.ImageField(blank=True, null=True, upload_to='cart-slip/')),
                ('slip_time', models.DateField(blank=True, null=True)),
                ('bank_account', models.CharField(choices=[('KBank', 'KBank'), ('SCB', 'SCB'), ('TTB', 'TTB'), ('BBL', 'BBL'), ('BAY', 'BAY'), ('อื่นๆ', 'อื่นๆ')], default='KBank', max_length=50)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstapp.product')),
            ],
        ),
    ]
