from django.urls import path
from . import views
urlpatterns = [
    path('view_leave',views.view_all_leaves),
    path('pending_leave',views.pending_leave),
    path('approve_or_reject',views.approve_or_reject),
     path('admin_dashboard',views.admin_dashboard),
 
   
]