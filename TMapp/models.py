from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        # Fetch Role instance
        role_name = extra_fields.pop('role', 'USER')  # Default to 'USER'
        role, _ = Role.objects.get_or_create(name=role_name)  # Fetch or create role

        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with admin privileges."""
        extra_fields.setdefault('role', 'SUPER_ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Role Model
class Role(models.Model):
    ROLE_CHOICES = [
        ('SUPER_ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50,unique=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(default='default/No-image-available.png', upload_to="profile_photos")

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name="users")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for Django Admin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email 

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    auth_token = models.CharField(max_length=100, null=True, blank=True)  # For email verification
    is_verified = models.BooleanField(default=False)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)  # For reset password
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class Project(models.Model):
        id = models.AutoField(primary_key=True)
        project_name = models.CharField(max_length=100,null=True)
        project_type = models.CharField(max_length=100,null=True)
        created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_project")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"{self.project_name} {self.project_type}"

# Task Model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="projects" ,default='0')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    status = models.CharField(max_length=20, default="PENDING")
    priority = models.CharField(max_length=20, default="LOW")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
