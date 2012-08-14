import sublime, sublime_plugin
from websocket import create_connection
import thread
import time

#view.run_command("livecode",{"execute":"on"})

class LivecodeCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.ws = None
        self.view = view
        self.running = False

    def run(self, edit, execute = None):
        self.choose(execute, edit)
        
    def choose(self, command, edit):
        if command == "on":
            self.turn_on(edit)
        elif command == "off":
            self.turn_off(edit)

    def turn_on(self, edit):
        if self.running == False:
            self.ws = create_connection("ws://echo.websocket.org/")
            def run(*args):
                self.send(edit)
            thread.start_new_thread(run, ())

    def send(self, edit):
        self.running = True
        def sendbuffer(*args):
            self.ws.send(self.view.substr(sublime.Region(0,self.view.size())));
        while self.running:
            print "Sending 'Hello, World'..."
            sublime.set_timeout(sendbuffer, 1)
            
            print "Sent"
            print "Reeiving..."
            result =  self.ws.recv()
            print "Received '%s'" % result
            time.sleep(5)

    def turn_off(self, edit):
        self.running = False
        self.ws.close()
        self.ws = None
        print "Off"