"""
    Sublime Text 3 plugin to update list of packages imported
    in a Go (golang) source file (scope: source.go) using 'goimports'
    (http://github.com/bradfitz/goimports)
"""

import sublime
import sublime_plugin
import os
import subprocess
import codecs
import tempfile

PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = "GoImports.sublime-settings"


def plugin_loaded():
    global s
    s = sublime.load_settings("GoImports.sublime-settings")


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
        # $ go get github.com/bradfitz/goimports
        goimports_cmd = s.get("goimports_bin")

        # Get formatting settings
        tabs_arg = " -tabs=false"
        if s.get("use_tabs", self.view.settings().get("use_tabs", False)):
            tabs_arg = tabs_arg.replace("false", "true")
        tabwidth_arg = " -tabwidth=4 "
        w = s.get("tab_width", self.view.settings().get("tab_width", 4))
        tabwidth_arg = tabwidth_arg.replace("4", str(w))

        # Save current text into a temp file
        tempPath = save_tmp(self.view)
        cmd = goimports_cmd + tabs_arg + tabwidth_arg + tempPath

        try:
            # Run the 'goimports' command
            r = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,
                                 stderr=subprocess.PIPE).communicate()

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


def save_tmp(view):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()
    tempPath = f.name
    print("Saving goimports buffer to: " + tempPath)

    bufferText = view.substr(sublime.Region(0, view.size()))
    f = codecs.open(tempPath, mode='w', encoding='utf-8')
    f.write(bufferText)
    f.close()
    return tempPath


def open_goimports_sublime_settings(window):
    fn = os.path.join(PLUGIN_FOLDER, SETTINGS_FILE)
    window.open_file(fn)
