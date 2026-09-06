# OS Downloader — Core

A free, Python-first cross-platform OS catalog and download helper.

## Run

### Windows
Double-click `start.bat`.

### Linux / macOS / Unix-like
Run:

```sh
chmod +x start.sh
./start.sh
```

The launcher checks for Python. If Python is missing, it tells the user where to get it.

## Included sections

- Windows
- Linux
- ChromeOS
- BSD
- DOS
- Other
- **Modified / Experimental**

The Modified / Experimental section contains entries such as Tiny10, Tiny11, TempleOS, SerenityOS, MenuetOS, KolibriOS, Redox OS, Red Star OS, and a placeholder for “Scary OS”.

## Safety / licensing

The app opens legitimate source or download pages. It does not claim unofficial projects are official, and it does not bypass activation, DRM, hardware checks, or licensing.

The catalog is intentionally editable in `app/catalog.py`.

## Roadmap

1. Larger catalog
2. Version → edition → architecture picker
3. Direct download manager
4. Checksum/signature verification
5. Bootable USB creator with explicit erase warnings
6. Boot manager / multi-boot helpers
7. Optional Pro edition and license service
