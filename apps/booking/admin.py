from django.contrib import admin, messages
from .models import Booking
from .tasks import update_status

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_date', 'end_date')

    actions = ['run_update_status_task']

    def run_update_status_task(self, request, queryset):

        update_status.delay()
        self.message_user(request, " Celery task started successfully!", level=messages.SUCCESS)

    run_update_status_task.short_description = "Run Update Status Task"

