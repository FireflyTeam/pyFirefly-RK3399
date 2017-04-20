#!/usr/bin/env python
"""
This is designed primarily for use with accessing /dev/mem on OMAP platforms.
It should work on other platforms and work to mmap() files rather then just
/dev/mem, but these use cases aren't well tested.

All file accesses are aligned to DevMem.word bytes, which is 4 bytes on ARM
platforms to avoid data abort faults when accessing peripheral registers.

References:
    http://wiki.python.org/moin/PythonSpeed/PerformanceTips
    http://www.python.org/dev/peps/pep-0008/

"""

import os
import mmap
import struct
import logging

""" DevMem
Class to read and write data aligned to word boundaries of /dev/mem
"""
class DevMem:
    # Size of a word that will be used for reading/writing
    word = 4
    mask = ~(word - 1)

    def __init__(self, base_addr, length = 1, filename = '/dev/mem',
                 ):

        if base_addr < 0 or length < 0: raise AssertionError

        self.base_addr = base_addr & ~(mmap.PAGESIZE - 1)
        self.base_addr_offset = base_addr - self.base_addr

        stop = base_addr + length * self.word
        if (stop % self.mask):
            stop = (stop + self.word) & ~(self.word - 1)

        self.length = stop - self.base_addr
        self.fname = filename

        # Check filesize (doesn't work with /dev/mem)
        #filesize = os.stat(self.fname).st_size
        #if (self.base_addr + self.length) > filesize:
        #    self.length = filesize - self.base_addr

        # self.debug('init with base_addr = {0} and length = {1} on {2}'.
        #         format(hex(self.base_addr), hex(self.length), self.fname))

        # Open file and mmap
        f = os.open(self.fname, os.O_RDWR | os.O_SYNC)
        self.mem = mmap.mmap(f, self.length, mmap.MAP_SHARED,
                mmap.PROT_READ | mmap.PROT_WRITE,
                offset=self.base_addr)


    """
    Read length number of words from offset
    """
    def read(self, offset, length):
        if offset < 0 or length < 0: raise AssertionError

        # Make reading easier (and faster... won't resolve dot in loops)
        mem = self.mem

        # self.debug('reading {0} bytes from offset {1}'.
        #            format(length * self.word, hex(offset)))

        # Compensate for the base_address not being what the user requested
        # and then seek to the aligned offset.
        virt_base_addr = self.base_addr_offset & self.mask
        mem.seek(virt_base_addr + offset)

        # Read length words of size self.word and return it
        data = []
        for i in range(length):
            data.append(struct.unpack('I', mem.read(self.word))[0])

		#just return list, modified by zhansb
		#abs_addr = self.base_addr + virt_base_addr
		#return DevMemBuffer(abs_addr + offset, data)
        return data


    """
    Write length number of words to offset
    """
    def write(self, offset, din):
        if offset < 0 or len(din) <= 0: raise AssertionError

        # self.debug('writing {0} bytes to offset {1}'.
        #         format(len(din), hex(offset)))

        # Make reading easier (and faster... won't resolve dot in loops)
        mem = self.mem

        # Compensate for the base_address not being what the user requested
        #offset += self.base_addr_offset	#fix double plus base_addr_offset by zhansb


        # Check that the operation is going write to an aligned location
        if (offset & ~self.mask): raise AssertionError

        # Seek to the aligned offset
        virt_base_addr = self.base_addr_offset & self.mask
        mem.seek(virt_base_addr + offset)
        # Read until the end of our aligned address
        for i in range(0, len(din), self.word):
            # self.debug('writing at position = {0}: 0x{1:x}'.
            #             format(self.mem.tell(), din[i]))
            # Write one word at a time
            mem.write(struct.pack('I', din[i]))

    '''
    def debug_set(self, value):
        self._debug = value

    def debug(self, debug_str):
        if self._debug: print 'DevMem Debug: {0}'.format(debug_str)
    '''


class MapReg:
    def __init__(self, name, addr, size):
        self.name = name # just for debug
        self.addr = addr
        self.size = size
        self.mem = DevMem(addr, size, "/dev/mem")

    def write(self, offset, val):
        #logging.debug("write: \toffset=%#06x, val=%#010x\t(%s)" % (offset, val, bin(val)))
        self.mem.write(offset, [val,])

    def read(self, offset):
        val = self.mem.read(offset, 1)[0]
        # logging.debug("read: \toffset=%#06x, val=%#010x\t(%s)" % (offset, val, bin(val)))
        return val

    def __str__(self):
        return 'MapReg: name=%s, phyaddr=%#010x, len=%#x' % (self.name, self.addr, self.size)
    __repr__ = __str__

