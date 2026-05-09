#!/usr/bin/env python3
import json, subprocess, time
prompt = 'Translate to Khmer (ខ្មែរ): There is a kind of silence'
proc = subprocess.Popen(
    ['/home/tali/.opencode/bin/opencode', 'run', '--model', 'opencode/nemotron-3-super-free'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd='/home/tali/tali-book'
)
out, err = proc.communicate(input=prompt.encode(), timeout=90)
print('OUTPUT:', out.decode()[:300])