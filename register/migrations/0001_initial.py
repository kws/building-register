# Generated by Django 3.2.9 on 2021-11-05 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('user_agent', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, unique=True)),
                ('method', models.CharField(choices=[('email', 'EMail'), ('phone', 'Phone')], max_length=5)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SignInRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('sign_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sign_in', to='register.auditrecord')),
                ('sign_out', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sign_out', to='register.auditrecord')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['sign_in__timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ContactValidationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('expires', models.DateTimeField()),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.contactdetails')),
            ],
        ),
    ]
