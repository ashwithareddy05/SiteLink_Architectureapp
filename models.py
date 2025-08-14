from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('firm', 'Firm'),
        ('client', 'Client'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# class Firm(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     location = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name
# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Firm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='firm_logos/', blank=True, null=True)

    def __str__(self):
        return self.name



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Internship(models.Model):
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    responsibilities = models.TextField()
    requirements = models.TextField()
    stipend = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    duration = models.CharField(max_length=100, default="6 months")
    deadline = models.DateField()
    perks = models.CharField(max_length=255)
    mode = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

class InternshipApplication(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    college_name = models.CharField(max_length=255)
    year_of_passing = models.IntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    achievements = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.internship.title}"

from django.utils import timezone  # Make sure this is at the top

class HouseProject(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='house_projects')
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE, null=True, blank=True, related_name='approved_projects')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    approval_message = models.TextField(blank=True, null=True)
    firm_response = models.TextField(blank=True, null=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    area_sqft = models.IntegerField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.user.username} - {self.message[:50]}"
