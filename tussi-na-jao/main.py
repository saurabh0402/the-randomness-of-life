from pybooklid import LidSensor
from playsound3 import playsound

class Player():
    def __init__(self):
        self.playing = False
        self.sound = None

    def play(self, path):
        if self.playing:
            self.sound.stop()
        self.sound = playsound(path, block=False)
        self.playing = True

class Angle_handler():
    def __init__(self, player):
        self.player = player
        self.last_alert_angle = None

    def __call__(self, angle):
        print(f"Lid angle changed: {angle:.1f}°")
        self.player.play("./audio/please_dont_go.mp3")
        self.last_alert_angle = angle

if __name__ == "__main__":
    player = Player()
    handle_angle_change = Angle_handler(player)

    with LidSensor() as sensor:
        for angle in sensor.monitor(callback=handle_angle_change, interval=0.5):
            pass
