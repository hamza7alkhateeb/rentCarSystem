from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "brand",
        "model",
        "year",
        "vehicle_type",
        "daily_rate",
        "plate_number",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "brand")
    list_filter = (
        "vehicle_type",
        "year",
        "created_at",
    )
    search_fields = (
        "brand",
        "model",
        "plate_number",
    )
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Basic Info", {
            "fields": ("brand", "model", "year", "vehicle_type", "description")
        }),
        ("Pricing & Plate", {
            "fields": ("daily_rate", "plate_number")
        }),
        ("Media", {
            "fields": ("image",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )