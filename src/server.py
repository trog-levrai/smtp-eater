import os, subprocess, tempfile

with tempfile.NamedTemporaryFile(delete = False) as f:
    f.write(b'default')
    f.close()
    cmd = os.environ.get('EDITOR', 'vi') + ' ' + f.name
    subprocess.call(cmd, shell=True)
