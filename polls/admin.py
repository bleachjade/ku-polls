from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """Create a choice for polls app."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Create a question for polls app."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {
            'fields': ['pub_date', 'end_date'],
            'classes': ['collapse']
        }),
    ]
    inlines = [ChoiceInline]

    list_display = (
        'question_text',
        'pub_date',
        'was_published_recently',
        'end_date'
    )

    list_filter = ['pub_date']

    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
