from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from db import dbconn
from random import randint

# Create your views here.

@api_view(['POST'])
def sign_up(request):
    
 try:
    
    
    userdata = json.loads(request.body)
    emailexist = dbconn.clnadmin.find_one({'email': userdata['email']})
    if not emailexist:
            if userdata['employ_type'] == 'admin':
                randnumber = randint(1111,9999)
                password = 'admin-'+str(randnumber)+'-'+userdata['phone'][6:10]
                print(password)
                new_admin = {
                            "firstname": userdata['firstname'],
                            "lastname": userdata['lastname'],
                            "age": userdata['age'],
                            "gender": userdata['gender'],
                            "email": userdata['email'],
                            "phone": userdata['phone'],
                            "password":password
                            
                            }
                dbconn.clnadmin.insert_one(new_admin)
                
            elif userdata['employ_type'] == 'user':
                randnumber = randint(1111,9999)
                password = 'user-'+str(randnumber)+'-'+userdata['phone'][6:10]
                print(password)
                new_user = {
                            "firstname": userdata['firstname'],
                            "lastname": userdata['lastname'],
                            "age": userdata['age'],
                            "gender": userdata['gender'],
                            "email": userdata['email'],
                            "phone": userdata['phone'],
                            "password":password
                            }
                
                dbconn.clnuser.insert_one(new_user)
            else:
                return JsonResponse({'statuscode': 400, 'message': 'Invalid user type'})
    
            return JsonResponse({'statuscode':200, 'message': 'User created successfully'})
    else:
         return JsonResponse({'statuscode':400, 'message': 'email already exist'})

 except Exception as e:
        print(e)

        return JsonResponse({'statuscode':400, 'message': 'Error creating user'})


@api_view(['POST'])
def email_check(request):
    formdata = request.data
    print(formdata)
    email = formdata['email']
    user_obj = dbconn.clnuser.find_one({'email': email})
    admin_obj = dbconn.clnadmin.find_one({'email': email})

    if user_obj or admin_obj:
        return JsonResponse(True,safe=False)
    else:
        return JsonResponse(False,safe=False)

@api_view(['POST'])
def admin_login(request):
    formdata = request.data
    email = formdata['email']
    password = formdata['password']

    admin_obj = dbconn.clnadmin.find_one({'email': email ,'password':password})

    if admin_obj:
        name = admin_obj['firstname']+" "+admin_obj['lastname']
        user_id = str(admin_obj['_id'])
        
        return JsonResponse({'statuscode':200,'name':name,'user_id':user_id})
    else:
        return JsonResponse({'statuscode':400})

@api_view(['POST'])
def user_login(request):
    formdata = request.data
    email = formdata['email']
    password = formdata['password']

    user_obj = dbconn.clnuser.find_one({'email': email ,'password':password})

    if user_obj:
        name = user_obj['firstname']+" "+user_obj['lastname']
        user_id = str(user_obj['_id'])
        
        return JsonResponse({'statuscode':200,'name':name,'user_id':user_id})
    else:
        return JsonResponse({'statuscode':400})