from django.contrib import admin
from profileuseraccount.models import UserProfile, Members, Producers


class UserProfileInline(admin.TabularInline):
    model = UserProfile


# use the inline in the User admin
"""
admin.site.register(User,MyUserAdmin)
class UserAdmin(admin.ModelAdmin):
     inlines = [UserProfileInline]
"""

admin.site.register(Members)
admin.site.register(Producers)
admin.site.register(UserProfile)
