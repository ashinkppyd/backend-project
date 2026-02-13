from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")

    def validate(self, data):
        if data.get("is_default"):
            user = self.context["request"].user
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return data
