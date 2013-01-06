import sublime, sublime_plugin
import re

class EzMotionCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward = False):
        self.forward = forward
        self.edit = edit
        self.window = self.view.window()
        self.tags = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.targets = self.find_targets()
        self.make_bookmarks()
        self.mark_targets()
        self.window.show_input_panel("EzMotion:", "", self.jump_to_target, None, self.unmark_targets)

    def jump_to_target(self, target):
        try:
            i = self.tags.index(target)
        except ValueError:
            self.unmark_targets()
            return

        self.unmark_targets()

        for k in range(0, i + 1):
            self.view.run_command("move", { "extend": False, "word_begin": True, "punct_begin": False, "forward": self.forward, "by": "stops" })

        if ((i == len(self.tags) - 1) and (len(self.targets))):
            self.view.run_command("ez_motion", { "forward": self.forward })

    def make_bookmarks(self):
        self.bookmarked = []
        print self.targets
        for i in range(0, len(self.targets)):
            if (i <= len(self.tags) - 1):
                self.bookmarked.append(self.targets.pop(0))

    def mark_targets(self):
        for i, r in enumerate(self.bookmarked):
            self.view.replace(self.edit, r, self.tags[i])

        print self.targets
        for r in (self.targets):
            self.view.replace(self.edit, r, self.tags[-1])

        self.view.add_regions('ez_motion', self.bookmarked + self.targets, 'comment')

    def unmark_targets(self):
        """ Remove target marks """
        self.view.erase_regions('ez_motion')
        self.view.end_edit(self.edit)
        self.window.run_command("undo")

    def find_targets(self):
        """ Find all possible motion targets and return them as a list of sublime.Region objects """

        self.start, self.end = self.get_start_end()

        text = self.text_fragment()
        matching_regions = []

        for match in re.finditer(r'\w+', text):
            pt = match.start() + self.start
            matching_regions.append(sublime.Region(pt, pt+1))

        if not self.forward:
            matching_regions.reverse()

        return matching_regions

    def get_start_end(self):
        """ Set the position coords """

        region = self.view.visible_region()

        if (self.forward):
            self.view.run_command("move", { "extend": False, "word_begin": True, "punct_begin": False, "forward": True, "by": "stops" })
            start = self.view.sel()[0].a
            if (start < region.a):
                start = region.a
            end = region.b

        else:
            end = self.view.sel()[0].a
            if (end > region.b):
                end = region.b
            start = region.a

        return (start, end)

    def text_fragment(self):
        """ Determine the region we will use """

        return self.view.substr(sublime.Region(self.start, self.end))
