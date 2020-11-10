import re


"""
 * Library classes loader
"""
class Loader(object):

	"""
	 * Find and include required class file
	 * @param string class_name
	 * @return boolean
	"""
	@staticmethod
	def loader(class_name: str):

		if (re.search('/^' + __NAMESPACE__.replace('\\', '\\\\') + '\\\/', class_name)):
			filePath = dirname(__FILE__) + DIRECTORY_SEPARATOR + class_name.replace(array(__NAMESPACE__ + '\\', '\\'), array('', DIRECTORY_SEPARATOR)) + '.php'
			if is_file(filePath) and is_readable(filePath):
				require_once filePath
				return True


spl_autoload_register('\Mypos\IPC\Loader.loader')
