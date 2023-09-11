from django.http import JsonResponse
import json
from products.models import Product
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
@swagger_auto_schema(
    method='post',
)
def api_home(request, *arg  , **kwargs):
    model_data = Product.objects.all().order_by("price").first()
    data = {}
    if model_data :
        data['title']= model_data.title
        data['content'] = model_data.content
        data['price']= model_data.price
    return JsonResponse(data)
