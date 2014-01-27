from imposm.parser import OSMParser

# simple class that handles the parsed OSM data.
class ATMCounter(object):
    atms = 0

    def atm_loc(self, ways):
        # callback method for ways
        for osmid, tags, refs in ways:
            if 'atm' in tags:
              self.atms += 1

# instantiate counter and parser and start parsing
counter = ATMCounter()
p = OSMParser(concurrency=1, ways_callback=counter.ways)
p.parse('sf-bay-area.osm')

# done
print counter.atms