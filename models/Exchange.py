class Exchange:

    properties = {}

    def setProperty(self, key, value):
        self.properties[key] = value

    def getProperty(self, key):
        return self.properties.get(key)

    def getAllProperties(self):
        return self.properties
