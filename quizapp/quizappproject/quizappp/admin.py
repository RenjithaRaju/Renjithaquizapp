from django.contrib import admin
from . models import user_register,questions,Quizresult

# Register your models here.
admin.site.register(user_register)
admin.site.register(questions)
admin.site.register(Quizresult)