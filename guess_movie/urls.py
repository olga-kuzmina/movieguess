from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'guess_movie.views.guess'),
    url(r'^add$', 'guess_movie.views.add'),
    url(r'^guess$', 'guess_movie.views.guess'),
    url(r'^rating$', 'guess_movie.views.rating'),
    url(r'^register$', 'guess_movie.views.register'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'})
    # Examples:
    # url(r'^$', 'guess_movie.views.home', name='home'),
    # url(r'^guess_movie/', include('guess_movie.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
    )