
# blobfish
## A library for frustrated Python programmers who want to work with binary data.

There are too many ways to work with binary data in Python. There are ints of ones and zeros, ints of ASCII values, strings of ones and zeros, strings of binary decoded into text, bytes (`b""`), lists of ints representing ASCII codes, lists of ints representing ones and zeros, lists of bools representing ones and zeros, and probably 10 more I can't think of while I'm writing this. There are also lots of ways to decode them: format, str.encode, bytes.decode, int.to_bytes, int.from_bytes, bin, ord, chr, and f-strings. __Blobfish fixes that by having one object for creating, concatenating, reading, and writing binary.__

---


## Installation

```bash
pip install git+https://github.com/jackr4bbit/blobfish
```

---

## Usage

## `blobfish.Binary`
__the main class for binary data.__

_(alias `blobfish.B`)_
- Parameters:
  - You can pass a `str` of ones and zeros.
    - `blobfish.Binary("1101")`
  - You can pass another `blobfish.Binary` instance.
    - `blobfish.Binary(blobfish.One)`
  - You can pass multiple `blobfish.Binary` instances.
    - `blobfish.Binary(blobfish.One, blobfish.Zero, blobfish.One)` (same as `blobfish.One+blobfish.Zero+blobfish.One`)
  - You can pass nothing.
    - `blobfish.Binary()`
- Operations (supported Python built-ins):
  - `+`: concatenation of two `blobfish.Binary` instances
    - `blobfish.One + blobfish.Zero` results in a `blobfish.Binary` instance representing "10".
  - `sum`: the data of multiple `blobfish.Binary` instances concatenated together (similarly to `+`, but with a list).
    - `sum([blobfish.One, blobfish.Zero, blobfish.One])` results in a `blobfish.Binary` instance representing "101".
  - `*`: repetition of a `blobfish.Binary` instance
    - `blobfish.One * 3` results in a `blobfish.Binary` instance representing "111".
  - `==`: equality comparison between two `blobfish.Binary` instances
    - `blobfish.One == blobfish.One` results in `True`.
    - `blobfish.One == blobfish.Zero` results in `False`.
  - `!=`: inequality comparison between two `blobfish.Binary` instances
    - `blobfish.One != blobfish.Zero` results in `True`.
    - `blobfish.One != blobfish.One` results in `False`.
  - `str`: string representation of the binary data
    - `str(blobfish.One)` results in `"1"`.
  - `len`: length of the binary data in bits or bytes depending on `byteIndexes` (see below).
    - `len(blobfish.OneByte)` results in `1` if `blobfish.byteIndexes == True`.
    - `len(blobfish.OneByte)` results in `8` if `blobfish.byteIndexes == False`.
  - `repr`: a constructor-style representation of the `blobfish.Binary` instance, showing its binary data. This should be used only for debugging purposes.
    - `repr(blobfish.OneByte)` results in `"Binary('11111111')"`.

### `blobfish.Binary.write`
__a method to write the binary data to a file.__

You must pass an instance of `io.BufferedIOBase` with writing capabilities (`io.BufferedRandom` or `io.BufferedWriter`), such as generated from `open(filename, "wb")` or `open(filename, "rb+")`.
> [!TIP]
> Writes are byte-aligned and trailing zero padding may be added automatically.
> If your data isn't multiple of 8 bits, the last byte will be padded with zeros to make it a full byte.

```python
import blobfish

binary = blobfish.Binary("011000010110001001100011")

with open("file.bin", "wb") as file:
    binary.write(file)
```

### `blobfish.Binary.encode`
__a method to encode the binary data into a string or list of ints__

You must pass `int` or `str` to specify the encoding type.
> [!TIP]
> Encodings are byte-aligned and trailing zero padding may be added automatically.
> If your data isn't multiple of 8 bits, the last byte will be padded with zeros to make it a full byte.

```python
import blobfish

binary = blobfish.Binary("011000010110001001100011")
print(binary.encode(str)) # Output: 'abc'
print(binary.encode(int)) # Output: [97, 98, 99]
```

---
## `blobfish.fromBytes`
__a function to create a `blobfish.Binary` instance from bytes.__

You must pass a `bytes` object.
`blobfish.fromBytes(b"abc")` creates a `blobfish.Binary` instance representing "011000010110001001100011".

---
## `blobfish.fromString`
__a function to create a `blobfish.Binary` instance from a string.__

_(alias `blobfish.fromStr`)_
- Parameters:
  - You must pass a `str` object.
  - Optionally, you can specify what encoding to use as a string. The default is utf-8.
`blobfish.fromString("abc")` creates a `blobfish.Binary` instance representing "011000010110001001100011".
`blobfish.fromString("abc", encoding="utf-16")` creates a `blobfish.Binary` instance representing "1111111111111110011000010000000001100010000000000110001100000000".

---
## `blobfish.fromFile`
__a function to create a `blobfish.Binary` instance from the contents of a binary file.__

You must pass an instance of `io.BufferedIOBase` with reading capabilities (`io.BufferedRandom` or `io.BufferedReader`), such as generated from `open(filename, "rb")` or `open(filename, "wb+")`.
> [!CAUTION]
> This function reads the entire file into memory, so it may not be suitable for large files.

```python
import blobfish

with open("file.bin", "rb") as file:
    binary = blobfish.fromFile(file)
    
print(type(binary)) # Output: <class 'blobfish.Binary'>
```

---
## Shortcuts
- `blobfish.One` (alias `blobfish.O`): an instance of `blobfish.Binary` with a single bit of value `1`.
- `blobfish.Zero` (alias `blobfish.Z`): an instance of `blobfish.Binary` with a single bit of value `0`.
- `blobfish.OneByte` (alias `blobfish.OB`): an instance of `blobfish.Binary` with a single byte of value `0xFF` (`11111111`).
- `blobfish.ZeroByte` (alias `blobfish.ZB`): an instance of `blobfish.Binary` with a single byte of value `0x00` (`00000000`).

---
## `blobfish.byteIndexes` and `blobfish.Binary.byteIndexes`
The length of a `blobfish.Binary` instance will be in bits if that instance's `byteIndexes` attributes is `False` and in bytes if it's `True`. If the instance's `byteIndexes` attribute is `None`, it will use the value of the global variable `blobfish.byteIndexes` instead.
It also affects the behavior of getting indexes or slices of a `blobfish.Binary` instance: if the instance's `byteIndexes` is `True` (or it's `None` and the global `byteIndexes` is `True`), getting an index or slice will return a `blobfish.Binary` instance representing the corresponding byte(s), and if not, getting an index or slice will return a `blobfish.Binary` instance representing the corresponding bit(s).
By default, `blobfish.byteIndexes` is set to `True` and `blobfish.Binary.byteIndexes` is set to `None`.

In short: If you want to change the behavior for all `blobfish.Binary` instances, change the value of `blobfish.byteIndexes`. If you want to change the behavior for a specific instance, set that instance's `byteIndexes` attribute to `True` or `False`.
```python
import blobfish
binary = blobfish.Binary("1111111100000000")
print(len(binary))  # Output: 2
print(binary[0])    # Output: Binary('11111111')
binary.byteIndexes = False
print(len(binary))  # Output: 16
print(binary[0])    # Output: Binary('1')
```