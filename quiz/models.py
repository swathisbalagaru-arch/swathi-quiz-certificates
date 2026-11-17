import secrets

from django.db import models

PASS_PERCENT = 60


def make_certificate_id():
    return "SW-" + secrets.token_hex(4).upper()


class Result(models.Model):
    student_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    score = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    certificate_id = models.CharField(
        max_length=20, unique=True, default=make_certificate_id, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def percent(self):
        return round(self.score * 100 / self.total) if self.total else 0

    @property
    def passed(self):
        return self.percent >= PASS_PERCENT

    def __str__(self):
        return f"{self.student_name} - {self.category} ({self.score}/{self.total})"
