from django.db import models

class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=11)
    student_email = models.EmailField(max_length=254, default='null')
    student_password = models.CharField(max_length=128)
    student_phone = models.CharField(max_length=15, null=True)

class Meetup(models.Model):
    meetup_id = models.AutoField(primary_key=True)
    meetup_name = models.CharField(max_length=30)
    meetup_description = models.CharField(max_length=100)
    meetup_date = models.DateField()
    meetup_location = models.CharField(max_length=50)
    meetup_poster = models.ImageField(upload_to='posters/', blank=True, null=True) 

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=100)
    comment_created_time = models.DateTimeField(auto_now_add=True)



class Registration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    registration_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Updated



class Staff(models.Model):
    staff_id = models.CharField(max_length=10, primary_key=True)
    staff_email = models.EmailField()
    staff_password = models.CharField(max_length=20)
    staff_phone = models.CharField(max_length=15)

