import sublime, sublime_plugin
import re

class EzMotionCommand(sublime_plugin.TextCommand):

	tags = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

	def run(self, edit, forward = False, line = False):

		self.targets = [];
		self.faded = [];
		self.in_selection = False
		self.in_word = False

		self.forward = forward
		self.line = line

		self.edit = edit
		self.window = self.view.window()

		self.find_targets()
		self.make_bookmarks()
		self.mark_targets()
		self.window.show_input_panel("EzMotion:", "", self.jump_to_target, None, self.unmark_targets)


	def jump_to_target(self, target):
		"""	Gets called after successful user input @ input panel """

		try:
			i = self.tags.index(target)
		except ValueError:
			self.unmark_targets()
			return

		self.unmark_targets()

		edit = self.view.begin_edit()
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(self.bookmarked[i].a, self.bookmarked[i].a))
		self.view.end_edit(edit)

		if ((i == len(self.tags) - 1) and (len(self.targets))):
			self.view.run_command("ez_motion", { "forward": self.forward })


	def make_bookmarks(self):
		""" Creates a list of bookmarks from targets, excess is left in place """

		self.bookmarked = []
		for i in range(0, len(self.targets)):
			if (i <= len(self.tags) - 1):
				self.bookmarked.append(self.targets.pop(0))


	def mark_targets(self):
		""" Highlights target letters and fades the rest """

		for i, r in enumerate(self.bookmarked):
			self.view.replace(self.edit, r, self.tags[i])

		for r in (self.targets):
			self.view.replace(self.edit, r, self.tags[-1])

		self.view.add_regions('ez_motion_target', self.bookmarked + self.targets, 'ezmotion.bookmark')
		self.view.add_regions('ez_motion_fade', self.faded, 'ezmotion.fade')


	def unmark_targets(self):
		""" Remove target marks """

		self.view.erase_regions('ez_motion_target')
		self.view.erase_regions('ez_motion_fade')
		self.view.end_edit(self.edit)
		self.window.run_command("undo")


	def find_targets(self):
		""" Find all possible motion targets and return them as a list of sublime.Region objects """

		self.where_am_i()

		text = self.text_fragment()

		for match in re.finditer(r'\w+', text):
			r_start = match.start() + self.start
			r_end = match.end() + self.start
			self.targets.append(sublime.Region(r_start, r_start+1))
			self.faded.append(sublime.Region(r_start+1,r_end))

		if not self.forward:
			self.targets.reverse()
			self.faded.reverse()

		if self.in_word:
			self.targets.pop(0)
			self.faded.pop(0)


	def where_am_i(self):
		""" Set the position coords and flags for selection and being in word """

		sel = self.view.sel()[0]
		self.start = sel.a
		self.end = sel.b

		if (self.start != self.end):
			self.in_selection = True

		if self.forward and re.match(r'\w', self.view.substr(self.start)) != None:
			self.in_word = True
		elif not self.forward and re.match(r'\w', self.view.substr(self.start-1)) != None:
			self.in_word = True

		region = self.view.visible_region()

		if (self.forward):
			if (self.start < region.a):
				self.start = region.a
			self.end = region.b

		else:
			if (self.end > region.b):
				self.end = region.b
			self.start = region.a


	def text_fragment(self):
		""" Determine the region we will use """

		return self.view.substr(sublime.Region(self.start, self.end))
