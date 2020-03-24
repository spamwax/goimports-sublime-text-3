"""
    Sublime Text 3 plugin to update list of packages imported
    in a Go (golang) source file (scope: source.go) using 'goimports'
    (http://github.com/bradfitz/goimports)

    Author: Hamid Ghadyani
    URL: https://github.com/spamwax/goimports-sublime-text-3
"""

import sublime
import sublime_plugin
import os
import subprocess
import codecs
import tempfile

PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = "GoImports.sublime-settings"
SETTINGS_FILE = "GoImports.sublime-settings"


def plugin_loaded():
    global s
    s = sublime.load_settings(SETTINGS_FILE)


class GoImportsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GoimportsrunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global s
        # check the scope and run only if view is a source.go
        scope = self.view.scope_name(0).split(' ')
        go_scope = False
        for _v in scope:
            if "source.go" in _v:
                go_scope = True
                break
        if not go_scope:
            return

        # Get the path to goimports binary.
        # you can install using:
        # $ go get -u golang.org/x/tools/cmd/goimports
        goimports_cmd = s.get("goimports_bin")

        # Save current text into a buffer that we can pass as stdin to goimports
        buf = buffer_text(self.view)

        try:
            # Run the 'goimports' command
            cur_dir = os.path.dirname(self.view.file_name())
            r = subprocess.Popen(goimports_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                                 cwd=cur_dir, stderr=subprocess.PIPE).communicate(input=buf)

            if len(r[1]) != 0:
                raise GoImportsException(r[1])

            newtext = r[0].decode("utf-8")
            if self.view.settings().get("ensure_newline_at_eof_on_save"):
                if not newtext.endswith("\n"):
                    newtext += "\n"

            # replace the content of the whole file
            selection = sublime.Region(0, self.view.size())
            self.view.replace(edit, selection, newtext)

        except Exception:
            import sys
            exc = sys.exc_info()[1]
            sublime.status_message(str(exc))


class OpenGoimportsSublimeSettings(sublime_plugin.TextCommand):
    """docstring for OpenGoimportsSublimeSettings"""
    def run(self, edit):
        open_goimports_sublime_settings(self.view.window())


class Goimportsrun(sublime_plugin.EventListener):
    """Will be executed just before saving"""
    def on_pre_save(self, view):
        if s.get("goimports_enabled",
                 view.settings().get("goimports_enabled", True)):
            view.run_command("goimportsrun")

def buffer_text(view):
    file_text = sublime.Region(0, view.size())
    return view.substr(file_text).encode('utf-8')

def open_goimports_sublime_settings(window):
    fn = os.path.join(PLUGIN_FOLDER, SETTINGS_FILE)
    window.open_file(fn)
