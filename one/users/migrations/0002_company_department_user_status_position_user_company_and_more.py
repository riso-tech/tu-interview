# Generated by Django 4.2.8 on 2023-12-21 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Company Name")),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Department Name")),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.company")),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="status",
            field=models.CharField(
                choices=[(2, "Active"), (1, "Not Started"), (0, "Terminated")],
                default=1,
                max_length=10,
                verbose_name="Status",
            ),
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Position Name")),
                ("department", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.department")),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="company",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="users.company"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="department",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="users.department"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="position",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="users.position"
            ),
        ),
    ]