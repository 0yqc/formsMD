other_txts = document.querySelectorAll('div.answer.other')
other_txts.forEach(init)

async function init(item) {
	check(item)
	document.querySelector('form').addEventListener('change',function () {
		check(item)
	})
}

function check(item) {
	if (item.querySelector('input[type=checkbox], input[type=radio]').checked) {
		item.querySelector('input[type=text]').classList.remove('hidden')
	} else {
		item.querySelector('input[type=text]').classList.add('hidden')
	}
}