import sublime, sublime_plugin
import re

class EzMotionCommand(sublime_plugin.TextCommand):

	tags = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

	def run(self, edit, forward = False, line = False, select = False, next = False):

		self.targets = [];
		self.faded = [];
		self.select = select
		self.next = next

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

		self.unmark_targets()
		edit = self.view.begin_edit()

		# if it's the nth run we don't want to clear selections
		if not self.next:
			self.view.sel().clear()

		for letter in target:
			try:
				i = self.tags.index(letter)
				if not self.select:
					self.view.sel().add(sublime.Region(self.bookmarked[i].a, self.bookmarked[i].a))
				else:
					self.view.sel().add(sublime.Region(self.sel.a, self.bookmarked[i].a))

			except ValueError:
				self.unmark_targets()
				return

		self.view.end_edit(edit)

		if ((i == len(self.tags) - 1) and (len(self.targets))):
			# if user has selected targets besides 'Z' or is in selection
			if len(target) > 1 or self.select:
				self.next = True
			self.view.run_command("ez_motion", { "forward": self.forward, "next": self.next, "select": self.select })


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

		if self.in_word():
			self.targets.pop(0)
			self.faded.pop(0)


	def where_am_i(self):
		""" Set the position coords """

		# on nth run our start should be relative to last caret/selection
		self.sel = self.view.sel()[-1] if self.next else self.view.sel()[0]

		self.start = self.sel.a
		self.end = self.sel.b

		if self.select and self.forward:
			# on nth run within selection, we want to start marking from end
			self.start = self.end

		region = self.view.visible_region()

		# we rely on visible region if cursor/selection is somewhere else
		if (self.forward):
			if (self.start < region.a):
				self.start = region.a
			self.end = region.b

		else:
			if (self.end > region.b):
				self.end = region.b
			self.start = region.a


	def in_word(self):
		""" Set a flag if caret is in or near word """

		if self.forward and re.match(r'\w', self.view.substr(self.start)) != None:
			return True
		elif not self.forward and re.match(r'\w', self.view.substr(self.start-1)) != None:
			return True

		return False


	def text_fragment(self):
		""" Returns text fragment we will be working with """

		return self.view.substr(sublime.Region(self.start, self.end))