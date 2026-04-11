from pyexpat.errors import messages
from django.contrib import messages 
from django.db.models import Min, Max, Q
from django.db.models import Count, Q
from django.http import HttpResponse 
from django.shortcuts import render, redirect, get_object_or_404
from properties.models import Property 
from utility.models import Locality,PropertyType,City,Bank,ProjectAmenities
from blog.models import Blog, Category
import json
from projects.models import Project
from core.models import PocketCategory, PocketItem
from rent.models import RentalProperty
from .models import (
    Setting, Slider, Testimonial, Leadership,
    Contact_Page, FAQ, Our_Team,Why_Choose,ImpactMetric,
    Service, FooterLink,ContactEnquiry,Our_Industry,Our_Clients, About_Us
)

from user.models import Developer 
    


def index(request):

    pocket_categories = PocketCategory.objects.all().prefetch_related('pocketitem_set')

    pocket_data = {}

    for cat in pocket_categories:
        item = cat.pocketitem_set.first()

        if item:
            pocket_data[cat.slug] = {
                "title": item.title,
                "desc": item.description,
                "image": item.image.url if item.image else ""
            }

    settings_obj = Setting.objects.first()
    cities = City.objects.filter(level_type="CITY").order_by("name")
    residential_type = PropertyType.objects.filter(name__iexact="Residential", is_top_level=True).first()
    commercial_type = PropertyType.objects.filter(name__iexact="Commercial", is_top_level=True).first()
    residential_types = residential_type.get_descendants(include_self=True) if residential_type else PropertyType.objects.none()
    commercial_types = commercial_type.get_descendants(include_self=True) if commercial_type else PropertyType.objects.none()
    new_launch_residential = Project.objects.filter(active=True,construction_status__iexact="New Launch",propert_type__in=residential_types).order_by("-create_at")[:10]
    new_launch_commercial = Project.objects.filter(active=True,construction_status__iexact="New Launch",propert_type__in=commercial_types).order_by("-create_at")[:10]
    project_featured = (
        Project.objects.filter(active=True, featured_property=True)
        .annotate(
            min_price=Min("configurations__price_in_rupees", filter=Q(configurations__price_in_rupees__gt=0)),
            max_price=Max("configurations__price_in_rupees", filter=Q(configurations__price_in_rupees__gt=0)),
        )
        .order_by("-create_at")[:6]
    )
    possession_counts = Project.objects.filter(active=True).aggregate(
        ready_to_move=Count("id", filter=Q(construction_status__iexact="Ready To Move")),
        under_construction=Count("id", filter=Q(construction_status__iexact="Under Construction")),
        new_launch=Count("id", filter=Q(construction_status__iexact="New Launch")),
    )
    featured_developers = (Developer.objects.filter(featured_builder=True).annotate(project_count=Count("project", distinct=True)).filter(project_count__gt=0).order_by("-create_at"))
    featured_locality = (Locality.objects.filter(featured_locality=True, project__active=True).annotate(project_count=Count("project", distinct=True)).order_by("-project_count", "name")[:20])
    bank = Bank.objects.filter(home_loan_partner=True).order_by("title")
    blogs = Blog.objects.filter(is_published=True).order_by("-published_date", "-created_at")[:3]
    about_page = About_Us.objects.filter(is_active=True).first()
    impact_metrics = ImpactMetric.objects.all()
    amenities = ProjectAmenities.objects.all()
    footerlink = FooterLink.objects.filter( is_active=True, parent__isnull=True).prefetch_related("children").order_by("order")
    why_choose_items = Why_Choose.objects.filter(is_active=True).order_by("order")[:6]
    our_industry = Our_Industry.objects.filter(is_active=True).order_by("order")
    our_clients = Our_Clients.objects.filter(is_active=True).order_by("order")
    testimonials = Testimonial.objects.all().order_by("-id")
    pocket_categories = PocketCategory.objects.all().prefetch_related('pocketitem_set')
    pocket_data = {}

    for cat in pocket_categories:
        item = cat.pocketitem_set.first()

        if item:
            pocket_data[cat.slug] = {
                "title": item.title,
                "desc": item.description,
                "image": item.image.url if item.image else ""
            }

    faqs = FAQ.objects.all().order_by("id")
    current_city = project_featured.first().city.name if project_featured.exists() else "Mumbai"
    rental_properties = (
        RentalProperty.objects
        .select_related("city", "locality", "tenant_type", "furnishing_type")
        .filter(active=True)
        .order_by("-id")[:10]
    )
    return render(request, "home/index.html", {
        "settings_obj": settings_obj,
        "cities": cities,
        "current_city": current_city,
        "project_featured": project_featured,
        "new_launch_residential": new_launch_residential,
        "new_launch_commercial": new_launch_commercial,
        "featured_developers": featured_developers,
        "featured_locality": featured_locality,
        "bank": bank,
        "blogs": blogs,
        "pocket_categories": pocket_categories,
        "pocket_data_json": json.dumps(pocket_data),
        "our_clients": our_clients,
        "about_page": about_page,
        "impact_metrics": impact_metrics,
        "amenities": amenities,
        "why_choose_items": why_choose_items,
        "footerlink": footerlink,
        "testimonials": testimonials,
        "our_industry": our_industry,
        "faqs": faqs,
        "possession_counts": possession_counts,
        "rental_properties": rental_properties,
    })

