from django.contrib import admin
from .models import Question, Choice

# Choice 인라인 (Tabular 형식)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# Question 모델 커스터마이징
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("제목", {"fields": ["question_text"]}),
        ("날짜정보", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

# 관리자에 등록
admin.site.register(Question , QuestionAdmin)
admin.site.register(Choice)