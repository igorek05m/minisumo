from sumolib import *
import time

start1 = Start1()
boot1 = Boot1()
led1, led2 = Led1(), Led2()
ledRgb1 = LedRgb1()
prawyCzujnik, glownyCzujnik, lewyCzujnik, dist4 = dists_init()
lewaZiemia, prawaZiemia, tylZiemia, grd4 = grds_init()
lewySilnik, prawySilnik = motors_init()
vBat = VBat()

GRD_TRESHOLD = 0.7
BACKGRD_TESHOLD = 1.2
DIST_TRESHOLD = 0.8
SEARCH_POWER = 0.5
ATTACK_POWER = 1
BACKWARDS_POWER = 0.6

delta_time = 0.1

state = None

class State:
    def Update(self):
        pass
    def __str__(self):
        return self.__class__.__name__
    def ChangeState(self):
        global state
        for condition, next_state in self.stateTransitions:
            if condition():
                state = next_state()

class SearchState(State):
    def __init__(self):
        self.stateTransitions = [
            ((lambda: (d1 or d2 or d3)), (lambda: AttackState())),
            ((lambda: (g2 and not (g1 or g3))), (lambda: MovingBackward(0.5, 'right'))),
            ((lambda: (g1 and not (g2 or g3))), (lambda: MovingBackward(0.5, 'left'))),
            ((lambda: ((g1 and g2) and not g3)), (lambda: MovingBackward(0.5, 'right'))),
            ((lambda: (g3 and not (g1 or g2))), (lambda: AttackState())),
            ((lambda: (g3 and g1) and not g2), (lambda: LineAndSideDetected(0.5, 'right'))),
            ((lambda: (g3 and g2) and not g1), (lambda: LineAndSideDetected(0.5, 'left')))
        ]
    def Update(self):
        lewySilnik.power = SEARCH_POWER
        prawySilnik.power = SEARCH_POWER
        lewySilnik.forward()
        prawySilnik.forward()
        ledRgb1.value = Color.CYAN

class AttackState(State):
    def __init__(self):
        self.stateTransitions = [
            ((lambda: not (d1 or d2 or d3)), (lambda: SearchState()))
        ]
    def Update(self):
        lewySilnik.forward()
        prawySilnik.forward()
        ledRgb1.value = Color.RED
        if d1:
            lewySilnik.power = ATTACK_POWER
            prawySilnik.power = ATTACK_POWER/4
        elif d3:
            lewySilnik.power = ATTACK_POWER/4
            prawySilnik.power = ATTACK_POWER
        elif d2:
            lewySilnik.power = ATTACK_POWER
            prawySilnik.power = ATTACK_POWER

class LineAndSideDetected(State):
    def __init__(self, time_to_change, direction):
        self.time_to_change = time_to_change
        self.direction = direction
        self.stateTransitions = [
            ((lambda: (self.time_to_change <= 0 and not (d1 or d2 or d3))), (lambda: SearchState())),
            ((lambda: (d1 or d2 or d3)), (lambda: AttackState()))
        ]
    def Update(self):
        self.time_to_change -= delta_time
        if self.direction == 'right':
            lewySilnik.power = SEARCH_POWER
            lewySilnik.forward()
            prawySilnik.power = SEARCH_POWER
            prawySilnik.backward()
            ledRgb1.value = Color.PURPLE
        elif self.direction == 'left':
            lewySilnik.power = SEARCH_POWER
            lewySilnik.backward()
            prawySilnik.power = SEARCH_POWER
            prawySilnik.forward()
            ledRgb1.value = Color.PURPLE

class MovingBackward(State):
    def __init__(self, time_to_change, direction):
        self.time_to_change = time_to_change
        self.direction = direction
        self.stateTransitions = [
            ((lambda: (self.time_to_change <= 0 and not (d1 or d2 or d3))), (lambda: SearchState())),
            ((lambda: (d1 or d2 or d3)), (lambda: AttackState()))
        ]
    def Update(self):
        self.time_to_change -= delta_time
        if self.direction == 'left':
            lewySilnik.power = BACKWARDS_POWER/4
            lewySilnik.backward()
            prawySilnik.power = BACKWARDS_POWER
            prawySilnik.backward()
            ledRgb1.value = Color.YELLOW
        elif self.direction == 'right':
            lewySilnik.power = BACKWARDS_POWER
            lewySilnik.backward()
            prawySilnik.power = BACKWARDS_POWER/4
            prawySilnik.backward()
            ledRgb1.value = Color.YELLOW

state: State = SearchState()

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

ledRgb1.value = Color.CYAN

start1.waitFor()

# odliczanie()

while (True):
    d1 = prawyCzujnik.value > DIST_TRESHOLD
    d2 = glownyCzujnik.value > DIST_TRESHOLD
    d3 = lewyCzujnik.value > DIST_TRESHOLD

    g1 = lewaZiemia.value < GRD_TRESHOLD
    g2 = prawaZiemia.value < GRD_TRESHOLD
    g3 = tylZiemia.value < BACKGRD_TESHOLD

    led1.value = g1
    led2.value = g2

    state.ChangeState()
    state.Update()
    time.sleep(delta_time)

    print(state)
