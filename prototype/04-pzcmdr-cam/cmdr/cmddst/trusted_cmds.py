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

}
