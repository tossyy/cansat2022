from machine import Machine

print("Machine setting up...")
ma = Machine()
print("Set up finished")

try:
    ma.remember_gps()
except UnicodeDecodeError:
    ma.remember_gps()
    
ma.close()