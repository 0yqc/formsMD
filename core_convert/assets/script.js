document.getElementById('page1_form').addEventListener('submit', function (event) { // execute this function when the form is submitted
	event.preventDefault() // prevent default form events
	const formData = new FormData(this) // get all the form data

	link = 'mailto:0yqc@duck.com?subject=Form Submission&body=' // base email link

	for (const key of formData.keys()) { // loop through the form data
		if (formData.get(key).toString().length > 0) { // only proceed if the value of a given key exists (is 1 or more chars long)
			link = link + '%0D%0A%0D%0AKey: ' + key.trim() + '%0D%0AValue:' + formData.get(key).toString().trim() // add this data to the link, %0D%0A is the unicode escape sequence for newlines, which can be used in links
		}
	}

	window.location.href = link // open the contructed link
})