other_input = document.querySelectorAll('div.answer.other') // dynamically hide other answer texts
other_input.forEach(check_other_visible) // check if they should be visible or not

input_elements = document.querySelectorAll('input, textarea, select') // auto-save
input_elements.forEach(load_input) // re-load saved input fields

textarea_elements = document.querySelectorAll('textarea') // auto-expand
textarea_elements.forEach(expand_textarea)

document.querySelector('form').addEventListener('change', function () {
	// change is for checkbox, radio
	other_input.forEach(check_other_visible) // dynamically hide other answer texts
	input_elements.forEach(save_input)
})

document.querySelector('form').addEventListener('input', function () {
	// input is for text, textarea
	input_elements.forEach(save_input)
	textarea_elements.forEach(expand_textarea)
})

// FUNCTIONS

function check_other_visible(item) {
	if (item.querySelector('input[type=checkbox], input[type=radio]').checked) {
		item.querySelector('input[type=text]').removeAttribute('disabled')
	} else {
		item.querySelector('input[type=text]').setAttribute('disabled', 'true')
	}
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