def robots_txt(request):
    """
    Serves the robots.txt file content for SEO.
    """
    robots_content = """
User-agent: *
Disallow: /admin/
Disallow: /accounts/
Allow: /

Sitemap: http://127.0.0.1:8000/sitemap.xml 
    """
    return HttpResponse(robots_content.strip(), content_type="text/plain")

def about_page_view(request):
    settings_obj = Setting.objects.filter(status="True").first()
    about_page = About_Us.objects.filter(is_active=True).order_by('-created_at').first()
    leaders = Leadership.objects.filter(is_active=True).order_by('display_order')
   
    context = {
        "about_page": about_page,
        "leaders": leaders,
        "settings_obj": settings_obj,
    }
    return render(request, "home/about.html", context)

def contact_view(request):
    settings_obj = Setting.objects.first()
    contact_content = Contact_Page.objects.first()

    if request.method == "POST":

        enquiry_type = request.POST.get("type")  # <-- Important

        ContactEnquiry.objects.create(
            type=enquiry_type if enquiry_type else None,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message"),
        )

        return redirect("thank_you")   # ✅ redirect to thank you page

    context = {
        "settings_obj": settings_obj,
        "contact_content": contact_content,
    }

    return render(request, "home/contact.html", context)


def faq_view(request):
    """Renders the FAQ page."""
    settings_obj = Setting.objects.first()

    faqs = FAQ.objects.all().order_by('id')

    context = {
        "settings_obj": settings_obj,
        "faqs": faqs,
    }
    return render(request, 'home/faq.html', context)

#-----------------------------------------------------------------------------------------------

def get_setting():

    settings_obj = Setting.objects.filter(status="True").first()    

    return Setting.objects.first()

def privacy_policy(request):

    
    settings_obj = Setting.objects.filter(status="True").first()    
    context = {
        "settings_obj": settings_obj,
    }

    return render(request, 'terms/privacy_policy.html', context)

def terms_conditions(request):
    settings_obj = Setting.objects.filter(status="True").first()   

    context = {
        "settings_obj": settings_obj,
    }
    return render(request, 'terms/terms_conditions.html', context)

def disclaimer(request):
    settings_obj = Setting.objects.filter(status="True").first()    

    context = {
        "settings_obj": settings_obj,
    }
    return render(request, 'terms/disclaimer.html', context)

def cookies(request):
    settings_obj = Setting.objects.filter(status="True").first()    

    context = {
        "settings_obj": settings_obj,
    }
    return render(request, 'terms/cookies-policy.html', context)

def services(request):
    settings_obj = Setting.objects.filter(status="True").first()    
    services = Service.objects.filter(is_active=True)

    context = {
        "settings_obj": settings_obj,
        "services": services,
    }
    return render(request, 'services/services.html', context)

def calculator(request):
    settings_obj = Setting.objects.filter(status="True").first()    
    

    context = {
        "settings_obj": settings_obj,
        
    }
    return render(request, 'home/calculator.html', context)

def thank_you(request):
    if not request.META.get("HTTP_REFERER"):
        return redirect("contact")
    return render(request, "home/thank_you.html")

def investment_properties(request):
    settings_obj = Setting.objects.filter(status="True").first()

    if not settings_obj:
        settings_obj = None
    
    context = {
        "settings_obj": settings_obj,
        
    }
    return render(request, 'investment/investment-properties.html', context)

def investment_properties(request):
    settings_obj = Setting.objects.filter(status="True").first()

    if not settings_obj:
        settings_obj = None
    
    context = {
        "settings_obj": settings_obj,
        
    }
    return render(request, 'investment/investment-properties.html', context)

def landlords(request):
    settings_obj = Setting.objects.filter(status="True").first()

    if not settings_obj:
        settings_obj = None
    
    context = {
        "settings_obj": settings_obj,
        
    }
    return render(request, 'landlords/landlords.html', context)

def resources(request):
    settings_obj = Setting.objects.filter(status="True").first()

    if not settings_obj:
        settings_obj = None
    
    context = {
        "settings_obj": settings_obj,
        
    }
    return render(request, 'resources/resources.html', context)

