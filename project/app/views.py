from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .forms import QuestionForm,QuizForm
from .models import Profile,Quiz,Questions,QuizOptions,QuizType,Answer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.
def index(request):
    context={}
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = QuizForm(request.POST)
            if form.is_valid():
                name=form.cleaned_data['name']
                user_app=Profile.objects.get(name=request.user.username)
                form=QuizForm({'name':name,'user_app':user_app})
                form.save()
                return redirect('index')
        else:
            form = QuizForm()

        user_name=request.user.username
        profile = Profile.objects.get(name=user_name)
        quizzes = Quiz.objects.filter(user_app_id=profile.id)
        context={'quizzes':quizzes,'form':form}

    return render(request,"app/index.html",context)
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            messages.success(request,f'User {username} created')
            return redirect('index')           
    else:       
        form = UserCreationForm()
    context = {'form':form}
    return render(request,'app/register.html',context)

#create user then send a signal to save profile
def create_profile(sender,instance,created,**kwards):
    if created:
        Profile.objects.create(name=instance)
post_save.connect(create_profile,sender=User)
#end

def quiz_remove(request,quiz_name):
    if request.method == 'GET':
        id_quiz=Quiz.objects.get(name=quiz_name)
        try:
            Quiz.objects.filter(id=id_quiz.id).delete()   
        except Quiz.DoesNotExist:
            print("error...",Quiz.DoesNotExist)
    
    return redirect('index') 
    
def quiz(request,quiz_name):

    id_quiz=Quiz.objects.get(name=quiz_name) 
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()                      
            sentence=form.cleaned_data['sentence']
            messages.success(request,f'sentence {sentence} created')
            form = QuestionForm()
            #save to questions
            id_sentence = QuizOptions.objects.get(sentence=sentence)
            id_quiz_type=QuizType.objects.get(name='quiz_options')
            Questions.objects.create(number=id_sentence.id, quiz_type=id_quiz_type, quiz=id_quiz)
               
    else:    
        form = QuestionForm()


    try:
        id_questions=Questions.objects.filter(quiz=id_quiz)
        #TODO:if quiz_options check
        questions=[]
        for e in id_questions:
            questions.append(QuizOptions.objects.get(id=e.number))
    except QuizOptions.DoesNotExist:
        print("error...",QuizOptions.DoesNotExist)

    context={'quiz_name':quiz_name,'form':form, 'questions':questions}
    return render(request,'app/quiz.html',context)


def student_quiz(request,profile,quiz_name,token):
    if request.method == 'GET':
        is_token = Quiz.objects.filter(name=quiz_name).filter(token=token).exists()
        if not is_token:
            return HttpResponse("token is invalid")

        id_quiz=Quiz.objects.get(name=quiz_name) 
        try:
            id_questions=Questions.objects.filter(quiz=id_quiz)
            #TODO:if quiz_options check
            questions=[]
            for e in id_questions:
                questions.append(QuizOptions.objects.get(id=e.number))
        except QuizOptions.DoesNotExist:
            print("error...",QuizOptions.DoesNotExist)
        
        context = {'questions':questions,'quiz_name':quiz_name}
        return render(request,'app/student_exam.html',context)

    if request.method == 'POST':
        myDict = request.POST
        Answer.objects.create(student=myDict.dict())
        return HttpResponse("your test has been saved")

def generate_link(request, quiz_name):
    
    if request.user.is_authenticated:
        token_generator=PasswordResetTokenGenerator()
        token = token_generator.make_token(request.user)
        id_quiz=Quiz.objects.get(name=quiz_name)
        setattr(id_quiz, 'token', token)
        id_quiz.save()

    context={'quiz_name':quiz_name,'token':token}
    return render(request,'app/generate_link.html',context)
   