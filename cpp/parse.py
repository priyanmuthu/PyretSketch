from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser

# Find the location of the xml generator (castxml or gccxml)
generator_path, generator_name = utils.find_xml_generator()
# Configure the xml generator
xml_generator_config = parser.xml_generator_configuration_t(
xml_generator_path=generator_path,
xml_generator=generator_name)
# The c++ file we want to parse
filename = "prog1.cpp"
# Parse the c++ file
decls = parser.parse([filename], xml_generator_config)
# Get access to the global namespace
print(decls)