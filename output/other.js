other_input = document.querySelectorAll('div.answer.other') // dynamically hide other answer texts
other_input.forEach(check_other_visible)

input = document.querySelectorAll('input, textarea, select')

document.querySelector('form').addEventListener('change', function () {
	// change is for checkbox, radio
	other_input.forEach(check_other_visible)
	input.forEach(save_input)
})

document.querySelector('form').addEventListener('input', function () {
	// input is for text, textarea
	input.forEach(save_input)
})

input.forEach(load_input)

// FUNCTIONS

function check_other_visible(item) {
	if (item.querySelector('input[type=checkbox], input[type=radio]').checked) {
		item.querySelector('input[type=text]').removeAttribute('disabled')
	} else {
		item.querySelector('input[type=text]').setAttribute('disabled','true')
	}
}

function save_input(item) {
	localStorage.setItem(item.id, item.value)
}

function load_input(item) {
	if (localStorage.getItem(item.id)) {
		item.value = localStorage.getItem(item.id)
	}
}