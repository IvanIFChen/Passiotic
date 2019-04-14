#!/usr/bin/python3

class MACLookup():
	# an instance of this class can determine if a MAC Address is in a list of unacceptable vendors.

	def __init__(self, vendors_f, unacceptable):
		self.lookup = get_mac_lookup(vendors_f)
		self.unacceptable = unacceptable

	def reject(self, sample):
		sample = sample.upper() # ensure MAC Address is in caps
		for mac in self.lookup:
			if sample[:len(mac[0])] == mac[0]:
				vendor_info = mac[1]
				vendor_abbr = vendor_info[0] # check against the vendor abbreviation
				return vendor_abbr in self.unacceptable
		return False

def get_mac_lookup(vendors):
# File -> list
# returns a list of tuples of str MAC addresses and tuple manufacturers
	mac_lookup = []
	mac_file = open(vendors, 'r')
	for line in iter(mac_file.readline, ''):
		entry = line.split('\t')
		# Get the MAC address prefix
		mac = mac_sanatize(entry[0])
		# Get manufacturer and long verison (if there is one) and remove '\n'
		man_info = man_sanatize(entry[1:])
		# Add to dict
		mac_lookup.append((mac, man_info))
	mac_file.close()
	return mac_lookup


def mac_sanatize(mac):
# str -> str
# makes the MAC address all caps
	prefix = mac.upper()
	return prefix

def man_sanatize(man):
# tuple -> tuple
# removes the '\n' from the last entry in the tuple
	man[-1] = man[-1][:-1]
	return tuple(man)


#test = MACLookup('vendors.txt', [])
#print(test.reject('40:4e:36:1e:4f:84'))
