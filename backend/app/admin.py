from django.contrib import admin
from .models import QuestionModel, FactModel, SayingModel, Number, ComplimentModel
from adminsortable2.admin import SortableAdminMixin
from django.utils.html import format_html


@admin.register(ComplimentModel)
class ComplimentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_filter = ("for_how", )


@admin.register(Number)
class NumberAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("value", "used_colored")
    list_filter = ("used",)

    def used_colored(self, obj):
        color = "green" if obj.used else "red"
        status = "Отработало" if obj.used else "Не отработало"
        return format_html('<b style="color:{};">{}</b>', color, status)
    used_colored.short_description = "Статус"

@admin.register(SayingModel)
class FactAdmin(admin.ModelAdmin):
    list_display = ("id", "short_text", "likes", "dislikes")
    search_fields = ("text",)
    list_filter = ("likes", "dislikes")
    ordering = ("-likes",)

    def short_text(self, obj):
        return (obj.text[:75] + "...") if len(obj.text) > 75 else obj.text
    short_text.short_description = "Текст мудрости"

@admin.register(FactModel)
class FactAdmin(admin.ModelAdmin):
    list_display = ("id", "short_text", "likes", "dislikes")
    search_fields = ("text",)
    list_filter = ("likes", "dislikes")
    ordering = ("-likes",)

    def short_text(self, obj):
        return (obj.text[:75] + "...") if len(obj.text) > 75 else obj.text
    short_text.short_description = "Текст факта"

@admin.register(QuestionModel)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "level", "correct_answer")  
    list_filter = ("level",) 
    search_fields = ("text", "answer1", "answer2", "answer3", "answer4")  
    list_editable = ("level", "correct_answer")  
    ordering = ("level",)  

    fieldsets = (
        ("Вопрос", {
            "fields": ("text", "level")
        }),
        ("Варианты ответов", {
            "fields": ("answer1", "answer2", "answer3", "answer4", "correct_answer")
        }),
    )
