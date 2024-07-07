from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Manager

class ManagerAdmin(UserAdmin):
    # Определение полей, которые будут отображаться в списке
    list_display = ('username', 'email', 'first_name', 'last_name', 'type_user', 'is_staff', 'is_active')
    # Определение полей, по которым можно будет фильтровать
    list_filter = ('type_user', 'is_staff', 'is_active')
    # Определение полей, по которым можно будет искать
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Поля, которые можно редактировать на странице списка
    list_editable = ('type_user', 'is_staff', 'is_active')
    # Поля, которые будут отображаться при создании новой записи
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'type_user')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # Поля, которые будут отображаться при изменении существующей записи
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'type_user', 'is_staff', 'is_active'),
        }),
    )
    # Поле, по которому будут сортироваться записи
    ordering = ('username',)
    # Поле, которое используется для идентификации пользователя
    USERNAME_FIELD = 'username'
    # Дополнительные обязательные поля при создании пользователя
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

# Регистрация модели Manager и её административного интерфейса
admin.site.register(Manager, ManagerAdmin)
