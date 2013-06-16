var count = 0;
function changed_vote(cb) {
	if (cb.checked) {
		count += 1;
	} else {
		count -= 1;
	}
	$('#num_votes').html(String(count));
}
