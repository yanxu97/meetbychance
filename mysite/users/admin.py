from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,travel_Plan

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
   model = UserProfile


class UserProfileAdmin(UserAdmin):
   inlines = [UserProfileInline, ]




@admin.register(travel_Plan)
class travel_PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_id','user','country','state','city','budget')


admin.site.register(User, UserProfileAdmin)
