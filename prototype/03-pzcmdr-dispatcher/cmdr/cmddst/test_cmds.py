commands = {
        "wakeup_labpcs": compile("print('Hello from Python code')", '<string>', 'exec'),

        "shutdown_labpcs": compile(
"""
import subprocess
p = subprocess.Popen('bash -c "echo Hello from bash"', shell=True)
""", '<string>', 'exec'),

}
