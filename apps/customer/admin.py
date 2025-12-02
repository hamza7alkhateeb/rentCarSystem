from django.contrib import admin , messages
from .models import Customer
from .tasks import sync_customers_status_task,sync_single_customer_status_task

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_username','status','phone_number')

    actions = ['run_sync_customers_status_task','run_sync_single_customers_task']

    def get_username(self,obj):
        return obj.user.username

    get_username.short_description = "Username"

    def run_sync_customers_status_task(self, request, queryset):
        sync_customers_status_task.delay()
        self.message_user(request, "Customer status task is running.")

    run_sync_customers_status_task.short_description = "Update ALL customer statuses"

    def run_sync_single_customers_task(self, request, queryset):
        count =0
        for customer in queryset:
            sync_single_customer_status_task.delay(customer.id)
            count += 1

        self.message_user(request, f"Task started: Updating status for {count} selected customers.")
    run_sync_single_customers_task.short_description = "Update SELECTED customers statuses"