from django.conf.urls import patterns, include, url
from django.contrib import admin
from basic import views as basic_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xAlbatross.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r"^signup/$", basic_views.register_user, name="signup"),
    #url(r'^register_success/', basic_views.post_registration),
    url(r'^confirm/(?P<activation_key>\w+)/', basic_views.register_confirm),
    url(r"^login/$", basic_views.custom_login, name="login"),
    url(r"^home/$", basic_views.home_page),
    url(r"^inactive/$", basic_views.inactive),
)
