from StringIO import StringIO
import logging

stream = StringIO()
handler = logging.StreamHandler(stream)
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(handler)

logging.info("test")
handler.flush()
val = stream.getvalue()

print val