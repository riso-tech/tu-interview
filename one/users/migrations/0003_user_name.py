# Generated by Django 4.2.8 on 2023-12-21 04:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_company_department_user_status_position_user_company_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name="Full Name"),
        ),
    ]