$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
var checkers = (function(){
    "use strict";
    var self = {};
    self.turn = '';
    self.board = $("#board");
    
    var get_state = function(){
        var game_state = [];
        var tr = self.board.find("tr");
        tr.each(function(key, value){
            var row = []; 
            var td = $(value).children('td');
            td.each(function(key, obj){
                if($(obj).hasClass('white')){
                    row.push('white');
                }else if($(obj).hasClass('black')){
                    row.push('black');
                }else{
                    row.push(null);
                }
            });
            game_state.push(row);
        });
        console.log(game_state);
        return game_state;
    };
    
    var request = function(url, data, handlers){
        var data = (data)? data : '';
        var success = (handlers.success)? handlers.success : '';
        var error = (handlers.error)? handlers.error : '';
        
        $.ajax({
            url: url,
            dataType:'json',
            type: 'POST', 
            data : {
                'data': JSON.stringify(data)
            }
        }).done(function(data){
            if(success){
                success(data);
            };
        }).fail(function(data){
            if(error){
                error(data);
            }
        });
    };
    
    var make_move = function(){
        
    };
    
    var show_av_moves = function(pawn){
        self.turn = ($(pawn).hasClass('white')) ? 'white' : 'black';
        self.board.find('.active').removeClass('active');
        self.board.find('.pos_move').removeClass('pos_move');
        pawn.addClass('active');
        var row = pawn.parents('tr').index();
        var col = pawn.index();
        var handlers = {
                success:function(data){
                    var tr = self.board.find('tr');
                    for(var move in data){
                        var move = data[move];
                        console.log(move);
                        var td = $(tr[move[0]]).find('td');
                        $(td[move[1]]).addClass('pos_move');
                    }
                    console.log(data)
                },
                error: function(data){
                    console.log(data);
                }
        };
        
        var data = {
                'state': get_state(), 
                'pawn_cords': [row, col], 
                'turn': self.turn
        }
        request('/get_available_moves_for_pawn/', data, handlers);
    };
    var gui = function(){
        var board = $('#board');
        board.on('click tap', '.pawn', function(){
            board.find('active').removeClass('active');
            show_av_moves($(this));
        })
        .on('click', '.pos_move', function(){
            var active = $('.pawn.active');
            //make move
            $(this).addClass('pawn')
                .addClass((active.hasClass('white')? 'white' : 'black'));
            //reset
            active.removeClass('active pawn white black');
            board.find('.pos_move').removeClass('pos_move');
        });
    };
    self.init = function(){
        gui();
    };
    return self;
})();

$(document).ready(function(){
    checkers.init();
});