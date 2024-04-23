from django.urls import path
from . import view
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('',view.getData),
    path('add/', view.addData),
    path('profile/', view.profilePicture),
    path('signup/', view.signUp),
    path('uploadProfilePicture/',view.uploadPicture),
    path('pagination/',view.showAll),
    path('delete-item/', view.delete_item),
    path('already-registered-page/', view.alreadyregister ),
    path('validatesignin/',view.checkUser)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

