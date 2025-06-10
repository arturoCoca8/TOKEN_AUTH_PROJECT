from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Cliente, Proveedor, Categoria, Producto, Venta, DetalleVenta, Compra, DetalleCompra
from .serializers import (
    ClienteSerializer, ProveedorSerializer, CategoriaSerializer, 
    ProductoSerializer, VentaSerializer, CompraSerializer
)

# Vistas para Dashboard
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Estadísticas generales
        total_clientes = Cliente.objects.filter(activo=True).count()
        total_productos = Producto.objects.filter(activo=True).count()
        total_proveedores = Proveedor.objects.filter(activo=True).count()
        
        # Ventas del mes actual
        mes_actual = timezone.now().replace(day=1)
        ventas_mes = Venta.objects.filter(
            fecha__gte=mes_actual,
            estado='completada'
        ).aggregate(
            total=Sum('total'),
            cantidad=Count('id')
        )
        
        # Compras del mes actual
        compras_mes = Compra.objects.filter(
            fecha__gte=mes_actual,
            estado='recibida'
        ).aggregate(
            total=Sum('total'),
            cantidad=Count('id')
        )
        
        # Productos con stock bajo (menos de 10)
        productos_stock_bajo = Producto.objects.filter(
            stock__lt=10,
            activo=True
        ).count()
        
        return Response({
            'total_clientes': total_clientes,
            'total_productos': total_productos,
            'total_proveedores': total_proveedores,
            'ventas_mes': {
                'total': ventas_mes['total'] or 0,
                'cantidad': ventas_mes['cantidad'] or 0
            },
            'compras_mes': {
                'total': compras_mes['total'] or 0,
                'cantidad': compras_mes['cantidad'] or 0
            },
            'productos_stock_bajo': productos_stock_bajo
        })

# Vistas para Clientes
class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.filter(activo=True)
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

# Vistas para Proveedores
class ProveedorListCreateView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.filter(activo=True)
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class ProveedorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

# Vistas para Categorías
class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

# Vistas para Productos
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

# Vistas para Ventas
class VentaListCreateView(generics.ListCreateAPIView):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class VentaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

# Vistas para Compras
class CompraListCreateView(generics.ListCreateAPIView):
    queryset = Compra.objects.all().order_by('-fecha')
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class CompraDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]

