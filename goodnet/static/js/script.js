/* Author:

*/

		jQuery(document).ready(function() {

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

		});

