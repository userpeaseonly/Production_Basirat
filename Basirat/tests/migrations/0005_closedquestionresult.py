# Generated by Django 5.0.1 on 2024-04-14 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_testsession'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosedQuestionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_answer', models.TextField()),
                ('is_correct', models.BooleanField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.question')),
                ('test_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testresult')),
            ],
        ),
    ]
