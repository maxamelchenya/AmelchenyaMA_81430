from django.urls import path
from rest_framework import routers

from .views import (
    AddCoinView,
    BidCoinView,
    ListAllCoinsView,
    ListCategoryView,
    ListCountryView,
    ListUsersCoinsView,
    LoginView,
    SignUpView,
    UserCreationStatisticView,
)

router = routers.DefaultRouter()

router.register("signup", SignUpView, basename="signup")
router.register("countries", ListCountryView, basename="countries")
router.register("categories", ListCategoryView, basename="categories")
router.register("all-coins", ListAllCoinsView, basename="all-coins")
router.register("bid-coin", BidCoinView, basename="bid-coin")
router.register("add-coin", AddCoinView, basename="add-coin")
router.register("users-coins", ListUsersCoinsView, basename="users-coins")
router.register(
    "user-creation-statistic",
    UserCreationStatisticView,
    basename="user-creation-statistic",
)

urlpatterns = router.urls
urlpatterns += [
    path("login/", LoginView.as_view(), name="login"),
]
