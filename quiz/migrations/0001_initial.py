import quiz.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Result",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("student_name", models.CharField(max_length=100)),
                ("category", models.CharField(max_length=50)),
                ("score", models.PositiveIntegerField()),
                ("total", models.PositiveIntegerField()),
                ("certificate_id", models.CharField(default=quiz.models.make_certificate_id, editable=False, max_length=20, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
