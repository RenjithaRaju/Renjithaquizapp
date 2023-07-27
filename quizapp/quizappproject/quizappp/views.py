from xml.dom import UserDataHandler
from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from . models import user_register,questions,Quizresult
import datetime
import easygui
from django.contrib.auth import logout as log
import pandas as pd


# Create your views here.
def home(request):
    return render(request,'login.html')

def logout(request):
    log(request)
    return render(request,'login.html')


def login(request):
      if request.method=="POST":
          username=request.POST['username']
          email=request.POST['email']
          user=user_register.objects.filter(username=username,email=email,std_type="Student")
          admin=user_register.objects.filter(username=username,email=email,std_type="admin")
          if user:
              for x in user:
                 request.session['id']=x.id
                 request.session['username']=x.username
                 request.session['email']=x.email
                 request.session['std_type']=x.std_type
                 return HttpResponseRedirect("/quizdash/")
          elif admin:
              for x in admin:
                  request.session['id']=x.id
                  request.session['username']=x.username
                  request.session['email']=x.email
                  request.session['std_type']=x.std_type
                  return HttpResponseRedirect("/admindash/")
          else:
              return render(request,'login.html',{'msg':'Invalid login credential'})
                  
      return render(request,'login.html')
     

def register(request):
    x=datetime.datetime.now()
    time=x.strftime("%X %p")
    if request.method=="POST":
        if user_register.objects.filter(email=request.POST['email']):
            return render(request,'register.html',{'msg':'This email id is already registered wih us'})
        else:
            user_dis=user_register()
            user_dis.email=request.POST['email']
            user_dis.username=request.POST['username']
            user_dis.phone=request.POST['phone']
            user_dis.course=request.POST['course']
            user_dis.std_type="Student"
            user_dis.logintime=time
            user_dis.save() 
            return redirect(login)      
    return render(request,'register.html')


def quizdash(request): 
    SessionId=request.session['id']
    user_display=user_register.objects.all().filter(id=SessionId)
    var=questions.objects.all()
    return render(request,'questions.html',{'var':var,'user_display':user_display})

def admindash(request):
    if request.method=="POST":
      quiz=questions()
      quiz.question=request.POST['question']
      quiz.opt1=request.POST['opt1']
      quiz.opt2=request.POST['opt2']
      quiz.opt3=request.POST['opt3']
      quiz.opt4=request.POST['opt4']
      quiz.ans=request.POST['ans']
      quiz.save()
      easygui.msgbox("succesfully added")
      return redirect(admindash)
    return render(request,'addquestion.html')


def result(request):
    if request.method=="POST":
        SessionId=request.session['id']
        sid=user_register.objects.get(id=SessionId)
        quiz=questions.objects.all()
        quiz_score=0
        quiz_wrong=0
        quiz_cottect=0
        x=datetime.datetime.now()
        time=x.strftime("%X %p")
        date=x.strftime("%Y-%m-%d")
        score=Quizresult()
        for q in quiz:
            score.quiz_total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            if q.ans == request.POST.get(q.question):
                score.quiz_score+=10
                score.quiz_cottect+=1
                score.quiz_percent=score.quiz_score/(score.quiz_total*10)*100
                score.quiz_id=sid
                score.quiz_date=date
                score.quiz_time=time
                score.save()     
            else:
                 score.quiz_wrong+=1
        return redirect(logout)
    
def resultview(request):
    dataview=Quizresult.objects.all()
    return render(request,'resultview.html',{'dataview':dataview})

def downloadcsv(request):
    data=user_register.objects.all().filter(std_type='Student').values("username","email","phone","course","logintime")
    df1=pd.DataFrame(list(data),index=None)
    data2=Quizresult.objects.all().values("quiz_score","quiz_percent","quiz_cottect","quiz_total","quiz_wrong","quiz_date","quiz_time")
    df2=pd.DataFrame(list(data2),index=None)
    data_frame=pd.concat([df1,df2],axis=1,ignore_index=True)
    csv=data_frame.to_csv(header=["Student Name","Student Mail","Phone Number","Course","Student LoginTime","Score","Percentage","Corrected","Total","Wrong","Date","Time"],index=True)
    response=HttpResponse(csv,content_type="text/csv")
    response['Content-Disposition']='attachment:filename=quiz result.csv'
    return response
