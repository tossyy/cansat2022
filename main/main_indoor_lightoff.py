from machine import Machine_indoor_lightoff


print("Machine setting up...")
ma = Machine_indoor_lightoff()
print("Set up finished")

print("Mision start")
ma.run()
print("Mission complete")