const input_elements = document.querySelectorAll('input, textarea, select:not(.multiple)') // auto-save
const other_input_elements = document.querySelectorAll('div.answer_option.other') // dynamically hide other answer texts
const textarea_elements = document.querySelectorAll('textarea') // auto-expand
const multi_dropdown_answer_elements = document.querySelectorAll('fieldset.dropdown.multiple .answer')
var multi_dropdown_close_buttons = null
multi_dropdown_answer_elements?.forEach(multi_dropdown_check)
multi_dropdown_close_buttons?.forEach(multi_dropdown_button_listener)

input_elements?.forEach(load_input) // re-load saved input fields
textarea_elements?.forEach(expand_textarea)
other_input_elements?.forEach(other_check_disabled)
other_input_elements?.forEach(other_check_text)

document.querySelector('form').addEventListener('input', function () {
	input_elements?.forEach(save_input)
	textarea_elements?.forEach(expand_textarea)
	other_input_elements?.forEach(other_check_disabled)
	multi_dropdown_answer_elements?.forEach(multi_dropdown_check)
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
	const inp_text = item.querySelector('input[type=text]')
	const inp_option = item.querySelector('input[type=checkbox], input[type=radio]')
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
	const inp_text = item.querySelector('input[type=text]')
	const inp_option = item.querySelector('input[type=checkbox], input[type=radio]')
	inp_text.addEventListener('input', function () {
		inp_option.checked = true
	})
}

function multi_dropdown_check(item) {
	const answers_div = item.querySelector('div.answers')
	const select = item.querySelector('select')
	const options = item.querySelectorAll('option')
	const selected = select.options[select.selectedIndex]
	const hidden = item.querySelector('input[type=hidden]')
	if (selected.value !== '' && selected.classList.contains('selected')) {
		selected.classList.remove('selected')
	} else if (selected.value !== '') {
		selected.classList.add('selected')
	}
	options?.forEach(function (item) {
		if (item.classList.contains('selected')) {
			let div = document.createElement('div')
			div.id = item.id + '_selected'
			if (!document.getElementById(div.id)) {
				div.innerHTML = `<span class="text">${item.innerHTML}</span><span class="close"><button type="button">×</button></span>`
				answers_div.appendChild(div)
				multi_dropdown_button_listener(div)
				hidden.value = hidden.value + `${item.innerHTML} (${item.id}) \n`
			}
		} else if (!item.classList.contains('selected')) {
			let div = document.getElementById(item.id + '_selected')
			if (div) {
				div.remove()
				hidden.value = hidden.value.replace(`${item.innerHTML} (${item.id}) \n`, '')
			}
			select.selectedIndex = 0
		}
	})
	multi_dropdown_close_buttons = document.querySelectorAll('fieldset.dropdown.multiple .answer .answers div')
}

function multi_dropdown_button_listener(item) {
	const button = item.querySelector('span.close button')
	button.addEventListener('click', multi_dropdown_button_click_handle)
	function multi_dropdown_button_click_handle() {
		const option_id = item.id.replace('_selected', '')
		document.getElementById(option_id).classList.remove('selected')
		multi_dropdown_answer_elements?.forEach(multi_dropdown_check)
		button.removeEventListener('click', multi_dropdown_button_click_handle)
	}
}