from django.urls import path
from .views import (
    DashboardStatsView,
    ClienteListCreateView, ClienteDetailView,
    ProveedorListCreateView, ProveedorDetailView,
    CategoriaListCreateView,
    ProductoListCreateView, ProductoDetailView,
    VentaListCreateView, VentaDetailView,
    CompraListCreateView, CompraDetailView
)

urlpatterns = [
    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    
    # Clientes
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
    
    # Proveedores
    path('proveedores/', ProveedorListCreateView.as_view(), name='proveedor-list-create'),
    path('proveedores/<int:pk>/', ProveedorDetailView.as_view(), name='proveedor-detail'),
    
    # Categorías
    path('categorias/', CategoriaListCreateView.as_view(), name='categoria-list-create'),
    
    # Productos
    path('productos/', ProductoListCreateView.as_view(), name='producto-list-create'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detail'),
    
    # Ventas
    path('ventas/', VentaListCreateView.as_view(), name='venta-list-create'),
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta-detail'),
    
    # Compras
    path('compras/', CompraListCreateView.as_view(), name='compra-list-create'),
    path('compras/<int:pk>/', CompraDetailView.as_view(), name='compra-detail'),
]

