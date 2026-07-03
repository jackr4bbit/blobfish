from types import NotImplementedType
import io

byteIndexes = True

class Binary:
    def __init__(self, *args: "Binary | str"):
        self.byteIndexes = None
        if len(args) == 0:
            self.__data = ""
        elif len(args) == 1:
            data = args[0]
            if isinstance(data, str) and set(data).issubset({"1", "0"}):
                self.__data = data
            elif isinstance(data, Binary):
                self.__data = str(data)
            else:
                raise TypeError("You must pass a string of ones and zeroes or one or more Binary objects")
        else:
            for arg in args:
                if not isinstance(arg, Binary):
                    raise TypeError("You must pass a string of ones and zeroes or one or more Binary objects")
            self.__data = "".join(str(arg) for arg in args)

    def __add__(self, other: "Binary") -> "NotImplementedType | Binary":
        if not isinstance(other, Binary):
            return NotImplemented
        return Binary(self.__data + other.__data)

    def __radd__(self, other: "Binary | int") -> "NotImplementedType | Binary":
        if other == 0:
            return self
        elif not isinstance(other, Binary):
            return NotImplemented
        return self.__add__(other)

    def __mul__(self, other: int) -> "NotImplementedType | Binary":
        if not isinstance(other, int):
            return NotImplemented
        return Binary(self.__data * other)

    def __rmul__(self, other: int) -> "NotImplementedType | Binary":
        return self.__mul__(other)

    def __eq__(self, other: "Binary") -> NotImplementedType | bool:
        if not isinstance(other, Binary):
            return NotImplemented
        return self.__data == other.__data

    def __str__(self) -> str:
        return self.__data

    def __repr__(self) -> str:
        return f"Binary({self.__data!r})"

    def __getitem__(self, key: slice | int) -> "Binary":
        step = 8 if (byteIndexes if self.byteIndexes is None else self.byteIndexes) else 1
        maxUnits = len(self.__data) // step
        if isinstance(key, slice):
            if key.step is not None:
                raise ValueError("Slice step not supported")
            start = 0 if key.start is None else key.start
            stop = maxUnits if key.stop is None else key.stop
            if start < 0:
                start += maxUnits
            start = max(0, min(start, maxUnits))
            if stop < 0:
                stop += maxUnits
            stop = max(0, min(stop, maxUnits))
            return Binary(self.__data[step*start:step*stop])
        elif isinstance(key, int):
            if key < 0:
                key += maxUnits
            if key < 0 or key >= maxUnits:
                raise IndexError("Binary index out of range")
            return Binary(self.__data[step*key:step*(key+1)])
        else:
            raise TypeError(f"Indices must be integers or slices, not {type(key).__name__}")

    def __len__(self) -> int:
        return len(self.__data) // (8 if (byteIndexes if self.byteIndexes is None else self.byteIndexes) else 1)

    def write(self, file: "io.BufferedRandom | io.BufferedWriter") -> int:
        """
        Writes the binary data to a file.

        Parameters:
        file (``io.BufferedRandom`` or ``io.BufferedWriter``): The file to write to.

        Returns:
        ``int``: The number of bytes written to the file.
        """
        if not isinstance(file, (io.BufferedRandom, io.BufferedWriter)) or "b" not in file.mode or not file.writable():
            raise ValueError("File must be opened in binary write mode (e.g. \"wb\" or \"rb+\")")
        return file.write(bytes(self.encode(int)))

    def encode(self, encodingType: type[str] | type[int] = str) -> str | list[int]:
        """
        Encodes the binary data into a string or list of ints.

        Parameters:
        encodingType (``str`` or ``int``, optional): The type to encode the binary data as. Default is ``str``.

        Returns:
        Passing ``str`` will return a string of the encoded binary data.
        Passing ``int`` will return a list of the ascii codes as integers.
        """
        if encodingType == str:
            return "".join(chr(i) for i in self.encode(int))
        elif encodingType == int:
            extra = len(self.__data) % 8
            data = self.__data+("0"*(8-extra if extra != 0 else 0))
            return [int(data[i:i+8],2) for i in range(0,len(data),8)]
        else:
            raise TypeError("Encoding type must be str or int")

    def join(self, data: "list[Binary]") -> "Binary":
        """
        Joins the binary data with a seperator.

        Parameters:
        data (``[Binary]``): The data to join.

        Returns:
        `Binary`: The joined binary data.
        """
        if not isinstance(data, Binary):
            raise TypeError("Data must be a list of Binary instances")
        return sum([item for binary in data for item in (binary, self)][:-1])


def fromBytes(bytes: bytes) -> "Binary":
    """
    Creates a `Binary` instance from a bytes object.

    Parameters:
    bytes (``bytes``): The input bytes object to convert.

    Returns:
    `Binary`: An instance representing the binary data of the input bytes object.
    """
    return Binary("".join(f"{byte:08b}" for byte in bytes))

def fromString(string: str, encoding: str="utf-8") -> "Binary":
    """
    Creates a `Binary` instance from a string.

    Parameters:
    string (``str``): The input string to convert.
    encoding (``str``, optional): The encoding to use for the string. Default is ``"utf-8"``.

    Returns:
    `Binary`: An instance representing the binary data of the input string.
    """
    return fromBytes(string.encode(encoding))

def fromFile(file: "io.BufferedRandom | io.BufferedReader") -> "Binary":
    """
    Creates a `Binary` instance from the contents of a binary file.

    Parameters:
    file (``io.BufferedRandom`` or ``io.BufferedReader``): The file to read from.

    Returns:
    `Binary`: An instance representing the binary data of the input file.
    """
    if not isinstance(file, (io.BufferedRandom, io.BufferedReader)) or "b" not in file.mode or not file.readable():
            raise ValueError("File must be opened in binary read mode (e.g. \"rb\" or \"wb+\")")
    return fromBytes(file.read())

#Shortcuts
One      = Binary("1")
Zero     = Binary("0")
OneByte  = One*8
ZeroByte = Zero*8

#Abbreviations
B        = Binary
O        = One
Z        = Zero
OB       = OneByte
ZB       = ZeroByte
fromStr  = fromString
