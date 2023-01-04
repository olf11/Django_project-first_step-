# Generated by Django 4.1.3 on 2023-01-04 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_rename_owner_choice_user_rename_owner_question_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='user_ip')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question', verbose_name='user questions votes')),
            ],
        ),
    ]
