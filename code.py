from sumolib import *
import time

start1 = Start1()
boot1 = Boot1()
led1, led2 = Led1(), Led2()
ledRgb1 = LedRgb1()
prawyCzujnik, glownyCzujnik, lewyCzujnik, dist4 = dists_init()
lewaZiemia, prawaZiemia, grd3, grd4 = grds_init()
lewySilnik, prawySilnik = motors_init()
vBat = VBat()

GRD_TRESHOLD = 0.7
DIST_TRESHOLD = 0.8
SEARCH_POWER = 0.2
ATTACK_POWER = 1
BACKWARDS_POWER = 0.5

def stop():
    lewySilnik.stop()
    prawySilnik.stop()
    ledRgb1.value = Color.GREEN

def prosto():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.forward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.forward()

def prostoAtak():
    lewySilnik.power = ATTACK_POWER
    lewySilnik.forward()
    prawySilnik.power = ATTACK_POWER
    prawySilnik.forward()
    ledRgb1.value = Color.RED

def prostoPrawo():
    lewySilnik.power = ATTACK_POWER
    lewySilnik.forward()
    prawySilnik.power = ATTACK_POWER/4
    prawySilnik.forward()
    ledRgb1.value = Color.WHITE

def prostoLewo():
    lewySilnik.power = ATTACK_POWER/4
    lewySilnik.forward()
    prawySilnik.power = ATTACK_POWER
    prawySilnik.forward()
    ledRgb1.value = Color.WHITE

def tyl():
    stop()
    lewySilnik.power = BACKWARDS_POWER
    lewySilnik.backward()
    prawySilnik.power = BACKWARDS_POWER
    prawySilnik.backward()
    ledRgb1.value = Color.YELLOW

def tylLewo():
    stop()
    lewySilnik.power = BACKWARDS_POWER/3
    lewySilnik.backward()
    prawySilnik.power = BACKWARDS_POWER
    prawySilnik.backward()
    ledRgb1.value = Color.YELLOW

def tylPrawo():
    stop()
    lewySilnik.power = BACKWARDS_POWER
    lewySilnik.backward()
    prawySilnik.power = BACKWARDS_POWER/3
    prawySilnik.backward()
    ledRgb1.value = Color.YELLOW

def lewo():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.backward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.forward()
    ledRgb1.value = Color.PURPLE

def prawo():
    lewySilnik.power = SEARCH_POWER
    lewySilnik.forward()
    prawySilnik.power = SEARCH_POWER
    prawySilnik.backward()
    ledRgb1.value = Color.PURPLE

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
    
    print('prawy: ', prawyCzujnik.value, 'srodkowy: ', glownyCzujnik.value, 'lewy: ',  lewyCzujnik.value)
    
    if g1 or g2:
        if g1 and g2:
            tylPrawo()
            time.sleep(0.5) 
        elif g1:
            tylLewo()
            time.sleep(0.5)
        elif g2:
            tylPrawo()
            time.sleep(0.5)
    elif d1 or d2 or d3:
        # na wprost
        if d2:
            prostoAtak()
            time.sleep(0.2)
        # po lewej
        elif d3:
            lewo()
            time.sleep(0.2)
        # po prawej
        elif d1:
            prawo()
            time.sleep(0.2)
    else:
        prostoLewo()

ledRgb1.value = Color.CYAN
start1.waitFor()

#countdown()

while (True):
    decide()
    time.sleep(0.001)

