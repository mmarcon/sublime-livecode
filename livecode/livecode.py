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
        self.buffer = None

    def run(self, edit, execute=None):
        self.choose(execute, edit)

    def choose(self, command, edit):
        if command == "on":
            self.turn_on(edit)
        elif command == "off":
            self.turn_off(edit)

    def turn_on(self, edit):
        if self.running == False:
            self.ws = create_connection("ws://localhost:8000")
            self.ws.settimeout(800)
            self.running = True
            thread.start_new_thread(lambda: self.getbuffer(edit), ())
            thread.start_new_thread(lambda: self.send(edit), ())

    def getbuffer(self, edit):
        print "*** ***"
        def get_buffer_internal(*args):
            print "Getting Buffer"
            view = sublime.active_window().active_view()
            self.buffer = view.substr(sublime.Region(0, view.size()));
        
        while self.running and self.ws.connected:
            print "Other LOOP"
            sublime.set_timeout(get_buffer_internal , 1)
            time.sleep(6)

    def send(self, edit):
        while self.running and self.ws.connected:
            try :
                print "LOOP"
                if self.buffer != None:
                    print "Sending buffer content..."
                    self.ws.send(self.buffer)
                    print "Sent"
            except Exception, e:
                print "Uhmmm... something wrong happened here..."
                self.turn_off(edit)
            time.sleep(5)

    def turn_off(self, edit):
        self.running = False
        self.ws.close()
        time.sleep(1)
        self.ws = None
        print "Off"
