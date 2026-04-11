from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    Setting, Slider, Leadership, Why_Choose, Contact_Page,
    Our_Team,Testimonial, FAQ, ImpactMetric, Service, FooterLink,
    ContactEnquiry,Our_Industry,Our_Clients,About_Us,Awards_Recognition
)

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):

    list_display = (
        "site_name",
        "status",
        "phone",
        "email",
        "logo_preview",
    )

    list_filter = ("status",)
    search_fields = ("site_name", "email", "phone")
    readonly_fields = ("logo_preview",)

    fieldsets = (

        ("🧠 Basic Branding", {
            "fields": (
                "site_name",
                "logo",
                "favicon",
                "logo_preview",
            )
        }),

        ("🎨 Theme Colors", {
            "fields": (
                "header_footer_color",
                "text_color",
                "button_color",
                "rera_color",
            )
        }),

        ("📍 Contact Details", {
            "fields": (
                "address",
                "phone",
                "whatsapp",
                "email",
                "google_map",
            )
        }),

        ("✉️ SMTP / Email Settings", {
            "fields": (
                "smtpserver",
                "smtpemail",
                "smtppassword",
                "smtpport",
            )
        }),

        ("🌐 Social Media", {
            "fields": (
                "facebook",
                "instagram",
                "twitter",
                "youtube",
            )
        }),

        ("🔍 SEO Settings", {
            "fields": (
                "meta_title",
                "meta_description",
                "meta_keywords",
            )
        }),

        ("📑 Legal Pages", {
            "fields": (
                "privacy_policy",
                "terms_conditions",
                "disclaimer",
                "cookies",
            )
        }),

        ("⚙️ Extra Settings", {
            "fields": (
                "search_bg",
                "testmonial_bg",
                "rera_number",
                "footer_text",
                "copy_right",
                "status",
            )
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(
                f'<img src="{obj.logo.url}" width="100" style="border-radius:8px;">'
            )
        return "No Logo"

    logo_preview.short_description = "Logo Preview"

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "subtitle")
    list_filter = ("is_active",)
    ordering = ("order",)

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("type","name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",) 

@admin.register(About_Us)
class About_UsAdmin(admin.ModelAdmin):
    list_display = ("Title","Subtitle", "Description")

    
    fieldsets = (

        ("Hero Section", {
            "fields": (
                "Hero_Title",
                "Hero_Subtitle",
                "Hero_Image",
            )
        }),

        ("About Section", {
            "fields": (
                "Title",
                "Subtitle",
                "Description",
            )
        }),

        ("Mission And Vision Section", {
            "fields": (
                "Mission_Title",
                "Mission_Description",
                "Vision_Title",
                "Vision_Description",
            )
        }),
    )


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "designation",
        "display_order",
        "is_active",
    )
    list_editable = ("display_order", "is_active")
    search_fields = ("name", "designation")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("👤 Profile", {
            "fields": ("name", "designation", "image", "bio")
        }),
        ("🔗 Links", {
            "fields": ("linkedin_url", "email")
        }),
        ("⚙️ Settings", {
            "fields": (
                "display_order",
                "is_active",
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(Why_Choose)
class WhyChooseAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)

@admin.register(Awards_Recognition)
class Awards_RecognitionAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)


@admin.register(Contact_Page)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("heading", "phone", "email")
    search_fields = ("heading", "phone", "email")

@admin.register(Our_Team)
class OurTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "designation")
    search_fields = ("name", "designation")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "rating")
    list_filter = ("rating",)
    search_fields = ("name", "designation", "message")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)
    search_fields = ("question", "answer")


@admin.register(ImpactMetric)
class ImpactMetricAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "order", "created_on")
    list_editable = ("order",)
    ordering = ("order",)
    search_fields = ("title", "value")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")


    list_display = (
        "title",
        "order",
        "is_active",
    )

    list_filter = ("is_active",)
    search_fields = ("title", "subtitle", "link")

    ordering = ("order",)

    list_editable = ("order", "is_active")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "subtitle", "link")
        }),
        ("Hierarchy", {
            "fields": ("parent",)
        }),
        ("Settings", {
            "fields": ("order", "is_active")
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("parent")    

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")
    ordering = ("parent", "order")

@admin.register(Our_Industry)
class Our_IndustryAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)

@admin.register(Our_Clients)
class Our_ClientsAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)