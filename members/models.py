from django.db import models
from django.core.validators import FileExtensionValidator

class Member(models.Model):
  id = models.AutoField(primary_key=True)
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)


  def __str__(self):
    return self.firstname

class Subject(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name


class Class(models.Model):
  id = models.AutoField(primary_key=True)
  subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
  start_hour = models.TimeField()
  end_hour = models.TimeField()
  weekday = models.IntegerField(default=0)

  def __str__(self):
    # 1. Map integers to acronyms
    days = {
      0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu",
      4: "Fri", 5: "Sat", 6: "Sun"
    }
    day_acronym = days.get(self.weekday, "???")

    # 2. Format the time to 24h (HH:MM)
    # %H is 24-hour format, %M is minutes
    time_string = self.start_hour.strftime('%H:%M')

    return f"{self.subject.name}_{time_string}_{day_acronym}"



class File(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)

    file = models.FileField(
        upload_to='files/%Y/%m',
        validators=[FileExtensionValidator(allowed_extensions=['txt'])]
    )

    def __str__(self):
        return self.filename
