from drf_yasg import openapi

api_info = openapi.Info(
    title="Artists API",
    default_version="v1",
    description="Artists API basic endpoints",
    terms_of_service="https://www.example.com/terms/",
    contact=openapi.Contact(email="contact@example.com"),
    license=openapi.License(name="License"),
)
