import subprocess
def getCPUTemp():
        return call(["vcgencmd", "measure_temp"])[5:7]
def call(com):
        return subprocess.check_output(com).split("\n")[0]
def getVoltage():
        return call(["vcgencmd", "measure_volts"])[5:8]


print getCPUTemp(), " Grad"
print getVoltage(), " V"
