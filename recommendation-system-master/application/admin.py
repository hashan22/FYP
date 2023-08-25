from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Question)
admin.site.register(Answer)
#admin.site.register(UserResponse)
admin.site.register(Combination)

admin.site.register(Dept_Question)
admin.site.register(Dept_Answer)
#admin.site.register(Dept_UserResponse)
admin.site.register(Dept_Combination)