import json
from django.shortcuts import render, render_to_response
from django.core.context_processors import request
from django.http.response import HttpResponse
from django.template.context import RequestContext
from engine import Engine

def homepage(request):

    return render_to_response('homepage.html', RequestContext(request))


def get_available_moves_for_pawn(request):
    data = json.loads(request.POST.get('data', False))
    # assuming that program displays av moves only for player
    if data['turn'] == 'white':
        turn = True
    elif data['turn'] == 'black':
        turn = False
    else:
        return HttpResponse('Wrong data passed')

    eng = Engine(data['state'], turn)
    available_moves = eng.get_available_moves_for_pawn(data['pawn_cords'])

    return HttpResponse(json.dumps(available_moves));

def make_move(request):
    '''
    Function will get from POST json representation of 
    chess board. 
    
    Make few steps:
    Valid if last user move is correct.
    If not valid:
        return info
    TODO: also check if user didn't modify DOM / hacks
    Call minmax algorithm and return computer move.
    
    '''
