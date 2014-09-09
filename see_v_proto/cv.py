class CVGroup:
	
	def __init__(self):
		self._name = ""
		self._cv_entries = []

		print "Created"

	def set_name(self, name):
		self._name = name

	def add_entry(self, new_entry):
		self._cv_entries.append(new_entry)

	def to_html(self):
		html_string = "<h1>" + self._name + "</h1>"
		for cv_entry in self._cv_entries:
			html_string += cv_entry.to_html()

		return html_string


class CVEntry:

	def __init__ (self):
		self._date = None
		self._content = ""
		self._tags = []
		print "Created"

	def add_tag (self, tag):
		self._tags.append(tag)

	def set_content (self, newContent):
		self._content = newContent

	def set_date (self, newDate):
		self._date = newDate

	def __str__(self):
		str_return = "Type: " + self._entry_type
		str_return += "\nTags: " + str(self._tags) 
		str_return += "\nContent: " + self._content
		str_return += "\nDate: " + str(self._date)
		return str_return

	def to_html(self):
		html_string = "<h2>" + str(self._date) + "</h2>"
		html_string += self._content + "<br>"
		return html_string