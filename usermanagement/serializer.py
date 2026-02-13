from rest_framework import serializers
from account.models  import UserAccount

class UserSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = ["id","username","email","role","status",]

    def get_status(self, obj):
        return "active" if obj.is_active else "block"
