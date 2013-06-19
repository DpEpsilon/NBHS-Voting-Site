var count = 0;

boxes = $('.vote_box');
for (var i = 0; i < boxes.length; i++) {
	// Just to make sure
	boxes[i].checked = false;
}

function changed_vote(cb) {
	if (cb.checked) {
		count += 1;
	} else {
		count -= 1;
	}
	$('#num_votes').html(String(count));
	if (count === $('#variables').data('num-votes')) {
		boxes = $('.vote_box');

		for (var i = 0; i < boxes.length; i++) {
			
			if (boxes[i].checked === false) {
				boxes[i].disabled = true;
			}
		}
		//$('#submit_votes')[0].disabled = false;
		$('.vote_counter').css('background-color','#beb')
		$('.vote_counter').css('border-color','#ada')
	} else {
		boxes = $('.vote_box');

		for (var i = 0; i < boxes.length; i++) {
			boxes[i].disabled = false;
		}
		//$('#submit_votes')[0].disabled = true;
		$('.vote_counter').css('background-color','#eee')
		$('.vote_counter').css('border-color','#ddd')
	}
}
