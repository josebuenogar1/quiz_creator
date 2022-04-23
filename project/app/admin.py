from django.contrib import admin
from app.models import Profile, Quiz,QuizOptions,QuizType,Questions
# Register your models here.

class QuizGetters(admin.ModelAdmin):
    list_display = ('get_true_answer','get_false_answer_one','get_false_answer_two')


admin.site.register(Profile)
admin.site.register(Quiz)
admin.site.register(QuizOptions,QuizGetters)
admin.site.register(QuizType)
admin.site.register(Questions)