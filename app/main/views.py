# views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .permissions import IsEmployee, IsAdmin, IsSecurity
from .models import Permit, ActivityLog
from .serializers import PermitSerializer, ActivityLogSerializer, PermitUpdateSerializer
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser


class PermitViewSet(viewsets.ModelViewSet):
    queryset = Permit.objects.all()

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [permissions.IsAuthenticated()]

        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsEmployee()]
        elif self.action == 'list':
            if self.request.user.is_admin():
                return [permissions.IsAuthenticated(), IsAdmin()]
            else:
                return [permissions.IsAuthenticated(), IsEmployee()]
        elif self.action == 'retrieve':
            if self.request.user.is_admin():
                return [permissions.IsAuthenticated(), IsAdmin()]
            else:
                return [permissions.IsAuthenticated(), IsEmployee()]
        elif self.action == 'update':
            return [permissions.IsAuthenticated(), IsAdmin()]
        elif self.action == 'partial_update':
            return [permissions.IsAuthenticated(), IsAdmin()]
        elif self.action == 'verify':
            return [permissions.IsAuthenticated(), IsSecurity()]
        else:
            return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PermitUpdateSerializer
        return PermitSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_admin():
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(employee=request.user)

        serializer = PermitSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Staff can create new permits
        serializer = PermitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(employee=request.user)
        ActivityLog.objects.create(
            permit=serializer.instance,
            action='created',
            performed_by=request.user,
            comment='Permit application submitted'
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        # Admin approves or rejects a permit
        permit = get_object_or_404(Permit, pk=pk)
        status = request.data.get('status')
        comment = request.data.get('comment', '')

        if status not in ['Approved', 'Rejected']:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        permit.status = status
        permit.save()

        # Log the approval or rejection action
        ActivityLog.objects.create(
            permit=permit,
            action=status,
            performed_by=request.user,
            comment=comment
        )

        return Response(PermitSerializer(permit).data)

    @action(detail=True, methods=['put'], permission_classes=[IsAdmin])
    def invalidate(self, request, pk=None):
        # Admin invalidates an active permit
        permit = get_object_or_404(Permit, pk=pk)
        if permit.status != 'approved':
            return Response({"detail": "Only approved permits can be invalidated"}, status=status.HTTP_400_BAD_REQUEST)

        permit.status = 'invalid'
        permit.save()

        # Log the invalidation action
        ActivityLog.objects.create(
            permit=permit,
            action='verified',  # Using "verified" action since it's technically a verification process
            performed_by=request.user,
            comment='Permit invalidated'
        )

        return Response(PermitSerializer(permit).data)


class VerifyPermitView(APIView):
    permission_classes = [IsAuthenticated, IsSecurity]
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        qr_code = request.data.get('qr_code')
        if not qr_code:
            return Response({"detail": "QR code is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            permit = get_object_or_404(Permit, qr_code=qr_code)
        except ValidationError:
            return Response({"detail": "Invalid QR code"}, status=status.HTTP_404_NOT_FOUND)

        # Log the verification action
        ActivityLog.objects.create(
            permit=permit,
            action='verified',
            performed_by=request.user,
            comment=f'Permit verified as {permit.permit_status}'
        )

        return Response(PermitSerializer(permit).data)

# class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ActivityLog.objects.all()
#     serializer_class = ActivityLogSerializer
#     permission_classes = [permissions.IsAuthenticated]
