
from django.urls import path
from . import views
urlpatterns = [
    path('leave_form',views.leave),
    path('view_leave/<str:userid>',views.view_leave),
    path('edit_leave',views.edit_leave),
    path('delete_leave',views.delete_leave),
   
   
]