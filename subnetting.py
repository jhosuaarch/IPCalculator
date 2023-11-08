import os

banner = """
\t\t-- IP Calculator ---
\t\t  made by @jhosua
"""

class JSpace:
	def __init__(self, **kwargs):
		self.data = kwargs.items()
		for key, value in self.data:
			setattr(self, key, value)
			
	def __str__(self):
		return f"data({', '.join([f'{key}={repr(value)}' for key, value in self.data])})"


class IPInfo:
	
	def __init__(self, ip, mask):
		self.ip = ip
		self.mask = mask
	
	@property
	def ip_class(self):
		start_ip = int(self.ip.split('.')[0])
		if 1 <= start_ip <= 126:
			return "A"
		elif 128 <= start_ip <= 191:
			return "B"
		elif 192 <= start_ip <= 223:
			return "C"
		elif 224 <= start_ip <= 239:
			return "D"
		elif 240 <= start_ip <= 255:
			return "E"
	
	@property
	def subnet(self):
		one_binary = []
		zero_binary = []
		data = self.mask.split('.')
		for i,value in enumerate(data, 0):
			if i != 0:
				for j in range(2):
					calculate = int(bin(int(value))[2:].zfill(8).count(str(j)))
					if j == 0:
						zero_binary.append(calculate)
					else:
						one_binary.append(calculate)
		
		total_subnet = 0
		host_subnet = 0
		
		if self.ip_class == "A":
			total_subnet = 2 ** sum(one_binary)
			host_subnet = 2 ** sum(zero_binary) - 2
		elif self.ip_class == "B":
			total_subnet = 2 ** sum(one_binary[1:])
			host_subnet = 2 ** sum(zero_binary[1:]) - 2
		elif self.ip_class == "C":
			total_subnet = 2 ** one_binary[2]
			host_subnet = 2 ** zero_binary[2] - 2
		
		# Blok Subnet
		blok = 256 - int(data[3])
			
		return JSpace(total=total_subnet,host=host_subnet, blok=blok)
	
	@property
	def network(self):
		n = []
		b = []
		ip = self.ip.split('.')
		mask_parts = self.mask.split('.')
		for i in range(4):
			if "/" in ip[i]:
				z = ip[i].replace("/", "")
			else:
				z = ip[i]
			n.append(str(int(z) & int(mask_parts[i])))
			
		subnet_mask = [str(255 - int(part)) for part in mask_parts]
		for i in range(4):
			b.append(str(int(n[i]) | int(subnet_mask[i])))
		
		address_broadcast = '.'.join(b)
		subnet_address = '.'.join(n)
		return JSpace(broadcast=address_broadcast,subnet_address=subnet_address)
		
		

while True:
	os.system("clear")
	
	print(banner)
	ip = input("\n\t[?] IP Address   : ")
	mask = input("\t[?] Mask Address : ")
	
	net = IPInfo(ip,mask)
	print(f"\n\t=> IP Class        : {net.ip_class}")
	print(f"\t=> Jumlah Subnet   : {net.subnet.total}")
	print(f"\t=> Host Per Subnet : {net.subnet.host}")
	print(f"\t=> Blok Subnet     : {net.subnet.blok}")
	print(f"\t=> Subnet Address  : {net.network.subnet_address}")
	print(f"\t=> Broadcast       : {net.network.broadcast}")
	
	input("\n\t[!] Tekan enter untuk melanjutkan ")
