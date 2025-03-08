from django.contrib import admin
from .models import Project, User, Role, Task, UserProfile

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(Project)
