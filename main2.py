#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
try:
    from pybricks.nxtdevices import LightSensor
except ImportError:
    LightSensor = None
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
import sys

# Initialisiere den EV3
ev3 = EV3Brick()

# ======================================================================
# 1. BITTE HIER DIE PORTS ANPASSEN 
# ======================================================================

# Motoren-Ports (Wahrscheinlich Port B und D, hier bei Bedarf ändern)
PORT_MOTOR_LINKS = Port.B
PORT_MOTOR_RECHTS = Port.D

# Sensor-Ports (Bitte richtig verkabeln oder hier im Code anpassen!)
PORT_SENSOR_LINKS = Port.S4      # Linker Licht-/Farbsensor
PORT_SENSOR_RECHTS = Port.S1     # Rechter Licht-/Farbsensor
PORT_ULTRASCHALL = Port.S2       # Ultraschallsensor

# ======================================================================
# 2. EINSTELLUNGEN & SCHWELLENWERTE (Ggf. anpassen)
# ======================================================================

# Schwellenwert für Schwarz/Weiß (0 = Schwarz, 100 = Weiß)
# Werte unter diesem Wert werden als "Schwarz" (Linie) erkannt.
SCHWARZ_SCHWELLENWERT = 30 

# Ultraschall: Ab welchem Wert soll der Roboter anhalten (in Millimeter)
# Tischkante: Der Wert wird groß, wenn er nach unten schaut und der Tisch aufhört.
MAX_ABSTAND_TISCH = 250  # mm - Wert größer als dieser bedeutet "Tischkante / Abgrund"
MIN_ABSTAND_HINDERNIS = 100 # mm - Wert sehr klein bedeutet "Hindernis am Tisch"

# Fahr-Einstellungen
FAHR_GESCHWINDIGKEIT = 150 # mm/s (Geschwindigkeit auf der Geraden)
LENK_GESCHWINDIGKEIT = 100 # mm/s (Geschwindigkeit während der Kurve)
LENK_RATE = 120            # Grad/s (Wie stark er in der Kurve dreht, anpassen falls er zu schwach lenkt)

# ======================================================================
# 3. INITIALISIERUNG DER HARDWARE
# ======================================================================

try:
    motor_links = Motor(PORT_MOTOR_LINKS)
    motor_rechts = Motor(PORT_MOTOR_RECHTS)
    
    # DriveBase vereinfacht das Fahren und Lenken
    robot = DriveBase(motor_links, motor_rechts, wheel_diameter=55.5, axle_track=104)
except Exception as e:
    print("FEHLER: Motoren nicht gefunden! Bitte Ports prüfen:", e)
    sys.exit()

def init_lichtsensor(port):
    try:
        # 1. Versuche, ob es der neue EV3 Farbsensor ist
        return ColorSensor(port)
    except:
        pass
    try:
        # 2. Falls nein, versuche, ob es der alte NXT Lichtsensor ist
        return LightSensor(port)
    except:
        return None

sensor_links = init_lichtsensor(PORT_SENSOR_LINKS)
if sensor_links is None:
    print("FEHLER: Linker Sensor an Port", PORT_SENSOR_LINKS, "fehlt!")
    sys.exit()

sensor_rechts = init_lichtsensor(PORT_SENSOR_RECHTS)
if sensor_rechts is None:
    print("FEHLER: Rechter Sensor an Port", PORT_SENSOR_RECHTS, "fehlt!")
    sys.exit()

try:
    ultraschall = UltrasonicSensor(PORT_ULTRASCHALL)
except Exception as e:
    print("FEHLER: Ultraschallsensor an Port", PORT_ULTRASCHALL, "fehlt!")
    sys.exit()

ev3.speaker.beep() # Kurzes Piepen wenn bereit
print("Roboter ist startklar!")

# ======================================================================
# 4. HAUPTSCHLEIFE (ROBOTER VERHALTEN)
# ======================================================================

while True:
    # A) Ultraschallsensor überprüfen (Auf Wunsch deaktiviert)
    # abstand = ultraschall.distance()
    # if abstand > MAX_ABSTAND_TISCH or abstand < MIN_ABSTAND_HINDERNIS:
    #     robot.stop()
    #     print("Sicherheits-Stopp! Abstand:", abstand)
    #     ev3.speaker.beep(frequency=400, duration=100)
    #     wait(200)
    #     continue

    # B) Lichtsensoren ablesen (Wert zwischen 0 und 100)
    wert_links = sensor_links.reflection()
    wert_rechts = sensor_rechts.reflection()
    
    # ZEIGE AN: Was sehen die Sensoren gerade?
    print("Messergebnis -> Links:", wert_links, "| Rechts:", wert_rechts)
    
    # C) Lenk-Logik (Der Roboter fährt *zwischen* den schwarzen Linien)
    ist_links_schwarz = wert_links < SCHWARZ_SCHWELLENWERT
    ist_rechts_schwarz = wert_rechts < SCHWARZ_SCHWELLENWERT
    
    if ist_links_schwarz and not ist_rechts_schwarz:
        # Linker Sensor sieht Schwarz -> droht die linke Linie zu übertreten -> nach RECHTS lenken
        robot.drive(LENK_GESCHWINDIGKEIT, LENK_RATE)
        ev3.speaker.beep(frequency=800, duration=50) # Hoher Pieps
        
    elif ist_rechts_schwarz and not ist_links_schwarz:
        # Rechter Sensor sieht Schwarz -> droht die rechte Linie zu übertreten -> nach LINKS lenken
        robot.drive(LENK_GESCHWINDIGKEIT, -LENK_RATE)
        ev3.speaker.beep(frequency=600, duration=50) # Etwas tieferer Pieps
        
    elif ist_links_schwarz and ist_rechts_schwarz:
        # Beide sehen schwarz -> Z.B. Ende des Tisches markiert -> Stopp
        robot.stop()
        ev3.speaker.beep(frequency=400, duration=200) # Langer tiefer Warnton
        wait(50)
        
    else:
        # Beide sehen Weiß -> Alles gut, fahre geradeaus in der Mitte
        robot.drive(FAHR_GESCHWINDIGKEIT, 0)
        
    # Kurze Pause für CPU (10 ms)
    wait(10)