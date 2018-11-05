# The configuration file for defining commands.

# The command ID lookup table
# The key is the command ID.
# The value is the object that can be executed by exec(). In the sample, we demonstrate
# how to pre-compile the python statement for execution.
commands = {
        "toggle_volumio": compile(
"""
import urllib.request
urllib.request.urlopen('http://192.168.211.103/api/v1/commands/?cmd=toggle')
""", '<string>', 'exec'),

        #"test_python_print": "print('Hello from Python code')",
        "test_python_print": compile("print('Hello from Python code')", '<string>', 'exec'),

        "test_shell_print": compile(
"""
import subprocess
p = subprocess.Popen('bash -c "echo Hello from bash"', shell=True)
""", '<string>', 'exec'),
}
