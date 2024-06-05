from Characters.Shotgun import Shotgun

shotgun = Shotgun()
print(shotgun.get_rounds())
shotgun.add_rounds(1)

print(shotgun.get_next_shot())