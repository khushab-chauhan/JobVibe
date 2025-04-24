from django.contrib import admin
from apps.users.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','account_type','is_active']
    list_filter = ['account_type','is_active']
    list_editable = ['email','is_active','account_type']
    search_fields = ['email','account_type']
    list_per_page = 2
    # ordering = ('-date_joined',)
    readonly_fields = ('email','password')
    fieldsets = (
        ('login information',{
            'fields' :('email','password')
        }),
        ('permission',{
            'fields':('account_type','is_active')
        }),
    )

    admin.site.site_header = "JobVibe Admin"
    admin.site.site_title = "JobVibe Admin Portal"
    admin.site.index_title = "Welcome to the JobVibe Admin Dashboard"

admin.site.register(User,UserAdmin)

