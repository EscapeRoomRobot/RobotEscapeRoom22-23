"""
    File Created By: Liang Lu 
    File Created On: Mar. 21, 2023 
    Description: 
        this files is just used for all kinds of testings
"""

# import built-in libraries
import keyboard
from time import sleep
import paho.mqtt.client as mqtt

# --- Global Variables ---
pi_ip_address = 'mqtt.eclipseprojects.io'
client = mqtt.Client(client_id="robot_control", clean_session=True)
servo = ""
puzzle = 1
duty = 2.5  # camera home position
enable_scan = False
enable_light = False
enable_blacklight = False
enable_move = False
# --- Global Variables Ends ---


# --- MQTT Setup ---
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


def on_message(client, userdata, msg):
    global enable_move
    print("on_message | topic: "+msg.topic +
          " \tmsg: "+str(msg.payload.decode("utf-8")))
    # enable arm if puzzle 3 is completed.
    # if (msg.topic == "website/status"):
    #     if msg.payload.decode("utf-8") == "puzzle 3 completed.":
    #         rmov.enable_arm()
    if (msg.topic == "robot/function"):
        if msg.payload.decode("utf-8") == "enable move":
            enable_move = True
        elif msg.payload.decode("utf-8") == "disable move":
            enable_move = False


def mqtt_setup() -> mqtt:
    client.connect(pi_ip_address)
    client.on_message = on_message
    client.subscribe("robot/function")
    client.subscribe("website/status")
    client.loop_start()

# --- MQTT Setup Ends ---


# --- Functions ---
def move_servo():  # FUNCION to move servo (for camera) up and down
    if (keyboard.is_pressed("w")):      # move servo up
        print("moving camera up")
        sleep(0.2)
    elif (keyboard.is_pressed("s")):    # move servo down
        print("moving camera down")
        sleep(0.2)
    else:                               # stop servo from possible vibration
        pass


def move_robot():  # FUNCIOM to control robot movement (wheels)
    if (keyboard.is_pressed("up")):         # move robot forward
        print("moving robot forward")
        sleep(0.2)
    elif (keyboard.is_pressed("down")):     # move robot backward
        print("moving robot backward")
        sleep(0.2)
    elif (keyboard.is_pressed("left")):     # turn robot left
        print("moving robot left")
        sleep(0.2)
    elif (keyboard.is_pressed("right")):    # turn robot right
        print("moving robot right")
        sleep(0.2)
    else:                                   # stop the robot
        pass


def move_arm():
    pass


def robot_func():
    global enable_scan, enable_light, enable_blacklight
    if (keyboard.is_pressed("q") and not enable_scan):          # enable scanning
        client.publish("robot/function", payload="enable scan")
        enable_scan = True
        sleep(0.2)
    elif (keyboard.is_pressed("q") and enable_scan):            # disable scanning
        client.publish("robot/function", payload="disable scan")
        enable_scan = False
        sleep(0.2)
    elif (keyboard.is_pressed("l") and not enable_light):       # enable light
        client.publish("robot/function", payload="enable light")
        enable_light = True
        sleep(0.2)
    elif (keyboard.is_pressed("l") and enable_light):           # disable light
        client.publish("robot/function", payload="disable light")
        enable_light = False
        sleep(0.2)
    elif (keyboard.is_pressed("b") and not enable_blacklight):  # enable blacklight
        client.publish("robot/function", payload="enable blacklight")
        enable_blacklight = True
        sleep(0.2)
    elif (keyboard.is_pressed("b") and enable_blacklight):      # disable blacklight
        client.publish("robot/function", payload="disable blacklight")
        enable_blacklight = False
        sleep(0.2)


def puzzle_wizard():
    global puzzle
    if (keyboard.is_pressed("1")):
        puzzle = 1
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("2")):
        puzzle = 2
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("3")):
        puzzle = 3
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("4")):
        puzzle = 4
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)
    elif (keyboard.is_pressed("5")):
        puzzle = 5
        client.publish("robot/puzzle", payload=str(puzzle))
        sleep(0.2)

# --- Functions Ends ---


def setup():
    # MQTT SET UP
    mqtt_setup()
    sleep(1)


def loop():
    if enable_move:
        move_servo()
        move_robot()
        robot_func()
    # puzzle_wizard()
    move_arm()


def destroy():
    print("disconnecting mqtt...")
    client.disconnect()


if __name__ == '__main__':     # Program start from here
    setup()
    while (1):
        try:
            loop()
            if (keyboard.is_pressed("esc")):
                client.publish("website/status", payload="escape")
                sleep(0.5)
                print("exiting...")
                break
        except KeyboardInterrupt:
            destroy()
