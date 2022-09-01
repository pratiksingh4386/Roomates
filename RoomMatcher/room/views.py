
from django.shortcuts import redirect, render

from matcher.models import SelectMatch,Match
from hostel.models import Register,Hostelite
from .models import Room
# Create your views here.

def roomselect(request):
    user = Register.objects.get(user = request.user).sic.sic
    roomate = Match.objects.get(roomate1=user)
    if roomate.room_no.room_no == 0:    
        rooms = Room.objects.all().values()
        room_list=[]
        for room in rooms:
            
            room_no = room['room_no']
            status = "Available" if room['is_available'] else "Not Availale"

            try:
                student1 = Match.objects.get(room_no=room_no).student1
                student2 = Match.objects.get(room_no=room_no).student2

                room_dict = {
                "room_no":room_no,
                "is_available": status,
                "student1": student1,
                "student2": student2
            }
            except Exception:
                room_dict = {
                "room_no":room_no,
                "is_available": status,
            }
            room_list.append(room_dict)
        context={
            "rooms" : room_list
        }


        return render(request,'room/roomselect.html',context)

    else:
        return redirect('showroomate')

def roomconfirm(request,id):
    user = Register.objects.get(user = request.user).sic.sic
    roomate = Match.objects.get(roomate1=user)
    room_no = Room.objects.get(room_no = id)
   
    room_no.is_available = False
    roomate.room_no = room_no 
    
    room_no.save()
    roomate.save()

    return redirect('showroomate')

def showroomate(request):
    student = Register.objects.get(user = request.user)
    roomate = Match.objects.get(roomate1=student.sic.sic)

    roomate1 = roomate.roomate1
    roomate2 = roomate.roomate2
    student2 = Register.objects.get(sic__sic = roomate2)
    room_no = roomate.room_no.room_no
    stulist=[]
    students ={
                "first_name" : student.sic.first_name,
                "last_name" : student.sic.last_name,
                "branch" : student.sic.branch+"E",
                "home" : student.sic.home,
                "hobby":student.hobby,
                "desc":student.desc,
                "sic":student.sic,
                "room":room_no
            }
    stulist.append(students)
    students ={
                "first_name" : student2.sic.first_name,
                "last_name" : student2.sic.last_name,
                "branch" : student2.sic.branch+"E",
                "home" : student2.sic.home,
                "hobby":student2.hobby,
                "desc":student2.desc,
                "sic":student2.sic
            }
    stulist.append(students)

    print(stulist)
    context = {
        "students":stulist
    }
    return render(request,'room/showroomate.html',context)
