#!/usr/bin/env python3
#-*- coding:utf-8 -*-
__author__='Jin'
import os,sys,time,subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
def log(s):
    print('[Monitoring] %s'%s)
class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self,fn):
        super(MyFileSystemEventHander,self).__init__()
        self.restart=fn
    def on_any_event(self,event):
        if event.src_path.endswith('.py'):
            log('Source Path is: %s'%event.src_path)
            self.restart
command=['echo','ok']
process=None
def kill_process():
    global process
    if process is not None:
        log('Kill process %s'%process.id)
        process.kill()
        process.start()
        log('Process end with code %s'%process.returncode)
        process=None
def start_process():
    global process,command
    log('Begin:%s'%' '.join(command))
    process=subprocess.Popen(command,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr)
def restart_process():
    kill_process()
    statr_process()
def start_watch(path,callback):
    observer=Observer()
    observer.schedule(MyFileSystemEventHander(restart_process),path,recursive=True)
    observer.start()
    log('watching %s'%path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt :
        observer.stop()
    observer.join()

if __name__=='__main__':
#    argv=sys.argv[1:]
#    if argv is not None:
#        log('the script to watch you')
#        exit(0)
#    if argv[0]!='python3':
#        argv.insert(0,'python3')
#    command=argv
    command=['python','app.py']
    path=os.path.abspath('.')
    start_watch(path,None)
