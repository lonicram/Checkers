import json
from django.shortcuts import render, render_to_response
from django.core.context_processors import request
from django.http.response import HttpResponse
from django.template.context import RequestContext
from engine import Engine

def homepage(request):

    return render_to_response('homepage.html', RequestContext(request))


def initialize_engine(data):
    '''
    Initialize game engine
    @param request - Request
    '''
    # assuming that program displays av moves only for player
    if data['turn'] == 'pawn_white':
        turn = True
    elif data['turn'] == 'pawn_black':
        turn = False
    else:
        return HttpResponse('Wrong data passed')

    return  Engine(data['state'], turn)


def get_available_moves_for_pawn(request):
    data = json.loads(request.POST.get('data', False))
    eng = initialize_engine(data)
    available_moves = eng.get_available_moves_for_pawn(data['pawn_cords'])

    return HttpResponse(json.dumps(available_moves));

def update_board(request):
    '''
    In example, remove pawn which has been beaten
    '''
    data = json.loads(request.POST.get('data', False))
    eng = initialize_engine(data)
    new_board_state = eng.update_board(
        data['start_coord'], data['end_coord']
        )

    return HttpResponse(json.dumps(new_board_state))

def get_ai_move(request):
    '''
    Function will get from POST json representation of 
    chess board. 
    
    Make few steps:
    TODO: also check if user didn't modify DOM / hacks
    Call minmax algorithm and return ai move.
    
    '''
    data = json.loads(request.POST.get('data', False))
    eng = initialize_engine(data)
    return HttpResponse(json.dumps(eng.get_possible_moves()))
