# Gra parkour w Minecraft
# Autor: Marcinosoft

from mcpi.minecraft import Minecraft               # funkcje dla Minecraft
import mcpi.block as block                         # definicje bloków w Minecraft
import random                                      # losowanie liczb
import time                                        # operacje na czasie

# funkcja wstawiająca docelowy blok niedaleko startowego
def losuj_blok(x, y, z):
    a = x + random.randint(1,3)                    # wylosuj współrzędną x bloku docelowego
    b = y + random.randint(-1,1)                   # wylosuj współrzędną y bloku docelowego
    c = z + random.randint(-3,3)                   # wylosuj współrzędną z bloku docelowego
    kolor = random.randint(0,15)                   # wylosuj cechę bloku wełny - kolor
    mc.setBlock(a, b, c, block.WOOL.id, kolor)     # wstaw wylosowany blok docelowy
    return a, b, c                                 # zwróć współrzędne bloku docelowego

print('Start gry')
mc = Minecraft.create('127.0.0.1')                 # podłącz do serwera gry

nick_gracza = 'Gracz1'                             # nick własnego gracza
punkty = 0                                         # licznik punktów
ilosc_blokow = 15                                  # z ilu bloków składa się parkour
licznik_blokow = 0                                 # licznik pokonanych bloków

# wyczyść kawałek świata pod grę parkour - wypełnij go blokami powietrza
mc.setBlocks(-10,60,-15, 3*ilosc_blokow, 80, 15, block.AIR.id)

x1, y1, z1 = 0, 70, 0                              # współrzędne bloku startowego x1,y1,z1
mc.setBlock(x1, y1, z1, block.WOOL.id, 1)          # wstaw blok startowy, białą wełnę
id_gracza = mc.getPlayerEntityId(nick_gracza)      # pobierz id gracza
mc.entity.setPos(id_gracza, x1, y1+1, z1)          # teleportuj gracza na blok startowy
x2, y2, z2 = losuj_blok(x1, y1, z1)                # wylosuj i wstaw blok docelowy w x2,y2,z2

mc.postToChat(f'Gracz {nick_gracza} zaczyna parkour')  # poinformuj o starcie gry na czacie
start = time.time()                                # zapamiętaj czas startu gry

while True:
    x, y, z = mc.entity.getTilePos(id_gracza)      # pobierz współrzędne gracza

    # jeśli blok docelowy został zniszczony - odbuduj go
    blok = mc.getBlock(x2,y2,z2)                   # pobierz rodzaj bloku w miejscu docelowym
    if blok == block.AIR.id:                       # jeśli w docelowym miejscu jest powietrze
        kolor = random.randint(0,15)               # wylosuj cechę - kolor bloku wełny
        mc.setBlock(x2,y2,z2,block.WOOL.id,kolor)  # wstaw w miejscu docelowego bloku wełnę

    # jeżeli gracz spadł poniżej wysokości bloku docelowego:
    if y < y2:
        # jeśli gracz spadł, bo zniszczył blok startowy - odbuduj go
        blok = mc.getBlock(x1,y1,z1)               # pobierz rodzaj bloku w miejscu docelowym
        if blok == block.AIR.id:                   # jeśli w docelowym miejscu jest powietrze
            kolor = random.randint(0,15)
            mc.setBlock(x1,y1,z1,block.WOOL.id,kolor)
        else:
            punkty -= 1                            # odejmij punkt
        # teleportuj garcza na blok startowy
        mc.entity.setPos(id_gracza, x1, y1+1, z1)

    # jeśli gracz skoczył na blok docelowy:
    if x == x2 and y-1 == y2 and z == z2:
        mc.setBlock(x1, y1, z1, block.AIR.id)      # usuń blok startowy
        x1, y1, z1 = x2, y2, z2                    # blok docelowy staje się nowym startowym
        punkty += 1                                # dodaj punkt
        licznik_blokow += 1                        # zwiększ licznik pokonanych bloków
        if licznik_blokow == ilosc_blokow:         # jeśli gracz pokonał wszystkie bloki to koniec
            break
        zostalo = ilosc_blokow - licznik_blokow    # policz ile bloków zostało do końca gry
        mc.postToChat(f'Graczowi {nick_gracza} zostało: {zostalo} bloków')
        x2, y2, z2 = losuj_blok(x1, y1, z1)        # wylosuj i wstaw nowy blok docelowy w x2,y2,z2

stop = time.time()                                 # zapamiętaj czas końca gry
czas = stop - start                                # wylicz ile sekund trwała gra
czas = time.gmtime(czas)                           # stwórz stempel czasu z ilości sekund
czas = time.strftime('%H:%M:%S', czas)             # formatuj stempel czasu
mc.postToChat(f'Wynik gracza {nick_gracza}: punkty: {punkty}, czas: {czas}')
print('Koniec gry')
