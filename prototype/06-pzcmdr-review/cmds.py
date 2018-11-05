commands = {
        "wakeup_labpcs": compile(
"""
import subprocess 
p = subprocess.Popen('ssh root@10.116.116.1 dcs -nl Wake-on-LAN', shell=True)
""", '<string>', 'exec'),

        "shutdown_labpcs": compile(
"""
import subprocess
p = subprocess.Popen('ssh root@10.116.116.1 dcs -nl shutdown', shell=True)
""", '<string>', 'exec'),

        "toggle_volumio": compile(
"""
import urllib.request
urllib.request.urlopen('http://192.168.211.103/api/v1/commands/?cmd=toggle')
""", '<string>', 'exec'),

        "test_python_print": compile("print('Hello from Python code')", '<string>', 'exec'),

        "test_shell_print": compile(
"""
import subprocess
p = subprocess.Popen('bash -c "echo Hello from bash"', shell=True)
""", '<string>', 'exec'),
}
