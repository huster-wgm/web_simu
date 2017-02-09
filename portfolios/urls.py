from django.conf.urls import url

from . import views

app_name = 'portfolios'
urlpatterns = [
    # ex: /simulator
    url(r'^simulator$', views.simulator, name="simulator"),
    # ex: /simu_result
    url(r'^simu_result$', views.simulation_result, name="simu_result"),
    # ex: /bio_calculator
    url(r'^bio_calculator$', views.bio_calculator, name="bio_calculator"),
    # ex: /congestion
    url(r'^congestion_map$', views.congestion, name="congestion_map"),
    # ex: /bio_result
    url(r'^bio_result$', views.bio_result, name="bio_result"),
]
