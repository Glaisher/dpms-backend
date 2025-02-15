# serializers.py
from rest_framework import serializers
from .models import Permit, ActivityLog


class PermitSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    full_name = serializers.CharField(source='employee.full_name', read_only=True)
    department = serializers.CharField(source='employee.department', read_only=True)

    class Meta:
        model = Permit
        fields = ['id', 'employee', 'employee_id', 'full_name', 'department', 'permit_type', 'valid_from', 'valid_until', 'justification', 'status', 'permit_status', 'qr_code', 'created_at', 'updated_at']
        read_only_fields = ['id', 'qr_code', 'created_at', 'updated_at', 'status', 'permit_status', 'qr_code', 'employee', 'employee_id', 'full_name', 'department']


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'permit', 'action', 'performed_by', 'comment', 'timestamp']


class PermitUpdateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(allow_blank=True)

    class Meta:
        model = Permit
        fields = ['status', 'comment']
