from django.conf import settings
from django.db import models

class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT='PRESENT','Present'; LATE='LATE','Late'; ABSENT='ABSENT','Absent'; REMOTE='REMOTE','Remote'; LEAVE='LEAVE','On Leave'
    employee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='attendance_records')
    date=models.DateField()
    clock_in=models.TimeField(null=True,blank=True)
    clock_out=models.TimeField(null=True,blank=True)
    status=models.CharField(max_length=16,choices=Status.choices,default=Status.PRESENT)
    notes=models.CharField(max_length=255,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-date','employee__full_name']; constraints=[models.UniqueConstraint(fields=['employee','date'],name='uniq_attendance_employee_date')]
    def __str__(self): return f'{self.employee} - {self.date}'
