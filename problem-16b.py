import math

def hex2bits(s):
    return ''.join(["{0:04b}".format(int(ch, base = 16)) for ch in s])

class Parser:
    def __init__(self, s):
        self.bits = hex2bits(s)

    def pop_bits(self, n):
        head, self.bits = self.bits[0:n], self.bits[n:]
        return head

    def pop_int(self, n):
        return int(self.pop_bits(n), base = 2)

    def parse(self):
        start_len = len(self.bits)

        version = self.pop_int(3)
        id = self.pop_int(3)
        if id == 4:
            s = ""
            stop = False
            while not stop:
                stop = (self.pop_int(1) == 0)
                s += self.pop_bits(4)
            return (version, id, start_len - len(self.bits), int(s, base = 2))
        
        mode = self.pop_int(1)
        sub_packets = []
        if mode == 0:
            pending_len = self.pop_int(15)
            while pending_len > 0:
                sub_packet = self.parse()
                sub_packets.append(sub_packet)
                pending_len -= sub_packet[2]
        else:
            pending_num = self.pop_int(11)
            while pending_num > 0:
                sub_packets.append(self.parse())
                pending_num -= 1
        return (version, id, start_len - len(self.bits), sub_packets)

def evaluate(packet):
    id = packet[1]
    if id == 4:
        return packet[3]

    sub_values = [evaluate(p) for p in packet[3]]
    if id == 0:
        return sum(sub_values)
    if id == 1:
        return math.prod(sub_values)
    if id == 2:
        return min(sub_values)
    if id == 3:
        return max(sub_values)
    assert(len(sub_values) == 2)
    if id == 5:
        return 1 if sub_values[0] > sub_values[1] else 0
    if id == 6:
        return 1 if sub_values[0] < sub_values[1] else 0
    if id == 7:
        return 1 if sub_values[0] == sub_values[1] else 0

with open("input-16.txt") as fp:
    for line in fp:
        line = line.strip()
        parser = Parser(line)
        packet = parser.parse()
        print(packet, evaluate(packet))
