from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from db import dbconn
from bson import ObjectId
from rest_framework.response import Response


# Create your views here.



# -------


@api_view(['POST'])
def leave(request):
    try:
        
        formdata = json.loads(request.body)
        print(formdata)

        userid = formdata['userid']
        userid = ObjectId(userid)
        user = dbconn.clnuser.find_one({'_id': userid})
        
        new_leave = {
            'firstName': formdata['firstName'],
            'lastName': formdata['lastName'],
            'leaveFromDate': formdata['leaveFromDate'],
            'leaveToDate': formdata['leaveToDate'],
            'reasonForLeave': formdata['reasonForLeave'],
            'gender': formdata['gender'],
            'leaveType':formdata['leaveType'],
            'status':'pending',
            'userid': user['_id'] 
            
        }
    
        dbconn.leave.insert_one(new_leave)

        return JsonResponse({'statuscode': 200, 'message': 'Leave created successfully'})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 400, 'message': 'Error creating leave'})





@api_view(['GET'])
def view_leave(request, userid):
    try:
            userid = ObjectId(userid)
            latest_document = dbconn.leave.find_one({'userid':userid}, sort=[('_id',-1)])
            print(type(latest_document))
            latest_document['_id'] = str(latest_document['_id'])
            latest_document['userid'] = str(latest_document['userid'])

            return Response({'statuscode':200,'details':latest_document })
    
    except Exception as e:
        return JsonResponse({'statuscode':400,'details' : print(e)})

@api_view(['POST'])
def edit_leave(request):
    try:
        formdata = json.loads(request.body)
        userid = formdata['userid']
        userid = ObjectId(userid)
        

        latest_document = dbconn.leave.find_one({'userid': userid}, sort=[('_id',-1)])
        
        if not latest_document:
            return JsonResponse({'statuscode': 400, 'message': 'No leave record found for the user'})
        
        # Update latest_document with formdata
        for key in formdata:
            if key in latest_document:
                latest_document[key] = formdata[key]
        latest_document['userid'] = userid
        latest_document['status']='pending'
        
        # Update the document in the collection
        dbconn.leave.update_one({'_id': latest_document['_id']}, {'$set': latest_document})
        
        return JsonResponse({'statuscode': 200,'message':'sucessfully updated leave form'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'statuscode': 400,'message':print(e)})




@api_view(['POST'])
def delete_leave(request):
    try:

        userid = request.data.get('userid')
        userid = ObjectId(userid)

        latest_leave = dbconn.leave.find_one({'userid':userid},sort=[('_id',-1)])

        if latest_leave:
            dbconn.leave.delete_one({'_id': latest_leave['_id']})

            return JsonResponse({'statuscode': 200,'message':'sucessfully deleted'})
        
        else:
        
            return JsonResponse({'statuscode':400,'message':'somthing went wrong'})
    
    except:
            return JsonResponse({'statuscode':400,'message':'somthing went wrong'})
        