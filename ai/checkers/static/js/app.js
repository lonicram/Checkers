$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
        $('.disable').show();
        $('#status').text('computing');
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
     }, 
     complete: function(){
        $('.disable').hide();
        $('#status').text('');
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
                if($(obj).hasClass('pawn_white')){
                    row.push('pawn_white');
                }else if($(obj).hasClass('pawn_black')){
                    row.push('pawn_black');
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
    
    var get_ai_move = function(){
        var handlers = {
            success: function(data){
                console.log(data);
            }, 
            error: function(data) {
                console.log(data);
            }
        };

        var data = {
            'state' : get_state(), 
            'turn': 'pawn_white'
        }

        request('/get_ai_move/', data, handlers);
    };
    
    var update_board = function(start_coord, end_coord, turn) {
        var handlers = {
            success: function(data){
                console.log(data);

                $(data).each(function (key, value) {
                    var row = key;
                    $(value).each(function(key, value){
                        var col = key;
                        var sign = data[row][col];
                        var tr = $(self.board.find('tr')[row])
                        var td = $(tr.find('td')[col]);
                        if (sign == 'beaten'){
                            td.addClass(sign);
                        }
                    })
                });
                setTimeout(function(){
                    $('.beaten').removeClass('pawn_white pawn_black beaten');
                        get_ai_move();
                    },1000);
            }, 
            error: function(data) {
                console.log(data);
            }
        };

        var data = {
            'state' : get_state(), 
            'turn': turn, 
            'start_coord' : start_coord,
            'end_coord' : end_coord
        }

        request('/update_board/', data, handlers);
    }

    var show_av_moves = function(pawn){
        self.turn = ($(pawn).hasClass('pawn_white')) ? 'pawn_white' : 'pawn_black';
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
                        var td = $(tr[move[0]]).find('td');
                        $(td[move[1]]).addClass('pos_move');
                    }
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
        board.on('click tap', '.pawn_white, .pawn_black ', function(){
            board.find('active').removeClass('active');
            show_av_moves($(this));
        })
        .on('click', '.pos_move', function(){
            var active = $('.active');
            var turn = '';
            //make move
            turn = (active.hasClass('pawn_white')? 'pawn_white' : 'pawn_black')
            $(this).addClass(turn);

            //TODO: make function for getting coords
            var start_coord = [];
            var end_coord = [];
            start_coord[0] = $('.active').parents('tr').index();
            start_coord[1] = $('.active').index();
            end_coord[0] = $(this).parents('tr').index();
            end_coord[1] = $(this).index();

            update_board(start_coord, end_coord, turn);

            //reset
            active.removeClass('active pawn_white pawn_black');
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