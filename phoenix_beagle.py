import sublime, sublime_plugin, os, re, glob, itertools, sys

class Phoenix(object):
    def __init__(self, file_path, patterns, folders):
        self.__file_path = file_path
        self.__patterns = patterns
        self.__root = self.__root(folders)
        self.__files = []
        self.__descriptions = []
        self.__build()

    def descriptions(self):
        return self.__descriptions

    def files(self):
        return self.__files

    def __build(self):
        files = set()

        file_path = self.__to_posixpath(self.__file_path)
        for regex, paths in list(self.__patterns.items()):
            match = re.compile(regex).match(file_path)
            if match:
                files.update(self.__files_for_paths(regex, match, paths))

        files = list(files)
        files.sort()

        self.__files = files
        self.__descriptions = [self.__file_without_root(file) for file in files]

    def __root(self, folders):
        for folder in folders:
            if self.__file_path.startswith(os.path.join(folder, "")):
                return folder

    def __files_for_paths(self, regex, match, paths):
        paths = [self.__replaced_path(match, path) for path in paths]

        files = [glob.glob(os.path.join(self.__root, path)) for path in paths]
        flattened = [self.__to_posixpath(path) for path in list(itertools.chain.from_iterable(files))]

        if self.__file_path in flattened:
            flattened.remove(unicode(self.__file_path))

        return flattened

    def __file_without_root(self, file):
        return os.path.basename(self.__root) + file[len(self.__root):]

    def __replaced_path(self, match, path):
        replaced_path = path
        for i, group in enumerate(match.groups()):
            replaced_path = replaced_path.replace("$%s" % (i + 1), group)
        return replaced_path

    def __to_posixpath(self, path):
        return re.sub("\\\\", "/", path)

class PhoenixBeagleCommand(sublime_plugin.WindowCommand):
    def run(self, index=None):
        active_file_path = self.__active_file_path()
        active_folders = sublime.active_window().folders()
        if not active_folders:
            active_folders = os.path.split(active_file_path)[0]
            sublime.error_message("SideBar is empty!")
        if active_file_path:
            if self.__patterns():
                self.__beagle = Phoenix(active_file_path, self.__patterns(), active_folders)
                self.window.show_quick_panel(self.__beagle.descriptions(), self.__open_file)
            else:
                self.__status_msg("Patterns are not loaded!")
        else:
            self.__status_msg("No open files")

    def __open_file(self, index):
        if index >= 0:
            self.window.open_file(self.__beagle.files()[index])
        else:
            self.__status_msg("No files found")

    def __patterns(self):
        return sublime.load_settings("PhoenixBeagle.sublime-settings").get('patterns')

    def __active_file_path(self):
        if self.window.active_view():
            file_path = self.window.active_view().file_name()

            if file_path and len(file_path) > 0:
                return file_path

    def __status_msg(self, message):
        sublime.status_message(message)
