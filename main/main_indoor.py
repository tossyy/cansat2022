from machine_indoor import Machine_indoor


print("Machine setting up...")
ma = Machine_indoor()
print("Set up finished")

print("Mision start")
ma.run()
print("Mission complete")