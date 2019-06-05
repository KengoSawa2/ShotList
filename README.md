# ShotList

![ShotList_1](https://github.com/KengoSawa2/ShotList/blob/master/SS/shotlist_1.png "ShotList_1")



![ShotList_2](https://github.com/KengoSawa2/ShotList/blob/master/SS/shotlist_2.png "ShotList_2")



![ShotList_3](https://github.com/KengoSawa2/ShotList/blob/master/SS/shotlist_3.png "ShotList_3")

## Overview
ShotList can easily export "Video" and "Image" files as "Metadata list with thumbnail" in Excel format(xlsx).

## Usage and Function
[See official site](https://www.shot-list.com/shotlist-en)


## License

[GPL v2.0]  

## to Build and Run

#### movie backend Library
ffmpeg 4.x with PyAV 6.x.x

#### still image backend Library
OpenImageIO 2.0.x Python Library
[https://github.com/OpenImageIO/oiio](https://github.com/OpenImageIO/oiio)

ShotList required many many Python Package

| Name | requireVer |
| ---------- | ---------- |
| PyAV | 6.0.0 |
| XlsxWriter | 1.1.5 |
| PySide2 | 5.12.2 |
| natsort | 6.0.0 |
| timecode | 1.2.0 |
| xattr | 0.9.6 |
| xxhash | 1.3.0 |
| pprint | 0.1 |
| tzlocal | 1.5.1 |
| Pydpx_meta

[PyAV6.0.0 needs special patch.](https://github.com/mikeboers/PyAV/pull/482)

The GUI relies on PySide2, so modifications require tools such as QtCreator and Qt Liguist.
See [Qt.io](https://www.qt.io/developers/)

## TODO
- Import from fcpxml?
