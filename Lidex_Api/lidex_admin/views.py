from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from db import dbconn
from bson import ObjectId
from rest_framework.response import Response




# Create your views here.

@api_view(['GET'])
def view_all_leaves(request):
    try:
        all_leaves = list(dbconn.leave.find())

        for leave in all_leaves:
            leave['_id'] = str(leave['_id'])
            leave['userid'] = str(leave['userid'])

        return Response({'statuscode': 200, 'details': all_leaves})
    
    except :
        return Response({'statuscode': 400, 'details':'somthing went wrong'})
    

@api_view(['GET'])
def pending_leave(request):
    try:
        pending_leave = list(dbconn.leave.find({'status':'pending'}))

        for leave in pending_leave:
            leave['_id'] = str(leave['_id'])
            leave['userid'] = str(leave['userid'])

        return Response({'statuscode': 200, 'details': pending_leave})
    
    except :
        return Response({'statuscode': 400, 'details':'somthing went wrong'})

@api_view(['POST'])
def approve_or_reject(request):
    try:

        formdata = request.POST

        ustatus = formdata['ustatus']
        leave_id = formdata['leaveId']
        leave_id = ObjectId(leave_id)
        

        dbconn.leave.update_one({'_id': leave_id}, {'$set': {'status': ustatus}})

        return Response({'statuscode': 200, 'details': "pending_leave"})
    except Exception as e:
        print(e)
        return Response({'statuscode': 400, 'details':'something went wrong'})

from pymongo import MongoClient

@api_view(['GET'])
def admin_dashboard(request):
  
   
    total_users = dbconn.clnuser.count_documents({})
    print(total_users)

    pending_leave = dbconn.leave.count_documents({'status':'pending'})
    approved_leave = dbconn.leave.count_documents({'status':'approved'})
    rejected_leave = dbconn.leave.count_documents({'status':'rejected'})
    
    data = {
        'total_users': total_users,
        'pending_leave': pending_leave,
        'approved_leave': approved_leave,
        'rejected_leave': rejected_leave
    }
    
    
    return JsonResponse({'details':data})
