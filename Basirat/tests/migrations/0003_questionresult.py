# Generated by Django 5.0.1 on 2024-03-18 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_alter_test_options_testresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.question')),
                ('test_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testresult')),
            ],
        ),
    ]
