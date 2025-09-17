document.getElementById('fmd_form').addEventListener('submit', function (event) { // execute this function when the form is submitted
	event.preventDefault() // prevent default form events
	const formdata = new FormData(this) // get all the form data

	let link = 'mailto:luna_hagemann@gmx.de?subject=New formsMD Form Submission!&body=You need to send this email for your result to count.' // base email link, New formsMD Form Submission! gets replaced by Py processing

	for (const key of formdata.keys()) { // loop through the form data
		if (formdata.get(key).toString().length > 0) { // only proceed if the value of a given key exists (is 1 or more chars long)
			link = link + '%0A%0A%0AKey: ' + key.trim() + '%0A%0AValue: ' + encodeURIComponent(formdata.get(key).toString().trim()) // add this data to the link, %0D%0A is the unicode escape sequence for newlines, which can be used in links, ecodeURIComponent() is being used to encode input fileds for email conversion
		}
	}

	window.location.href = link // open the contructed link
	window.location.href = window.location.href // gets replaced by Py processing
})