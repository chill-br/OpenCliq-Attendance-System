from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attendance 

class AttendanceStatsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"is_online": request.user.is_online})

    def post(self, request):
        user = request.user
        if user.is_online:
            return Response({"status": "error", "message": "Already checked in."}, status=400)

        data = request.data
        Attendance.objects.create(
            user=user,
            check_in=timezone.now(),
            date=timezone.now().date(),
            work_mode=data.get('work_mode', 'OFFICE'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        user.is_online = True
        user.save()
        return Response({"status": "success", "message": "Checked in via API"}, status=200)