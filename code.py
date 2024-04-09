from sumolib import *
import time

print('hej')

lewySilnik, prawySilnik= motors_init()

start1 = Start1()
boot1 = Boot1()
led1 = Led1()
led2 = Led2()
ledRgb1 = LedRgb1()
dist1, prawyCzujnik, lewyCzujnik, glownyCzujnik = dists_init()

grd1, grd2, grd3, grd4 = grds_init()

vBat = VBat()

ledRgb1.brightness = 0.3
ledRgb1.value = Color.RED

lewySilnik.power = 0
prawySilnik.power = 0

start1.waitFor()

ledRgb1.value = Color.GREEN

while True:
    #print(lewySilnik, prawySilnik, lewyCzujnik.value, prawyCzujnik.value, glownyCzujnik.value)
    lewySilnik.power = 0
    prawySilnik.power = 0
    lewySilnik.forward()
    prawySilnik.forward()

    print('GRD1:', grd1, 'GRD2:', grd2, 'GRD3:', grd3, 'GRD4:', grd4)

    if lewyCzujnik.value > 1.3 and glownyCzujnik.value < 1.3:
        prawySilnik.power = .6
    elif prawyCzujnik.value > 1.3 and glownyCzujnik.value < 1.3:
        lewySilnik.power = .6

    if glownyCzujnik.value > 1.3:
        lewySilnik.power = 1
        prawySilnik.power = 1

    if boot1.value:
        lewySilnik.stop()
        prawySilnik.stop()
        ledRgb1.value = Color.GREEN
        break
    time.sleep(0.1)
