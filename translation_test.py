from googletrans import Translator

translator = Translator()
translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
for translation in translations:
    print(translation.origin, ' -> ', translation.text)

print(translator.translate('''Allie couldn't take much more of her earnestness. She headed for the door, leaving her bag behind. 'I'm off. If I'm not back in an hour, send a search party.''', src='en', dest='pl'))
