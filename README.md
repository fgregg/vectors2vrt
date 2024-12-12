# `vectors2vrt`

## Usage
```console
Usage: vectors2vrt [OPTIONS] [INPUT_FILES]...

  Create a VRT file from vector inputs.

  example:
     vectors2vrt A.geojson B.sqlite -o output.vrt

Options:
  -o, --output TEXT  Path to the output VRT file or '-' to write to stdout
                     [required]
  --help             Show this message and exit.
```

## Installation

Requires GDAL to be installed on your system.

```console
> pip install vectors2vrt
```

if you upgrade your GDAL you will need to re-install.
