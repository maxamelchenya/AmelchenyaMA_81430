from django.contrib.auth import authenticate
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import BidHistory, Category, Coin, Country, User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]

        extra_kwargs = {
            "email": {
                "write_only": True,
            },
            "username": {"write_only": True},
            "password": {"write_only": True, "min_length": 8},
        }

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "created_at", "is_superuser"]


class CoinSerializer(serializers.ModelSerializer):
    end_date = serializers.DateTimeField(format="%H:%M %d-%m-%Y", read_only=True)

    class Meta:
        model = Coin
        fields = [
            "id",
            "user",
            "country",
            "category",
            "status",
            "name",
            "image",
            "description",
            "year",
            "price",
            "end_date",
        ]

    def to_representation(self, obj):
        self.fields["user"] = serializers.CharField(source="user.username")
        self.fields["country"] = serializers.CharField(source="country.name")
        self.fields["category"] = serializers.CharField(source="category.name")
        return super().to_representation(obj)


class BidCoinSerializer(CoinSerializer):
    class Meta(CoinSerializer.Meta):
        read_only_fields = [
            "id",
            "user",
            "country",
            "category",
            "status",
            "name",
            "image",
            "description",
            "year",
        ]

    def validate(self, data):
        price = data["price"]
        instance = getattr(self, "instance", None)
        if instance.price >= price:
            raise serializers.ValidationError(
                {
                    "Error": _(
                        f"Ваша ставка {price} должна быть больше текущей цены: {instance.price}!"
                    )
                }
            )
        return data

    def update(self, coin, validated_data):
        with transaction.atomic():
            price = validated_data.get("price", coin.price)
            user = self.context["request"].user
            coin.price = price
            coin.save()
            BidHistory.objects.create(coin=coin, price=price, user=user)
            return coin


class AddCoinSerializer(CoinSerializer):
    class Meta(CoinSerializer.Meta):
        read_only_fields = [
            "id",
            "user",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        credit_card = Coin.objects.create(user=user, **validated_data)
        return credit_card


class UserCreationStatisticSerializer(serializers.Serializer):
    month = serializers.DateTimeField(format="%m.%Y")
    id__count = serializers.IntegerField()
