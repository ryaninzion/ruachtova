/* Author:

*/
(function($){})(window.jQuery);
		$(document).ready(function (){

			$(".desc-less").hide();

			$(".desc-more").click(function(){
				$(".desc p").show("fast");
				$(".desc-more").hide();
				$(".desc-less").show();
			});

			$(".desc-less").click(function(){
				$(".desc p").hide();
				$(".desc p:first-child").show();
				$(".desc-more").show();
				$(".desc-less").hide();
			});

			$("#profile_search_form").show();
			$("#event_search_form").hide();
			$("#initiative_search_form").hide();

			$("#search_form_select").change(function(){
				if ($(this).val() == 'profile') {
					$("#profile_search_form").show();
					$("#event_search_form").hide();
					$("#initiative_search_form").hide();
				} else if ($(this).val() == 'event') {
					$("#profile_search_form").hide();
					$("#event_search_form").show();
					$("#initiative_search_form").hide();
				} else if ($(this).val() == 'initiative') {
					$("#profile_search_form").hide();
					$("#event_search_form").hide();
					$("#initiative_search_form").show();
				} else {
					$("#profile_search_form").show();
					$("#event_search_form").hide();
					$("#initiative_search_form").hide();
				}
			});

/*			$("#photo-bar-ul li:first").before($("photo-bar-ul li:last"));

			$("#right-scroll img").click(function(){
				var item_width = $("#photo-bar-ul li").outerWidth() + 10;
				var left_indent = parseInt($("#photo-bar-ul").css("right")) - item_width;

				$("#photo-bar-ul").animate({"right" : left_indent}, {queue:false, duration:500},function(){
					$("#photo-bar-ul li:last").after($("#photo-bar-ul li:first"));
					$("#photo-bar-ul").css({"right" : "-120px"});
				});
			});


			$("#left-scroll img").click(function(){
				var item_width = $("#photo-bar-ul li").outerWidth() + 10;
				var left_indent = parseInt($("#photo-bar-ul").css("right")) + item_width;

				$("#photo-bar-ul").animate({"right" : left_indent}, {queue:false, duration:500},function(){
					$("#photo-bar-ul li:first").after($("#photo-bar-ul li:last"));
					$("#photo-bar-ul").css({"right" : "-120px"});
				});
			});
*/

			var auto_slide = 1;
			var hover_pause = 1;  
		        var key_slide = 1;  
  
        		var auto_slide_seconds = 5000;  
        		
			$('#photo-bar-ul li:first').before($('#photo-bar-ul li:last'));  
  
        		if(auto_slide == 1){  
            			var timer = setInterval('slide("right")', auto_slide_seconds);  
            			$('#hidden_auto_slide_seconds').val(auto_slide_seconds);  
		        }  
  
        		if(hover_pause == 1){  
            			$('#photo-bar-ul').hover(function(){  
                			clearInterval(timer)  
				},function(){  
                			timer = setInterval('slide("right")', auto_slide_seconds);  
				});  
		        }  
  
        		if(key_slide == 1){  
            			$(document).bind('keypress', function(e) {  
                			if(e.keyCode==37){  
                        			slide('left');  
			                }else if(e.keyCode==39){  
                        			slide('right');  
			                } 
				});  
		        }
		
			$("a.lightbox").lightBox();

		});


//FUNCTIONS BELLOW  
  
//slide function  
function slide(where){  
  
            //get the item width  
            var item_width = $('#photo-bar-ul li').outerWidth() + 10;  
  
            /* using a if statement and the where variable check 
            we will check where the user wants to slide (left or right)*/  
            if(where == 'right'){  
                //...calculating the new left indent of the unordered list (ul) for left sliding  
                var left_indent = parseInt($('#photo-bar-ul').css('right')) - item_width;  
            }else{  
                //...calculating the new left indent of the unordered list (ul) for right sliding  
                var left_indent = parseInt($('#photo-bar-ul').css('right')) + item_width;  
  
            }  
  
            //make the sliding effect using jQuery's animate function... '  
            jQuery('#photo-bar-ul:not(:animated)').animate({'right' : left_indent},500,function(){  
  
                /* when the animation finishes use the if statement again, and make an ilussion 
                of infinity by changing place of last or first item*/  
                if(where == 'left'){  
                    //...and if it slided to left we put the last item before the first item  
                    $('#photo-bar-ul li:first').before($('#photo-bar-ul li:last'));  
                }else{  
                    //...and if it slided to right we put the first item after the last item  
                    $('#photo-bar-ul li:last').after($('#photo-bar-ul li:first'));  
                }  
  
                //...and then just get back the default left indent  
                $('#photo-bar-ul').css({'right' : '-120px'});  
            });  
  
}
