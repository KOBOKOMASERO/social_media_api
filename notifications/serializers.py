from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor_username', 'verb', 'target_repr', 'is_read', 'timestamp']

    def get_target_repr(self, obj):
        return str(obj.target) if obj.target else None
