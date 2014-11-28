import subprocess

def call(command):
	return subprocess.check_output(command).split("\n")[0][5:7]

print call(["vcgencmd"," measure_temp"])
