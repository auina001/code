import sys, time

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)
    print('')

print_slow('Velkommen til flappy bird!')
print_slow('Trykk space for å hoppe og pil til høyre for å skyte')
print('')
print_slow('Press enter for å starte...')
