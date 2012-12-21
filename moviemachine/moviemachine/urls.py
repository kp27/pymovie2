from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',


    url(r'^movies/seed_movies','machineapp.views.seed_movies'),
    url(r'^movies/parse_daily','machineapp.views.parse_daily'),
    url(r'^movies/details/(\d+)', 'machineapp.views.details'),
    url(r'^movies/about', 'machineapp.views.about'),
    url(r'^movies/thanks', 'machineapp.views.thanks'),
    url(r'^movies/feedback', 'machineapp.views.feedback'),
    url(r'^movies/', 'machineapp.views.index'),
    url(r'media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    url(r'', 'machineapp.views.redir'),

    # Examples:
    # url(r'^$', 'moviemachine.views.home', name='home'),
    # url(r'^moviemachine/', include('moviemachine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
#urlpatterns += patterns('',
#
#    # Static files url.
#    (r'media/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT})
#    )


