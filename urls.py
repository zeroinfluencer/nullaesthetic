from django.conf.urls.defaults import patterns

import views

urlpatterns = patterns('',
    ( r"^admin/ensure_aesthetic_options_defaults/?$", views.ensure_aesthetic_options_defaults ),
    ( r"^random_aesthetic/?$", views.random_aesthetic ),
)

