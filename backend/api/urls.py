from django.urls import path
from . import views

urlpatterns = [
    # Pages (HTML)
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_page, name='login'),
    path('profile/', views.profile_page, name='profile'),
    path('settings-ui/', views.settings_page, name='settings_ui'),
    path('memory-ui/', views.memory_page, name='memory_ui'),
    path('reminders-ui/', views.reminders_page, name='reminders_ui'),

    # Data API (JSON)
    path('api/auth/register/', views.register_view),
    path('api/auth/login/', views.login_view),
    path('api/auth/logout/', views.logout_view),
    path('api/auth/me/', views.me_view),
    
    path('api/settings/', views.settings_view),
    path('api/chats/', views.chat_list),
    path('api/chats/<int:chat_id>/', views.chat_detail),
    path('api/chats/<int:chat_id>/messages/', views.chat_messages),
    
    path('api/memories/', views.memory_list),
    path('api/memories/<int:memory_id>/', views.memory_detail),
    
    path('api/reminders/', views.reminder_list),
    path('api/reminders/<int:reminder_id>/', views.reminder_detail),
]
