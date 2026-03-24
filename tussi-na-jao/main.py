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
        self.last_played = None
        self.angle = None

    def __call__(self, angle):
        print(f"Lid angle changed: {angle:.1f}°")

        if not self.angle:
            self.angle = max(0, angle - 10)
            return

        if self.angle - angle < 10:
            if self.angle < angle:
                self.angle = angle
                self.last_played = None
            return

        if angle < 60:
            if self.last_played == "go_away":
                return
            
            self.player.play("./audio/go_away.mp3")
            self.last_played = "go_away"
            return

        if angle < 90:
            if self.last_played == "please_dont_go":
                return
            
            self.player.play("./audio/please_dont_go.mp3")
            self.last_played = "please_dont_go"

        self.angle = angle

if __name__ == "__main__":
    player = Player()
    handle_angle_change = Angle_handler(player)

    with LidSensor() as sensor:
        for angle in sensor.monitor(callback=handle_angle_change, interval=1):
            pass
