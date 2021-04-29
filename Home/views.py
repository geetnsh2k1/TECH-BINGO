from django.shortcuts import render, redirect
from Profile.models import Profile
from Game.models import Game
import json

# Create your views here.
def home(request):
    try:
        data = {}
        data['display'] = "login to play"
        if request.user.is_authenticated:
            profile = Profile.objects.get(User=request.user)
            data['profile'] = profile
            data['display'] = "start game"    
            try:
                game = Game.objects.get(Player=profile)
                if game.Status == False: data['display'] = "game over"
                else : data['display'] = "continue"
            except Exception as e: print(e)     
            
            if request.user.is_superuser:
                games = Game.objects.filter(Current='')
                games = sorted(games, key=lambda game: (game.End-game.Start, game.Player.User.username))
                
                res = ""
                for game in games:
                    res += (game.Player.User.username+"\n")
                data['superuser'] = json.dumps(res)
    except Exception as e: print(e)        
    return render(request, 'home.html', data)   