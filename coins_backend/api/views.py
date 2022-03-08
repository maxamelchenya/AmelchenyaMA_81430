import datetime
from collections import OrderedDict

from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser
from .models import Category, Coin, Country, User
from .serializers import (
    AddCoinSerializer,
    BidCoinSerializer,
    CategorySerializer,
    CoinSerializer,
    CountrySerializer,
    LoginSerializer,
    SignUpSerializer,
    UserCreationStatisticSerializer,
    UserSerializer,
)


class SignUpView(GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"Success": "User created successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(instance=user).data}
        )


class ListCategoryView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ListCountryView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class ListAllCoinsView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = CoinSerializer
    queryset = Coin.objects.filter(status=Coin.STATUS_CHOICES[1][0])
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["category__name", "country__name", "price"]
    ordering_fields = ["name", "year"]

    def get_queryset(self):
        min_price = self.request.GET.get("min_price", None)
        max_price = self.request.GET.get("max_price", None)
        if max_price and min_price:
            return self.queryset.filter(price__gte=min_price, price__lt=max_price)
        elif max_price:
            return self.queryset.filter(price__lt=max_price)
        elif min_price:
            return self.queryset.filter(price__gte=min_price)
        return self.queryset


class BidCoinView(GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = BidCoinSerializer
    queryset = Coin.objects.all()
    permission_classes = [IsAuthenticated]


class AddCoinView(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = AddCoinSerializer
    permission_classes = [IsAuthenticated]


class ListUsersCoinsView(ListAllCoinsView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        users_coins_queryset = Coin.objects.filter(user=user)
        min_price = self.request.GET.get("min_price", None)
        max_price = self.request.GET.get("max_price", None)
        if max_price and min_price:
            return users_coins_queryset.filter(price__gte=min_price, price__lt=max_price)
        elif max_price:
            return users_coins_queryset.filter(price__lt=max_price)
        elif min_price:
            return users_coins_queryset.filter(price__gte=min_price)
        return users_coins_queryset

    @action(methods=["POST"], detail=True)
    def put_up_for_sale(self, request, *args, **kwargs):
        coin = self.get_object()
        coin.status = Coin.STATUS_CHOICES[1][0]
        coin.save()
        return Response(
            data=self.serializer_class(instance=coin).data, status=status.HTTP_200_OK
        )


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class UserCreationStatisticView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = UserCreationStatisticSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        # returns statistics about how many users were created
        # every mont for last 365 days
        date_from = timezone.now() - datetime.timedelta(days=365)
        queryset = (
            User.objects.filter(created_at__gte=date_from)
            .annotate(month=TruncMonth("created_at"))
            .values("month", year=TruncYear("month"))
            .annotate(Count("id"))
            .order_by("year", "month")
        )
        return queryset
