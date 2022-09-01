
from django.shortcuts import redirect, render
from hostel.models import Register
from room.models import Room
from .models import SelectMatch,Match

# Create your views here.


def isMatched(request):
    curr_user = SelectMatch.objects.filter(sic__user=request.user).values()
    for curr in curr_user:
        if(curr['status1'] and curr['status2'] ):
            room1 = SelectMatch.objects.filter(later=curr["later"]).get(sic__user=request.user).sic.sic.sic
            room2 = curr['later']
            if Match.objects.filter(roomate1=room1).exists():
                
                print("alredey booked")
            else:
                match = Match.objects.create(
                roomate1= room1,
                roomate2= room2,
                room_no = Room.objects.get(room_no=0)
                )   
                match.save()
                print("saved")
                
            return True
    return False
           
    
def matcher(request):
    # curr_user = SelectMatch.objects.filter(sic__user=request.user).values()
    # for curr in curr_user:
    #     if(curr['status1'] and curr['status2'] ):
    #         return redirect('roomselect')
    if isMatched(request):
        return redirect('roomselect')

    stu = Register.objects.all()
    curr = Register.objects.get(user = request.user).sic
    stulist=[]
    
    for student in stu:
        print(student.sic,curr,curr!=student.sic)
        if student.sic != curr:
            students ={
                "first_name" : student.sic.first_name,
                "last_name" : student.sic.last_name,
                "branch" : student.sic.branch+"E",
                "home" : student.sic.home,
                "hobby":student.hobby,
                "desc":student.desc,
                "sic":student.sic
            }
            stulist.append(students)
    context={
       "students":stulist
   }

    return render(request,'matcher/display.html',context)

def wishlist(request):
    # curr_user = SelectMatch.objects.filter(sic__user=request.user).values()
    # for curr in curr_user:
    #     if(curr['status1'] and curr['status2'] ):
    #         return redirect('roomselect')
    if isMatched(request):
        return redirect('roomselect')
    later = SelectMatch.objects.filter(sic__user=request.user).values()
    later_list=[]
    
    for i in later:
        student = Register.objects.get(sic =i['later'])
        students ={
                "first_name" : student.sic.first_name,
                "last_name" : student.sic.last_name,
                "branch" : student.sic.branch+"E",
                "home" : student.sic.home,
                "hobby":student.hobby,
                "desc":student.desc,
                "sic":student.sic.sic
            }
        
        if(students not  in later_list):
            later_list.append(students)


    sic_curr = Register.objects.get(user = request.user).sic.sic
    match_curr = SelectMatch.objects.filter(later = sic_curr).values()

    match_list=[]
    for match in match_curr:
        later_id = match['id']
        sic_later = SelectMatch.objects.get(id=later_id).sic
        match_later = SelectMatch.objects.filter(later = sic_later.sic.sic).values()
        
        for ml in match_later:
           
            ml_id = ml['id']
            sic_next = SelectMatch.objects.get(id=ml_id).sic
            if(sic_next.sic.sic == sic_curr):
                students1 ={
                "first_name" : sic_later.sic.first_name,
                "last_name" : sic_later.sic.last_name,
                "branch" : sic_later.sic.branch+"E",
                "home" : sic_later.sic.home,
                "hobby":sic_later.hobby,
                "desc":sic_later.desc,
                "sic":sic_later.sic.sic,
                "status":ml['status1']
            }
                if(students1 not  in match_list):
                    match_list.append(students1) 
    
    context={
       "students":later_list,
       "matches": match_list
   }

    return render(request,"matcher/wishlist.html",context)

def add(request,id):
 
    
    curr = Register.objects.get(user= request.user)
    # print(curr.sic.sic)
    if(SelectMatch.objects.filter(later=id).exists() or Match.objects.filter(roomate1=id).exists() or Match.objects.filter(roomate2=id).exists()):
        return redirect('matcher')
    try:
        sm= SelectMatch.objects.create(
            sic = curr,
            later = id
        )
        sm.save()
        print("done")
        return redirect('matcher')
    except Exception as e:
        print("f")


    return redirect('matcher')

def remove(request,id):
    try:
        SelectMatch.objects.filter(sic__user=request.user).get(later=id).delete()
        return redirect('wishlist')
    
    except Exception as e:
        print(e)
    
        return redirect('wishlist')

def matched(request):

    sic_curr = Register.objects.get(user = request.user).sic.sic
    match_curr = SelectMatch.objects.filter(later = sic_curr).values()

    match_list=[]
    for match in match_curr:
        later_id = match['id']
        sic_later = SelectMatch.objects.get(id=later_id).sic
        
        match_later = SelectMatch.objects.filter(later = sic_later.sic.sic).values()
        for ml in match_later:
            ml_id = ml['id']
            sic_next = SelectMatch.objects.get(id=ml_id).sic
            if(sic_next.sic.sic == sic_curr):
                students ={
                "first_name" : sic_later.sic.first_name,
                "last_name" : sic_later.sic.last_name,
                "branch" : sic_later.sic.branch+"E",
                "home" : sic_later.sic.home,
                "hobby":sic_later.hobby,
                "desc":sic_later.desc,
                "sic":sic_later.sic.sic 
            }
            if(students not  in match_list):
                match_list.append(students)
    
    
    context={
       "students":match_list
   }


    

    return render(request,'matcher/matched.html',context)

def confirm(request,id):
    curr_user = SelectMatch.objects.filter(sic__user=request.user).values()
 
    if isMatched(request):
        return redirect('roomselect')

    confirm_user = SelectMatch.objects.filter(later=id).get(sic__user=request.user)
    confirm_mate = SelectMatch.objects.filter(later=confirm_user.sic.sic.sic).get(sic__sic__sic=confirm_user.later)
    print(confirm_user,confirm_mate)
    try:
        confirm_user.status1 = True
        confirm_user.save()

        confirm_mate.status2=True
        confirm_mate.save()

        print("saved both satus")
      
    except Exception as e:
        print(e)

    return redirect('wishlist')


