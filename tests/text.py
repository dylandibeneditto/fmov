from fmov import Text

content = """
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
this, is a test of the punctuation, breaking, etc. I also want to make sure of the allowance of manual new lines \nhopefully that works
"""

t = Text(text=content, position=(0,0), max_width=50, line_limit=50)
print(t.display_text())
