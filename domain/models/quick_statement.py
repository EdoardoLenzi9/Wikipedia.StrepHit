# A value can be another item, a string, a time, a location, or a quantity, depending on the property type
# Each statement "triplet" can be followed by an unlimited number of "qualifiers pairs" of property TAB value.
# Each statement can be followed by an unlimited number of "source pairs" of source property TAB value
#   A source property is identical to the normal property but takes Sxx prefix
#   the meaning of a source property is "with reference ..."

#    Q340122 TAB Lpl TAB "Cyprian Kamil Norwid" Meaning: add Polish label "Cyprian Kamil Norwid" to Cyprian Norwid (Q340122)
class QuickStatement(object):
    item = ""
    property = ""
    value = ""
    qualifiers = []
    sources = []
    labels = []
    aliases = []
    descriptions = []
    sitelinks = []

    def __init__(self, item, property, value, qualifiers, sources, labels, aliases, descriptions, sitelinks):
        self.item = item
        self.property = property
        self.value = value
        self.qualifiers = qualifiers
        self.sources = sources
        self.labels = labels
        self.aliases = aliases
        self.descriptions = descriptions
        self.sitelinks = sitelinks

class Qualifier(object):
    property = ""
    value = ""

    def __init__(self, property, value):
        self.property = property
        self.value = value

class Source(object):
    source_property = ""
    value = ""

    def __init__(self, source_property, value):
        self.source_property = source_property
        self.value = value

class Command(object):
    command = ""
    content = ""

    def __init__(self, command, content):
        self.command = command
        self.content = content