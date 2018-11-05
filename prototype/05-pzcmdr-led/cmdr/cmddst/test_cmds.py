commands = {
        "wakeup_labpcs": compile("print('Hello from Python code')", '<string>', 'exec'),

        "shutdown_labpcs": compile(
"""
import subprocess
p = subprocess.Popen('bash -c "echo Hello from bash"', shell=True)
""", '<string>', 'exec'),
        
        "toggle_volumio": compile(
"""
import urllib.request
urllib.request.urlopen('http://192.168.211.103/api/v1/commands/?cmd=toggle')
""", '<string>', 'exec')

}
