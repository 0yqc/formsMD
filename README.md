# formsMD
advanced markdown extension to handle form elements and logic

Use *formsMD* to create forms and surveys with ease and host them on your own infrastructure (such as a custom server, or even GitHub/GitLab/Cloudflare Pages, etc.), fully client side! You can write forms in a MarkDown like syntax with complete support for all Markdown syntaxes, so you can style it well and *formsMD* will convert it into a fully working, good-looking online form which you can share and get results on.

# Question Types

- Radio Buttons / Multiple-Choice (incl. Other, this:)
- Checkbox (incl. Other, this:)
- Text, Number, E-Mail, Date, etc. (HTML Input Element with variable Type)
- Textarea / Multi-line Text
- Dropdown (single and multiple (custom))
- Matrix (most input types possible)

# Install & Run

1. Clone the repository:
   `git clone https://github.com/0yqc/formsMD/`

2. Set your CWD (current working directory):
   `cd ~/path/to/formsMD/`

4. Run `./core_convert/main.py -i ~/path/to/input/file/ -o ~/path/to/output/directory/ -a ./core_convert/assets/`