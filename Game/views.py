from django.shortcuts import render, redirect, HttpResponse
from Game.models import Game
from Profile.models import Profile
from urlparams.redirect import param_redirect
from django.contrib import messages
from django.utils import timezone
from Question.models import Question
import random
import json
from django.utils import timezone
from datetime import timedelta

from Game.main import Bingo 

# Create your views here.
def game_home(request, username):
    data = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(User=request.user)
        data['profile'] = profile
    
    try:
        game = Game.objects.get(Player=profile)
        return param_redirect(request, 'main', username)
    except Exception as e:
        print(e)
        print('new game required!!')
    return render(request, 'game.html', data)

def save(request, username):
    try:
        if request.user.is_authenticated == False:
            return redirect('home')
        data = {}
        if request.method == "POST":
            profile =  Profile.objects.get(User=request.user)
            
            matrix = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
            ct = 0
            i = 0
            j = 0
            l = []
            while ct!=25:
                num = eval(request.POST[str(ct+1)])
                if num > 0 and num <= 25: 
                    if num not in l:
                        matrix[i][j] = num
                        l.append(num)
                        j += 1
                        if j == 5:
                            i += 1
                            j = 0
                        ct+=1
                    else:
                        messages.error(request, "Refil the form, as one of the number is repeating.")
                        return param_redirect(request, 'g_home', username)
                        break
                else:
                    messages.error(request, "Refil the form, as one of the number is not with in the contstraints.")
                    return param_redirect(request, 'g_home', username)
                    break
            new_game = Game.objects.create(Player=profile, Matrix=matrix)
            questions = Question.objects.all()
            
            ct=0
            for question in questions:
                if ct == 25: break
                new_game.Questions.add(question)
                ct += 1
            
            new_game.save()
            return param_redirect(request, 'main', username)
            
        return param_redirect(request, 'g_home', username)
    except : return redirect('home')

def play(request, username):
    try:
        if request.user.is_authenticated == False:
            return redirect('home')
        data = {}
        if request.user.is_authenticated:
            profile = Profile.objects.get(User=request.user)
            data['profile'] = profile
            try:
                game = Game.objects.get(Player=profile)
            except :
                messages.error(request, "Your game ended.") 
                return redirect('home')
            data['game'] = game
            
            if game.Status == False:
                messages.error(request, "You have already finished that game.")
                return redirect('home')
            
            matrix = eval(game.Matrix)
            ct = 1
            for i in range(5):
                for j in range(5):
                    data["ans_"+str(ct)] = matrix[i][j]
                    ct += 1
                    
            # num = random.randint(0, game.Questions.all().count()-1)
            data['question'] = game.Questions.all()[0]
            
            months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
            
            S = game.Start
            S = S+timedelta(hours=5, minutes=30)
            start = months[S.month]+" "
            start += str(int(S.day))+", "
            start += str(S.year)+" "
            start += S.strftime("%H:%M:%S")
            
            data['start'] = start
            
        return render(request, 'main.html', data)
    except : return redirect('home')

def update(request, username):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                number = eval(request.POST['input'])
                q_id = request.POST['question']
                
                question = Question.objects.get(Id=q_id)
                profile = Profile.objects.get(User=request.user)
                game = Game.objects.get(Player=profile)
                
                if number == eval(question.Answer):
                    data = {}
                    data['matrix'] = eval(game.Matrix)
                    data['completed'] = None
                    if game.Completed == "": data['completed'] = set()
                    else: data['completed'] = eval(game.Completed)
                    data['current'] = game.Current
                    data['input'] = number
                    
                    b = Bingo(data)
                    res = b.get_data()
                    if res['found']:
                        game.Matrix = res['matrix']
                        game.Current = res['current']
                        if len(res['completed']) != len(data['completed']):
                            game.Completed = res['completed']
                        
                        if game.Current == "":
                            messages.success(request, "You have successfully completed the task.")
                            game.End = timezone.now()
                            #update status
                            game.Status = False
                            game.save()
                            return redirect('home')
                        game.Questions.remove(question)
                        game.save()
                    else:
                        messages.error(request, "Wrong Input")
                else:
                    game.Penalty+=1
                    game.save()
                    messages.error(request, "Wrong Answer")
                
                return param_redirect(request, 'main', username)
                
        else : return redirect('home')
    except Exception as e:
        return redirect('home')