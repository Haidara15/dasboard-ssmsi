
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from dashboard.admin import admin_statistiques, admin_import_xlsx

urlpatterns = [
    path("admin/statistiques/", admin_statistiques, name="admin_statistiques"),
    path("admin/import/", admin_import_xlsx, name="admin_import_xlsx"),
    path("admin/", admin.site.urls),
    path("admin/logout/", lambda request: redirect('/admin/login/?next=/admin/'), name="logout"),
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(), name="admin_password_reset"),
    path("admin/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("admin/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("admin/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)