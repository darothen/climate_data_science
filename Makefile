
deck = basic_pandas

slides: $(deck).ipynb
	jupyter-nbconvert  $< --to slides --reveal-prefix=reveal.js
serve: $(deck).ipynb
	jupyter-nbconvert  $< --to slides --post serve

clean:
	rm $(deck).slides.html
