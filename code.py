from sumolib import *
import time

start1 = Start1()
boot1 = Boot1()
led1, led2 = Led1(), Led2()
ledRgb1 = LedRgb1()
prawyCzujnik, glownyCzujnik, lewyCzujnik, dist4 = dists_init()
lewaZiemia, prawaZiemia, grd3, grd4 = grds_init()
lewySilnik, prawySilnik= motors_init()
vBat = VBat()

GRD_TRESHOLD = .7
DIST_TRESHOLD = .9
SEARCH_POWER = 0
ATTACK_POWER = 0

def prosto():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.forward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.forward()
    #ledRgb1.value = Color.WHITE

def prostoAtak():
    lewySilnik.power = ATTACK_POWER
    lewySilnik.forward()
    prawySilnik.power = ATTACK_POWER
    prawySilnik.forward()
    #ledRgb1.value = Color.RED

def prostoPrawo():
    lewySilnik.power = ATTACK_POWER
    lewySilnik.forward()
    prawySilnik.power = ATTACK_POWER/4
    prawySilnik.forward()
    #ledRgb1.value = Color.WHITE

def prostoLewo():
    lewySilnik.power = ATTACK_POWER/4
    lewySilnik.forward()
    prawySilnik.power = ATTACK_POWER
    prawySilnik.forward()
    #ledRgb1.value = Color.WHITE

def tyl():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.backward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.backward()
    #ledRgb1.value = Color.YELLOW

def tylLewo():
    lewySilnik.power = SEARCH_POWER/4
    lewySilnik.backward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.backward()
    #ledRgb1.value = Color.YELLOW

def tylPrawo():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.backward()
    prawySilnik.power = SEARCH_POWER/4
    prawySilnik.backward()
    #ledRgb1.value = Color.YELLOW

def stop():
    lewySilnik.stop()
    prawySilnik.stop()
    ledRgb1.value = Color.GREEN

def lewo():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.backward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.forward()
    #ledRgb1.value = Color.PINK

def prawo():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.forward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.backward()
    #ledRgb1.value = Color.PINK

def odliczanie():
    for i in range(10):
        ledRgb1.value = (250 - i*5, i*5, 0)
        time.sleep(0.1)
    for i in range(10):
        ledRgb1.value = (200 - i*5, 50 + i*5, 0)
        time.sleep(0.1)
    for i in range(10):
        ledRgb1.value = (150 - i*5, 100 + i*5, 0)
        time.sleep(0.1)
    for i in range(10):
        ledRgb1.value = (100 - i*5, 150 + i*5, 0)
        time.sleep(0.1)
    for i in range(10):
        ledRgb1.value = (50 - i*5, 200 + i*5, 0)
        time.sleep(0.1)

def decide():
    d1 = prawyCzujnik.value > DIST_TRESHOLD
    d2 = glownyCzujnik.value > DIST_TRESHOLD
    d3 = lewyCzujnik.value > DIST_TRESHOLD

    g1 = lewaZiemia.value < GRD_TRESHOLD
    g2 = prawaZiemia.value < GRD_TRESHOLD
    
    print('l ', lewaZiemia.value, g1, 'p ', prawaZiemia.value, g2)

    led1.value = g1
    led2.value = g2

    if d1 or d2 or d3:
        # na wprost
        if d2:
            prostoAtak()
        # po lewej
        elif d3:
            prostoLewo()
        # po prawej
        elif d1:
            prostoPrawo()

    elif g1 or g2:
        if g1 and g2:
            tylPrawo()
            time.sleep(0.5)
        elif g1:
            tylPrawo()
            time.sleep(0.5)
        elif g2:
            tylLewo()
            time.sleep(0.5)
    else:
        prosto()

ledRgb1.value = Color.BLACK
start1.waitFor()

#countdown()

while (True):
    decide()
    time.sleep(0.02)

