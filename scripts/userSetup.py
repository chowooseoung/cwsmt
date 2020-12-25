from pymel import mayautils
from cwsmt.version import *

print " {:_^30}".format("")
print "|{: ^30}|".format(name)
print "| {: <10} {: <18}|".format("author", author)
print "| {: <10} {: <18}|".format("version", version)
print "|{:_^30}|".format("")

mayautils.executeDeferred("import cwsmt; cwsmt.initialize()")