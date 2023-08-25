from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('submit-response/', views.submit_response, name="submit-response"),
    path('dept-submit-response/', views.dept_submit_response, name="dept-submit-response"),
    path('society/', views.society, name="society"),
    path('department/', views.department, name="department"),
    path('department-result/', views.department_result, name="department-result"),
    path('admin-portal/', views.admin_portal, name="admin-portal")

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
