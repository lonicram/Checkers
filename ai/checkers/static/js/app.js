var checkers = (function(){
    "use strict";
    var self = {};
    self.turn = '';
    
    var make_move = function(){
        
    };
    var show_av_moves = function(pawn){
        self.turn = ($(this).hasClass('white')) ? 'white' : 'black';
        pawn.addClass('active');
        var row = pawn.parents('tr').index();
        var col = pawn.index();
        
    };
    var gui = function(){
        var pawns = $('#board .pawn');
        pawns.on('click tap', function(){
            pawns.removeClass('active');
            show_av_moves($(this));
            
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