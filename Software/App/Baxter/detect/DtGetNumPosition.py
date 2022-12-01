#!/usr/bin/python3

import sys

class DtGetNumPosition(object):
    _cx:int = 0.0
    _cy:int = 0.0
    _sectorW:int = 0.0
    _sectorH:int = 0.0
    _countW:int = 7
    _numSectorH:int = 0
    _numSectorW:int = 0
    _additional:int = 0

    def __init__(self, gridCoord, objectCoord) -> None:
        if gridCoord == objectCoord:
            print("Error")
            sys.exit(1)
        self._gridCoord = gridCoord
        self._objectCoord = objectCoord
    
    def getNumPosition(self)->int:

        if (self._gridCoord[0] == True) and (self._objectCoord[0] ==  True):
            self._sectorH = (self._gridCoord[4] - self._gridCoord[3]) / 7
            self._cy = (self._objectCoord[3] + self._objectCoord[4]) / 2
            self._cx = (self._objectCoord[1] + self._objectCoord[2]) / 2
        else:
            print("wrong dimensions")
            sys.exit(1)
        

        if self._cx <= self._gridCoord[2] and self._cx >= self._gridCoord[1] and \
            self._cy <= self._gridCoord[4] and self._cy >= self._gridCoord[3]:

            for i in range(7): 
                if self._cy <= (self._gridCoord[4] - i * self._sectorH) and \
                    self._cy >= (self._gridCoord[4] - (i * self._sectorH + self._sectorH)):
                    self._numSectorH = i
                    if self._numSectorH > 0:
                        self._additional = 1
                    print(f'numSectorH {self._numSectorH}')
                    break

            if self._numSectorH == 0  or self._numSectorH == 6:
                self._sectorW = (self._gridCoord[2] - self._gridCoord[1]) / self._countW
            else:
                self._countW = 8
                self._sectorW = (self._gridCoord[2] - self._gridCoord[1]) / self._countW    

            print(f'countW {self._countW}')
            for j in range(self._countW): 
                if self._cx <= (self._gridCoord[2] - j * self._sectorW) and \
                    self._cx >= (self._gridCoord[2] - (j * self._sectorW + self._sectorW)):
                    self._numSectorW = j
                    print(f'numSectorW {self._numSectorW}')
                    break
        else:
            print("wrong dimensions")
            sys.exit(1)
        
        print(f'additional {self._additional}')
        return (self._numSectorH * 7 + self._numSectorW + self._additional)