#!/usr/bin/python3

import argparse

def main():
# -> None
# prints the manufacturers for all the mac addresses in the file

	parser = parser_setup()

	args = vars(parser.parse_args())
	venders_f = args['vendors']
	sample_f = args['sample']
	log_f = args['log']
	delim = args['delimiter']

	mac_lookup = get_mac_lookup(venders_f)
	samples = get_sample_macs(sample_f)

	hits = 0
	misses = 0
	all_found = []
	all_missed = []

	log = open(log_f, 'w')

	for sample in samples:
		found = False
		for mac in mac_lookup:
			if sample[:len(mac[0])] == mac[0]:
				#print(sample + ": " + str(mac[1]))
				log.write(sample + delim + str(mac[1]) + '\n')
				found = True
				hits += 1
				all_found.append(sample)
		if not found:
			#print(sample + ": NOT FOUND")	
			log.write(sample + delim + 'NOT FOUND\n')
			misses += 1
			all_missed.append(sample)

	log.close()
	print('\nHits: ' + str(hits) + ' Misses: ' + str(misses))
	
#	print('\nSORTED MISSED: ')
#	for miss in sorted(all_missed):
#		print(miss)

	return None

def parser_setup():
# -> ArgumentParser
# sets up a command line parser.
	p = argparse.ArgumentParser()
	p.add_argument('vendors', help='File containing the MAC address prefixes of common vendors.')
	p.add_argument('sample', help='File containing a sample of MAC addresses.')
	p.add_argument('log', help='File to output the results.')
	p.add_argument('-d', '--delimiter', default=',', help='Delimiter for the file, default = \',\'')

	return p

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

def get_sample_macs(sample):
# File -> list
# returns a list of sample MAC address
	samples = []
	sample_file = open(sample, 'r')
	for line in iter(sample_file.readline, ''):
		addr = sample_sanatize(line)
		samples.append(addr)
	sample_file.close()
	return samples

def sample_sanatize(addr):
# str -> str
# remove newline and make caps
	return addr[:-1].upper()


main()
