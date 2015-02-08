from django.conf.urls import patterns, include, url
from django.contrib import admin
from checkers import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ai.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.homepage, name='homepage'),
    url(r'^make_move/', views.make_move, name='make_move'),
    url(r'^get_available_moves_for_pawn/', views.get_available_moves_for_pawn,
        name="get available moves for pawn"),
    url(r'^update_board/', views.update_board,
        name="validate and update board")
)
