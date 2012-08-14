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

    def run(self, edit, execute=None):
        self.choose(execute, edit)

    def choose(self, command, edit):
        if command == "on":
            self.turn_on(edit)
        elif command == "off":
            self.turn_off(edit)

    def turn_on(self, edit):
        if self.running == False:
            self.ws = create_connection("ws://echo.websocket.org/")
            thread.start_new_thread(lambda: self.send(edit), ())

    def send(self, edit):
        self.running = True

        def sendbuffer(*args):
            view = sublime.active_window().active_view()
            self.ws.send(view.substr(sublime.Region(0, view.size())))

        while self.running:
            print "Sending buffer content..."
            sublime.set_timeout(sendbuffer, 1)
            print "Sent"
            #result = self.ws.recv()
            #print "Received '%s'" % result
            time.sleep(5)

    def turn_off(self, edit):
        self.running = False
        self.ws.close()
        time.sleep(1)
        self.ws = None
        print "Off"
