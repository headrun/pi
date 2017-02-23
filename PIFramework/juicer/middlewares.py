import scrapy
import logging
import random
import netifaces
from netifaces import AF_INET 

round_robin_iplist = [ "eth0:0", "eth0:1", "eth0:2", "eth0:3", "eth0:4", "eth0:5", "eth0:6", "eth0:7", "eth0:8", "eth0:9", "eth0:10", "eth0:11", "eth0:12", "eth0:13", "eth0:14", "eth0:15", "eth0:16", "eth0:17", "eth0:18", "eth0:19", "eth0:20", "eth0:21", "eth0:22", "eth0:23", "eth0:24", "eth0:25", "eth0:26", "eth0:27", "eth0:28", "eth0:29", "eth0:30"]

#Here, we shall give list of ips in the below list variable. Instead of getting the computers IP, we shall check in net and get few public ips.
round_robin_ips = ['176.9.181.35', '176.9.181.40', '144.76.48.150', '144.76.48.148']

class InterfaceRoundRobinMiddleware(object):
    def process_request(self, request, spider):
        vir_itf_count = 30
        #round_robin_ip = netifaces.ifaddresses( 'eth0:%d'%(random.randrange(0,vir_itf_count) ) )[AF_INET][0]['addr']
        #round_robin_ip = netifaces.ifaddresses('wlan0')[AF_INET][0]['addr']
        round_robin_ip = random.choice(round_robin_ips)
        #request.meta["bindaddress"]= ("127.0.0.1",random.randrange(49152,65535))
        ip_port_tuple = ( round_robin_ip , 3279)#random.randrange(49152,65535) )
        request.meta["bindaddress"]= ip_port_tuple
        logging.warning("request bindaddress ip_tuple = ('%s','%s')"%ip_port_tuple)
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        return None
