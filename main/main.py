from machine import Machine

try:
    print("Machine setting up...")
    ma = Machine()
    print("Set up finished")

    print("Mision start")
    ma.run()
    print("Mission complete")
except Exception as e:
    print(e)
finally:
    ma.close()