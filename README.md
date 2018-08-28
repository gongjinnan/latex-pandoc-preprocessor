Latex to Markdown Preprocessor
==============================

Annoyed that Pandoc doesn't correctly handle figure labels? Well, this module
is just for you!

```ltmd``` uses regex to extract figures, references, and mathematics, and 
processes them separately to Pandoc so that the figure references, etc. are
preserved.

Usage
-----

Use:
```
python3 preprocess.py <input> <output>
```
for example to generate the test markdown, we use
```
python3 preprocess.py test.tex test.md
```

The module can also be used through an API, through the two objects that are given.

One should use:

```python
pre_processed = ltmd.PreProcess(input_text)
pandocced = ltmd.run_pandoc(pre_processed.parsed_text)
post_processed = ltmd.PostProcess(pandocced, pre_processed.parsed_data)
```

The final output string can then be extracted by using ```post_processed.parsed_text```.

It is also possible to use a wrapper function in ```ltmd``` from markdown,

```
ltmd.inputoutput.parse_file(input_filename, output_filename)
```

Requirements
------------

+ ```python3``` (no ```python2``` version will *ever* be made available)
+ ```pandoc``` somewhere in your path.
+ ```pypandoc```

Several things should be done
------------
1. Preprocessing
`python3 preprocess.py input.tex output.md debug`

2. Remove labels in figure
In sublime text, open output.md
Find using RegEx: `\\label\{fig:(.*?)\}`
replace to:

3. Change figure reference
In sublime text, open output.md
Find using RegEx:  `\[@fig:(.*?)\]`
replace to: `{@fig:$1}`

4. Align figure in center
In sublime text, open output.md
Find using RegEx: `!\[(.*?)\]\((.*?)\){#fig:(.*?)}`
replace to: `<div align=center>\n![$1]\($2){#fig:$3}\n</div>`

5. Fix multi-citations
In sublime text, open output.md
Find using RegEx: `\[@(.*?), (.*)\]`
replace to: `[@$1; @$2]`
***Several times!!!***

6. Convert to docx
pandoc --filter pandoc-fignos --filter pandoc-citeproc --bibliography=mybib.bib --csl=elsevier-harvard.csl output.md -o output.docx

