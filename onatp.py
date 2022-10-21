import random

class Mike(): # her lager vi egenskapene til hovedkarakteren,Mike
    def __init__(self,navn,hp):
        self.navn = navn
        self.hp = hp
        
    def heal(self, healing):
        self.hp += healing

    def lose_hp(self,damage):
        self.hp -= damage


class Enemy(): #her lager vi vi egenskapene til "Enemy"
    def __init__(self, navn, hp, word):
        self.navn = navn
        self.hp = hp
        self.word = word

    def lose_hp(self,damage):
        self.hp -= damage


level = 0  #level

hovedperson = Mike ("Mike", 100)
m = Enemy
print('\x1b[6;36;47m' + 'Velkommen' + '\x1b[0m')
print("Hei jeg er Mike","hp:",hovedperson.hp)
print("Du må kjempe med 3 utfordrere for å vinne dette spillet")

try:   #"press enter" for å fortsette 
    input('\x1b[6;30;42m' + 'Press enter to continue and attack' + '\x1b[0m')
except SyntaxError:
    pass  #fortsett 
Enemyss=[0,0,0]

Enemyss[0] = m("Enemy NR1",80, "e")
Enemyss[1] = m("Enemy NR2",90, "")
Enemyss[2] = m("Enemy NR3",100, "du er sterk")

protection = 0
extra_damage = 1
ability_counter = 0
start_line = False

while True:
    if (start_line == False):
        print("Hei,jeg er ",Enemyss[level].navn,"hp:", Enemyss[level].hp)
        ability_counter = 0
        start_line = True

    extra_damage = 1
    protection = 2
    ability = ""
    if (ability_counter <2):
        ability= input('\x1b[0;30;43m' +'Du har to abilities: double damage og heal' + '\x1b[0m')

    if (ability == "heal"):
        healing = random.randint(20, 30)
        hovedperson.heal(healing)
        print("du healet og har nå", hovedperson.hp, "liv")
    elif (ability == "extra damage"):
        extra_damage= 2 ##########3spør her
    elif (ability =="shield"):
        protection = 1
    if (ability != ""):
        ability_counter +=1

    damage = random.randint(15*extra_damage,25*extra_damage)  #damage mellom 15 og 25 hp
    hoved_damage = random.randint(5*protection, 10*protection) 
    print("enemy mister", damage, "liv")
    print("du mister", hoved_damage, "liv")
    Enemyss[level].lose_hp(damage)
    hovedperson.lose_hp(hoved_damage)

    if (Enemyss[level].hp <= 0):
        Enemyss[level].hp = 0
    if (hovedperson.hp <= 0):
        hovedperson.hp = 0

    print("Din hp:", hovedperson.hp, "Enemys hp:",Enemyss[level].hp)

    if (Enemyss[level].hp == 0):
        if (level == 2):
            print('\x1b[7;32;47m' + 'Success! Du vant' + '\x1b[0m')
            exit()
        print("rip", Enemyss[level].navn,"døde")
        level += 1
        start_line = False

    if (hovedperson.hp ==0):    #hvis hp=0, game over
        print('\x1b[7;31;47m' + 'GAME OVER!' + '\x1b[0m')
        exit()    
