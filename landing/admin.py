from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Application, 
    CriminalApplication, 
    AdministrativeApplication, 
    CivilApplication, 
    BusinessApplication,
    BlogPost,
    CourtCase,
    HeroSettings
)

# Customize Admin Site Branding
admin.site.site_header = "Universal Law Forum | CRM Tizimi"
admin.site.site_title = "Universal Law Forum Boshqaruv Paneli"
admin.site.index_title = "Mijozlar Murojaatlari va Kontent Boshqaruvi"

class BaseApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status_colored', 'created_at', 'notes')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    exclude = ('category',)

    def status_colored(self, obj):
        color_map = {
            'new': 'red',
            'in_progress': 'orange',
            'completed': 'green',
        }
        color = color_map.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: 700">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Holat / Статус'
    status_colored.admin_order_field = 'status'


@admin.register(CriminalApplication)
class CriminalApplicationAdmin(BaseApplicationAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.category = 'criminal'
        super().save_model(request, obj, form, change)


@admin.register(AdministrativeApplication)
class AdministrativeApplicationAdmin(BaseApplicationAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.category = 'administrative'
        super().save_model(request, obj, form, change)


@admin.register(CivilApplication)
class CivilApplicationAdmin(BaseApplicationAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.category = 'civil'
        super().save_model(request, obj, form, change)


@admin.register(BusinessApplication)
class BusinessApplicationAdmin(BaseApplicationAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.category = 'business'
        super().save_model(request, obj, form, change)


# Master List containing all applications for broad oversight
@admin.register(Application)
class AllApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'category', 'status_colored', 'created_at', 'notes')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)
    fields = ('name', 'phone', 'category', 'description', 'status', 'notes', 'created_at')
    ordering = ('-created_at',)

    def status_colored(self, obj):
        color_map = {
            'new': 'red',
            'in_progress': 'orange',
            'completed': 'green',
        }
        color = color_map.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: 700;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Holat / Статус'
    status_colored.admin_order_field = 'status'


# BlogPost Admin Configuration
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


# CourtCase Admin Configuration
@admin.register(CourtCase)
class CourtCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'result', 'category', 'created_at')
    list_filter = ('result', 'category', 'created_at')
    search_fields = ('title', 'title_ru', 'description', 'description_ru')
    ordering = ('-created_at',)
    fieldsets = (
        ("O'zbekcha / Узбекский", {
            'fields': ('title', 'description'),
        }),
        ('Ruscha / Русский', {
            'fields': ('title_ru', 'description_ru'),
            'description': 'Rus tilidagi tarjima (ixtiyoriy). Agar bo\'sh qoldirilsa, o\'zbekcha matn ko\'rsatiladi.',
        }),
        ('Umumiy / Общее', {
            'fields': ('result', 'category'),
        }),
    )


# HeroSettings Admin Singleton Configuration
@admin.register(HeroSettings)
class HeroSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title_uz', 'title_ru')
    
    def has_add_permission(self, request):
        # Only allow adding if there is no instance yet
        return self.model.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        # Do not allow deleting the singleton setting
        return False

