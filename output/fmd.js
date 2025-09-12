input_elements = document.querySelectorAll('input, textarea, select') // auto-save
input_elements.forEach(load_input) // re-load saved input fields

other_input = document.querySelectorAll('div.answer_option.other') // dynamically hide other answer texts
other_input.forEach(check_other_disabled) // check if they should be visible or not
other_input.forEach(check_other_clicked) // check if they are clicked to select appropriate radio/checkbox

textarea_elements = document.querySelectorAll('textarea') // auto-expand
textarea_elements.forEach(expand_textarea)

document.querySelector('form').addEventListener('change', function () {
	// change is for checkbox, radio
	other_input.forEach(check_other_disabled) // dynamically hide other answer texts
	input_elements.forEach(save_input)
})

document.querySelector('form').addEventListener('input', function () {
	// input is for text, textarea
	input_elements.forEach(save_input)
	textarea_elements.forEach(expand_textarea)
})

// FUNCTIONS

function check_other_disabled(item) {
	if (item.querySelector('input[type=checkbox], input[type=radio]').checked) {
		item.querySelector('input[type=text]').setAttribute('required', '')
		item.querySelector('input[type=text]').setAttribute('placeholder', 'Enter your answer here...')
	} else {
		item.querySelector('input[type=text]').removeAttribute('required')
		item.querySelector('input[type=text]').removeAttribute('placeholder')
		item.querySelector('input[type=text]').value = ''
	}
}

function check_other_clicked(item) {
	item.querySelector('input[type=text]').addEventListener('mousedown', function () {
		item.querySelector('input[type=checkbox], input[type=radio]').checked = true
		check_other_disabled(item)
		save_input(item.querySelector('input[type=checkbox], input[type=radio]'))
	})
}

function save_input(item) {
	if (item.type === 'radio' || item.type === 'checkbox') {
		localStorage.setItem(item.id, item.checked)
	} else {
		localStorage.setItem(item.id, item.value)
	}
}

function load_input(item) {
	if (localStorage.getItem(item.id)) {
		if (item.type === 'radio' || item.type === 'checkbox') {
			item.checked = (localStorage.getItem(item.id) === 'true')
		} else {
			item.value = localStorage.getItem(item.id)
		}
	}
}

function expand_textarea(item) {
	item.style.height = item.scrollHeight + 'px'
}