from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user/<int:pk>/profile/$', views.profile, name='profile'),
    path('user/<int:pk>/profile/update/$', views.profile_update, name='profile_update'),
    path('user/<int:pk>/pwdchange/$', views.pwd_change, name='pwd_change'),
    path('logout/', views.logout, name='logout'),
    # path('user/int:<pk>/plan/detail/<int:planpk>/$', views.plan, name='plan'),
    path('plan/post/<int:pk>/$', views.post_plan, name='post_plan'),
    # grab matched data from the database
    path('matched_list/<int:pk>/$', views.matched_list, name='matched_list'),

    # delete the latest record
    #path('delete/detail/<int:pk>/$', views.delete, name='delete'),

    # what is hot
    path('whatishot/detail/<int:pk>/$', views.topone, name='topone'),

    #saxue
    path('search/',views.search,name='search'),
    path('search/detail', views.search_detail, name='search_detail'),

    path('user/<int:pk>/plan_list/$',views.plan_list,name='plan_list'),
    path('user/<int:pk>/plan/detail/<int:planpk>/$', views.plan_detail, name='plan_detail'),
    path('user/<int:pk>/plan/delete/<int:planpk>/$', views.plan_delete, name='plan_delete'),
    path('user/<int:pk>/plan/update/<int:planpk>/$', views.plan_update, name='plan_update'),
    path('user/<int:pk>/plan/update/action/<int:planpk>/$', views.plan_up, name='plan_up'),

    # sheng
    path('whatishot/detaillalaland/$', views.hotbybudget, name='hotbybudget'),
    # path('whatishot/currdata/$', views.hotbybudget, name = 'hotbybudget')
    path('whatishot/serve/$', views.serve, name='serve'),
    path('whatishot/map/$', views.map, name='map'),


    # confirm
    path('matched_list/<int:pk>/<int:myPlanPK>/confirm_information/$', views.confirm, name='confirm'),
    path('matched_list/<int:pk>/<int:myPlanPK>/confirm_1_information/$', views.confirm_1, name='confirm_1'),
    path('matched_list/<int:pk>/<int:myPlanPK>/confirm_2_information/$', views.confirm_2, name='confirm_2'),
    # reject
    path('matched_list/<int:pk>/<int:myPlanPK>/reject_information/$', views.reject, name='reject'),
path('matched_list/<int:pk>/<int:myPlanPK>/reject_1_information/$', views.reject_1, name='reject_1'),

path('matched_list/<int:pk>/<int:myPlanPK>/reject_2_information/$', views.reject_2, name='reject_2'),
    path('home/', views.home, name='home'),
path('homeLogin/', views.homeLogin, name='homeLogin'),
path('whatishot/<int:pk>/$', views.chart, name='chart'),

]

