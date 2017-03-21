from praatinterface import PraatLoader
basic_script ='echo hello'
pl = PraatLoader(debug = True)
pl.ini
text = pl.run_script('basic')
formants = pl.read_praat_out(text)
print text
# assert(text=='hello')