import logging
import logging.config

# Set up logging
# Create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Create handlers
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
# Create formatters
basic_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
# Add formatters to handlers
stream_handler.setFormatter(basic_formatter)
# Add formatters to logger
logger.addHandler(stream_handler)