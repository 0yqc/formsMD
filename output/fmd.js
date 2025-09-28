input_elements = document.querySelectorAll('input, textarea, select') // auto-save
other_input_elements = document.querySelectorAll('div.answer_option.other') // dynamically hide other answer texts
textarea_elements = document.querySelectorAll('textarea') // auto-expand
multi_dropdown_answers = document.querySelectorAll('fieldset.dropdown.multiple .answer')

input_elements.forEach(load_input) // re-load saved input fields
textarea_elements.forEach(expand_textarea)
other_input_elements.forEach(other_check_disabled)
other_input_elements.forEach(other_check_text)
multi_dropdown_answers.forEach()

document.querySelector('form').addEventListener('input', function () {
	input_elements.forEach(save_input)
	textarea_elements.forEach(expand_textarea)
	other_input_elements.forEach(other_check_disabled)
})

// FUNCTIONS

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

function other_check_disabled(item) {
	inp_text = item.querySelector('input[type=text]')
	inp_option = item.querySelector('input[type=checkbox], input[type=radio]')
	if (inp_option.checked) {
		inp_text.required = true
		inp_text.placeholder = 'Type your answer here...'
	} else {
		inp_text.required = false
		inp_text.placeholder = ''
		inp_text.value = ''
	}
}

function other_check_text(item) {
	inp_text = item.querySelector('input[type=text]')
	inp_option = item.querySelector('input[type=checkbox], input[type=radio]')
	inp_text.addEventListener('input', function () {
		inp_option.checked = true
	})
}

function multi_dropdown_check(item) {

}