class CourseModule:
	# Initialize a course module with validated title, content,
	# and completion status

	def __init__(self, title, content, completed):

		# Validate the module's attributes.
		if not isinstance(title, str) or not title.strip():
			raise ValueError("Module title cannot be empty.")

		if not isinstance(content, str) or not content.strip():
			raise ValueError("Module content cannot be empty.")

		if not isinstance(completed, bool):
			raise ValueError("Completion status must be True or False.")

		# Store the module's attributes as private.
		self.__title = title.strip()
		self.__content = content.strip()
		self.__completed = completed

	# Return the module attributes.
	def get_title(self):
		return self.__title

	def get_content(self):
		return self.__content

	def is_completed(self):
		return self.__completed

	# Update the module's completion status after validation.
	def update_progress(self, completed):
		if not isinstance(completed, bool):
			raise ValueError("Completion status must be True or False.")
		self.__completed = completed

	# Return the module information as a formatted string.
	def __str__(self):
		return (
			f"Title: {self.__title}\n"		
			f"Content: {self.__content}\n"
			f"Completed: {self.__completed}"
		)
	
# Demonstration
course_module = CourseModule(
	"Python Intermediate",
	"Object Oriented Programming",
	True
)

print(course_module)