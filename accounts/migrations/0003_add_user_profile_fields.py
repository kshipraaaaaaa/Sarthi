from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(
                max_length=30,
                choices=[
                    ('Male', 'Male'),
                    ('Female', 'Female'),
                    ('Other', 'Other'),
                    ('Prefer not to say', 'Prefer not to say'),
                ],
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_no',
            field=models.CharField(
                max_length=15,
                null=True,
                blank=True,
            ),
        ),
    ]
