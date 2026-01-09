from django.utils import timezone
from .models import CustomUser


class AutoUpdateDriverStatusMiddleware:
    """
    Middleware to automatically update driver status from on_leave/emergency to available
    when their leave/emergency period has ended.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update driver statuses before processing the request
        self.update_expired_leave_status()
        response = self.get_response(request)
        return response

    def update_expired_leave_status(self):
        """Check and update drivers whose leave/emergency period has ended"""
        now = timezone.now()
        
        # Find drivers whose leave/emergency has ended
        expired_drivers = CustomUser.objects.filter(
            driver_status__in=['on_leave', 'emergency'],
            on_leave_until__isnull=False,
            on_leave_until__lte=now
        )
        
        # Update them to available
        for driver in expired_drivers:
            driver.driver_status = 'available'
            driver.on_leave_until = None
            driver.save(update_fields=['driver_status', 'on_leave_until'])
