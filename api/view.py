from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from base.models import Item
from .serializers import ItemSerializer 
from django.shortcuts import render,redirect
from rest_framework.parsers import MultiPartParser
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from PIL import Image

@api_view(['GET'])
def getData(request):
    
    items = Item.objects.all()
    serializer = ItemSerializer(items,many=True)
    return Response(serializer.data)



def alreadyregister(request):
    return render(request, 'alreadyRegister.html')





def showAll(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items,many=True)
    items_per_page = 4
    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pagination.html', {'page_obj': page_obj})


@api_view(['POST'])
def checkUser(request):
    print(request.data.get("username_or_email"))
    data = request.data.get("username_or_email")
    if (not Item.objects.filter(Q(username=data) | Q(email=data)).exists()):
        return Response({'msg':'user not exist','error':1})


    user_item = Item.objects.filter(Q(username=data) | Q(email=data)).first()


    return Response({'email':user_item.email,'username':user_item.username})




@api_view(['POST'])
def delete_item(request):
    data = json.loads(request.body)
    item_id_from_body = data.get('id')
    item = Item.objects.get(pk=item_id_from_body)
    item.delete()
    reorder_ids()

    print(item_id_from_body)
    return showAll(request)

def reorder_ids():
    instances = Item.objects.all().order_by('id')
    for index, instance in enumerate(instances, start=1):
        instance.sequential_id = index
        instance.save()

@api_view(['POST'])
def addData(request):
    serializer = ItemSerializer(data=request.data)

    data = request.data

    if Item.objects.filter(username=data.get('username')).exists():
        msg = {"msg":"Username already exist","error":1}
        return Response(msg)

    if Item.objects.filter(email=data.get('email')).exists():
        msg = {"msg":"Email already exist ", "error":1}
        return Response(msg)
    
    if serializer.is_valid():
        serializer.save()
        reorder_ids()

    items = Item.objects.all()
    serializers = ItemSerializer(items,many=True)
    msg = {
        'msg':"user added successfully"
    }
    return Response(msg)



def profilePicture(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    user_item = Item.objects.filter(Q(username=username) | Q(email=email)).first()
    
    context = {'username' :username,'email':email,'profile_image':user_item.profile_image}
    return render(request,"profile.html",context)


def signUp(request):
    return render(request,"makeProfile.html")





@api_view(['POST'])
@parser_classes([MultiPartParser])
def uploadPicture(request):
    if 'profile-picture' in request.FILES:
        profile_picture = request.FILES['profile-picture']
        username = request.data.get('username')
        email = request.data.get('email')
        try:
            image = Image.open(profile_picture)
        except:
            return Response({'msg': 'Invalid image file.','error':1})
        max_size = 5*1024*1024 
        if profile_picture.size > max_size:
            return Response({'msg': 'Image size exceeds the limit (5MB).','error':1})
        user_item, created = Item.objects.get_or_create(username=username, email=email)
        user_item.profile_image = profile_picture
        user_item.save()
        serializer = ItemSerializer(user_item)
    
    return Response({'msg':"profile picture added successfully"})




