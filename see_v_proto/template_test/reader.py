import re
import copy

BASE_ELEMENT = 1001
VAR_ELEMENT = 1002
COMPOSITE_ELEMENT = 1003
SECTION_ELEMENT = 1004
CV_ELEMENT = 1005

class BaseElement():

	def __init__(self, value):
		self.value = value
		self._element_type = BASE_ELEMENT

	def compile_template(self):
		return value

	def is_empty(self):
		return len(self.value) == 0

	def find_variables(self, index_offset = 0):
		working_value = str(self.value)
		new_parts = []
		variables = {}

		regex_pattern = r'(.*?)<%(.*?)%>(.*)'

		matched_obj = re.match(regex_pattern, working_value, re.I|re.S)
		while len(working_value) > 0 and not matched_obj == None:
			foreword = BaseElement(matched_obj.group(1))
			if not foreword.is_empty():
				new_parts.append(foreword)

			variable_name = matched_obj.group(2).strip().lower()
			variables[variable_name] = len(new_parts) + index_offset
			new_parts.append(VariableElement(value = None, identifier = variable_name))

			working_value = matched_obj.group(3)
			matched_obj = re.match(regex_pattern, working_value, re.I|re.S)

		if len(working_value) > 0:
			new_parts.append(BaseElement(working_value))

		return new_parts, variables

	def __repr__(self):
		return self.value


class VariableElement(BaseElement):

	def __init__(self, value, identifier):
		BaseElement.__init__(self, value)
		self.identifier = identifier
		self._element_type = VAR_ELEMENT



class CompositeElement(BaseElement):

	def __init__(self, value):
		BaseElement.__init__(self, value)
		self.sub_parts = []
		self.variables = {}
		self._element_type = COMPOSITE_ELEMENT

	def interpret_template(self):
		self._create_variables()

	def _create_variables(self):
		self.sub_parts, self.variables = self.find_variables()
		self.value = ""

	def compile_template(self):
		pass

	def is_empty(self):
		return len(self.sub_parts) == 0

	def find_variable_at(self, position):
		variable_name = "[No Variable Found]"
		for x in self.variables:
			if self.variables[x] == position:
				variable_name = "[ " + x +" ]"
		return variable_name

	def set_variable(self, variable_name, value):
		print self.variables
		self.sub_parts[self.variables[variable_name]].value = value

	def __repr__(self):
		return_string = ""
		for i in range(0, len(self.sub_parts)):
			part = self.sub_parts[i]
			if part._element_type == VAR_ELEMENT:
				if part.value == None:
					return_string += "[" + part.identifier + "]"
				else:
					return_string += part.value
			else:
				return_string += str(part)

		return return_string


class SectionElement(CompositeElement):

	

	def __init__(self, details, value):
		CompositeElement.__init__(self, value)
		self.name = details #Could make details contain all config parameters
		self._element_type = SECTION_ELEMENT
		self.entry_templates = []
		self.entry_counter = 0

		self.entries = []


	def interpret_template(self):
		self._create_entries()
		self._create_variables()

	def _create_variables(self):
		#print self.sub_parts
		for i in range(0, len(self.sub_parts)):
			part = self.sub_parts[i]
			new_parts, new_variables = part.find_variables(index_offset = i)
			if len(new_parts) > 1:
				self.sub_parts[i:i+1] = new_parts
				self.variables.update(new_variables)


	def _create_entries(self):
		regex_pattern = r'(.*?)<%\s?entry:(.*?):start\s?%>(.*?)<%\s?entry:.*?:end\s?%>(.*)'

		matched_obj = re.match(regex_pattern, self.value, re.I|re.S)
		while len(self.value) > 0 and not matched_obj == None:
			foreword = BaseElement(matched_obj.group(1))
			if not foreword.is_empty():
				self.sub_parts.append(foreword)

			entry_number = matched_obj.group(2)
			entry_content = matched_obj.group(3)
			new_entry = CompositeElement(value = entry_content)
			new_entry.interpret_template()
			self.sub_parts.append(new_entry)
			self.entry_templates.append(new_entry)

			self.value = matched_obj.group(4)
			matched_obj = re.match(regex_pattern, self.value, re.I|re.S)


	def create_next_entry(self, add_to_entries = True):
		return_entry = copy.deepcopy(self.entry_templates[self.entry_counter])
		self.entry_counter = (self.entry_counter + 1)%len(self.entry_templates)

		if add_to_entries:
			self.entries.append(return_entry)

		return return_entry

	def compile_template(self):
		pass


class CVTemplate(CompositeElement):

	def __init__(self, value):
		CompositeElement.__init__(self, value)
		self._element_type = CV_ELEMENT

	def interpret_template(self):
		self._create_sections()
		self._create_variables()

	def _create_sections(self):
		regex_pattern = r'(.*?)<%\s?section:(.*?):start\s?%>(.*?)<%\s?section:.*?:end\s?%>(.*)'

		matched_obj = re.match(regex_pattern, self.value, re.I|re.S)
		while len(self.value) > 0:
			foreword = BaseElement(matched_obj.group(1))
			if not foreword.is_empty():
				self.sub_parts.append(foreword)

			section_name = matched_obj.group(2)
			section_content = matched_obj.group(3)
			new_section = SectionElement(value = section_content, details = section_name)
			new_section.interpret_template()
			self.sub_parts.append(new_section)

			self.value = matched_obj.group(4)
			matched_obj = re.match(regex_pattern, self.value, re.I|re.S)


	def _create_variables(self):
		#print self.sub_parts
		for i in range(0, len(self.sub_parts)):
			part = self.sub_parts[i]
			new_parts, new_variables = part.find_variables(index_offset = i)
			if len(new_parts) > 1:
				self.sub_parts[i:i+1] = new_parts
				self.variables.update(new_variables)

	def get_section(self, section_name):
		section_name = section_name.lower()
		for element in self.sub_parts:
			if element._element_type == SECTION_ELEMENT:
				if element.name == section_name:
					return element

		return None

	def compile_template(self):

		pass


class TemplateReader():

	def __init__(self):
		pass

	def read_template(self, template_file):

		template_text = open(template_file).read()
		template = CVTemplate(template_text)
		template.interpret_template()
		template.set_variable("name", "Kieran")
		section = template.get_section("education")
		section.set_variable("title", "Education")
		entry1 = section.create_next_entry()
		entry1.set_variable("institute", "Wits")
		entry1.set_variable("start_date", "2008")
		entry1.set_variable("content", "Bsc Physics")


		print template