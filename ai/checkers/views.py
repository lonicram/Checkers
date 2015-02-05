import json
from django.shortcuts import render, render_to_response
from django.core.context_processors import request
from django.http.response import HttpResponse
from django.template.context import RequestContext


def homepage(request):

    return render_to_response('homepage.html', RequestContext(request))


def get_available_moves_for_pawn(request):
    data = request.POST.get('data', False)
    data = json.loads(data)

    state = data['state']
    pawn_cords = data['pawn_cords']



    return HttpResponse("ok");

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
