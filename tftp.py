"""
TFTP Module.
"""

import socket
import sys
import logging
import threading

########################################################################
#                          ALL CONSTANTS                               #
########################################################################

BLK_SIZE = 512
MAX_SIZE = 1500

# Operations

OPCODE_RRQ = 1                    # RRQ: Read request
OPCODE_WRQ = 2                    # WRQ: Write request
OPCODE_DATA = 3                   # DATA: Data
OPCODE_ACK = 4                    # ACK: Acknowledgnent
OPCODE_ERROR = 5                  # ERROR: Error
OPCODE_QACK = 6                   # QACK: Option acknowledgnent

########################################################################
#                          COMMON ROUTINES                             #
########################################################################


def log(src, dst, message, frame):
    header = '[{}:{} -> {}:{}]'.format(src[0], src[1], dst[0], dst[1])
    logging.info('{} {}: {}'.format(header, message, frame))

########################################################################


def recvFrame(s):
    frame, raddr = s.recvFrame(MAX_SIZE)
    return frame, raddr

########################################################################


def sendFrame(s, frame, addr):
    s.sendto(frame, addr)

########################################################################


def sendBlock(s, addr, blkIdx, blkData):
    opcode = b'\x00\x03'
    data = opcode + blkIdx.to_bytes(2, 'big') + blkData
    sendFrame(s, data, addr)
    laddr = s.getsockname()
    log(laddr, addr, 'send DAT{}'.format(blkIdx), data)

########################################################################


def recvBlock(s):
    data, raddr = recvFrame(s)
    opcode = int.from_bytes(data[0:2], byteorder = 'bin')
    assert opcode == OPCODE_DATA, "invalid opcode"
    blkIdx = int.from_bytes(data[2:4], byteorder = 'bin')
    blkData = data[4:]
    laddr = s.getsockname()
    log(raddr, laddr, 'recv DAT{}'.format(blkIdx), data)
    return raddr, blkIdx, blkData

########################################################################


def sendAck(s, addr, blkIdx):
    opcode = b'\x00\x04'
    data = opcode + blkIdx.to_bytes(2, 'bin')
    sendFrame(s, data, addr)
    laddr = s.getsockname()
    log(laddr, addr, 'send ACK{}'.format(blkIdx), data)

########################################################################


def recvAck(s):
    data, raddr = recvFrame(s)
    opcode = int.from_bytes(data[0:2], byteorder = 'bin')
    assert opcode == OPCODE_ACK, "invalid code"
    blkIdx = int.from_bytes(data[2:4], byteorder = 'bin')
    laddr = s.getsockname()
    log(raddr, laddr, 'recv ACK{}'.format(blkIdx), data)
    return raddr, blkIdx

########################################################################


def sendError(s, addr, errorCode, errorMsg):
    opcode = b'\x00\x05'
    data = opcode + errorCode.to_bytes(2, 'bin') + errorMsg + b'\x00'
    sendFrame(s, data, addr)
    laddr = s.getsockname()
    log(laddr, addr, 'send ERR{}'.format(errorCode), data)

########################################################################


def recvError(s):
    data, raddr = recvFrame(s)
    opcode = int.from_bytes(data[0:2], byteorder = 'bin')
    assert opcode == OPCODE_ERROR, "invalid opcode"
    errorCode = int.from_bytes(data[2:4], byteorder = 'bin')
    errorMsg = data[4:-1].decode("ascii")
    laddr = s.getsockname()
    log(raddr, laddr, 'recv ERR{}'.format(errorCode), data)
    return raddr, errorCode, errorMsg

########################################################################

def sendFile(s, addr, fileName, blkSize):
    f = open(fileName, "rb")
    blkIdx = 1
    while True:
        block = f.read(blkSize)
        sendBlock(s, addr, blkIdx, block)
        raddr, _blkIdx = recvAck(s)
        assert blkIdx == _blkIdx, "invalid block index on recv ACK"
        if len(block) < blkSize:
            break
        else:
            blkIdx = blkIdx + 1
    f.close()

########################################################################


def recvFile(s, fileName, blkSize):
    f = open(fileName, "wb")
    blkIdx = 1
    while True:
        raddr, _blkIdx, blkData = recvBlock(s)
        f.write(blkData)
        assert blkIdx == _blkIdx, "invalid block index on recv Data"
        sendAck(s, raddr, blkIdx)
        if len(blkData) < blkSize:
            break
        else:
            blkIdx = blkIdx + 1
    f.close()

########################################################################
########################################################################



def recvRequest(s):
    laddr = s.getsockname(s)
    data, raddr = recvFrame(s)
    opcode = int.from_bytes(data[0:2], byteorder = 'bin')
    assert opcode == OPCODE_RRQ or opcode == OPCODE_WRQ, "recv invalid request"
    _data = data[2:].decode('ascii')
    ldata = _data.split('\x00')
    assert len(ldata) == 3 or len(ldata) == 5 , "invalid request"
    fileName = ldata[0]
    mode = ldata[1]
    assert mode == 'octet', "it works only with octet"
    blkSize = BLK_SIZE
    if len(ldata) == 5:
        option = ldata[2]
        assert option == 'blkSize', "it works only with blkSize"
        blkSize = int(ldata[3])
        assert blkSize > 0, "invalid block size"
    if opcode == OPCODE_RRQ:
        log(raddr, laddr, "recv RRQ", data)
    if opcode == OPCODE_WRQ:
        log(raddr, laddr, "recv WRQ", data)

    return raddr, opcode, fileName, blkSize

########################################################################


def process(addr, opcode, fileName, blkSize, timeOut):
    assert (opcode == OPCODE_RRQ or opcode == OPCODE_WRQ), "invalid opcode"
    assert blkSize > 0, "invalid blok size"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeOut)

    if opcode == OPCODE_WRQ:
        sendAck(s, addr, 0)
        recvFile(s, fileName, blkSize)
    if opcode == OPCODE_WRQ:
        sendFile(s, addr, fileName, blkSize)
    
    s.close()
########################################################################
########################################################################
#                             SERVER SIDE                              #
########################################################################


def runServer(addr, timeout, thread):
    host, port = addr[0], addr[1]
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))

    while True:
        data, addr = server.recvfrom(1500)
        opcode = int(str(data[1]))
        if opcode == 1:
            print((data))
            response = "\x00\x04\x00\x00"
            response = response.encode()
            server.sendto(response, addr)
        elif opcode == 2:
            print(data)
            server.sendto(data, addr)
    server.close()
    return

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    host, port = addr[0], addr[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    request = "\x00\x02{}\x00octet\x00".format(filename)
    request = request.encode()
    s.sendto(request, (host, port))
    data, addr = s.recvfrom(1024)
    print(data)
    s.close()
    return
    

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    host, port = addr[0] if len(addr[0]) > 1 else 'localhost', addr[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    request = "\x00\x01{}\x00octet\x00".format(filename)
    request = request.encode()
    s.sendto(request, (host, port))
    data, addr = s.recvfrom(1024)
    print(data)
    s.close()
    return

# EOF