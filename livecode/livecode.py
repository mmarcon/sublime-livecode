import sublime, sublime_plugin
from websocket import create_connection
import thread
import time
import multiprocessing

#view.run_command("livecode",{"execute":"on"})


class LivecodeCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.ws = None
        self.view = view
        self.running = False
        self.buffer = None
        self.queue = multiprocessing.Queue()
        self.wshandler = None

    def run(self, edit, execute=None):
        self.choose(execute, edit)

    def choose(self, command, edit):
        if command == "on":
            self.turn_on(edit)
        elif command == "off":
            self.turn_off(edit)

    def turn_on(self, edit):

        def wshandler(q):
            ws = create_connection("ws://localhost:8000")
            ws.settimeout(800)
            while True:
                print "Sending"
                b = q.get(True, None)
                ws.send(b)

        if self.running == False:
            self.running = True
            thread.start_new_thread(lambda: self.getbuffer(edit), ())
            self.wshandler = multiprocessing.Process(target=wshandler, args=(self.queue,))
            self.wshandler.start()

    def getbuffer(self, edit):
        def get_buffer_internal(*args):
            print "Getting Buffer"
            view = sublime.active_window().active_view()
            self.queue.put(view.substr(sublime.Region(0, view.size())))
        
        while self.running:
            print "Other LOOP"
            sublime.set_timeout(get_buffer_internal , 1)
            time.sleep(3)

    def turn_off(self, edit):
        self.running = False
        if self.wshandler.is_alive():
            self.wshandler.terminate()
        print "Off"
