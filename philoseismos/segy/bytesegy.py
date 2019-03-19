""" philoseismos: with passion for the seismic method.

@author: sir-dio
e-mail: dubrovin.io@icloud.com """


class byteSegy:

    """ """

    def __init__(self, segy):
        """ """

        # store a reference to the Segy object:
        self.segy = segy

        # create empty bytearrays for different file parts:
        self.tfh = bytearray()
        self.bfh = bytearray()
        self.data = bytearray()

        # new byteSegy has no size:
        self.sizeB, self.sizeMB = 0, 0

    def load_from_file(self, file):
        """ """

        # get the bytes and load them:
        bytes_ = self._get_bytearray_from_file(file)
        self._load_from_bytearray(bytes_)

    def to_file(self, file):
        """ """

        self._update()
        out = self._pack_to_bytearray()
        self._write_bytearray_into_file(file, out)

    def _update(self):
        """ """

        self.segy.TFH._pack_to_byteSegy()
        self.segy.BFH._pack_to_byteSegy()
        self.segy.Data._pack_to_byteSegy()

    def _load_from_bytearray(self, bytearray_):
        """ """

        # separate the array into file parts:
        self.tfh = bytearray_[:3200]
        self.bfh = bytearray_[3200:3600]
        self.data = bytearray_[3600:]

        # store the size information:
        self.sizeB = len(bytearray_)
        self.sizeMB = round(self.sizeB / 1e6, 1)

    def _get_bytearray_from_file(self, file):
        """ """

        # open the file and return the bytes:
        with open(file, 'br') as f:
            return f.read()

    def _pack_to_bytearray(self):
        """ """

        return self.tfh + self.bfh + self.data

    def _write_bytearray_into_file(self, file, bytearray_):
        """ """

        with open(file, 'bw') as f:
            f.write(bytearray_)
