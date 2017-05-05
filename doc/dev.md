# DEVELOPMENT

## ENTER VIRTUAL ENVIRONMENT

```bash
# Ensure that packages blow was installed
apt-get install git python2 python3 inkscape xcursorgen

# Clone repository
git clone https://github.com/kevin-leptons/venom.git
cd venom

# Create python virtual environment
# Only require on first time
./env init

# Active python virtual environments
. venv/bin/active

# Install development packages
# Only require on first time or dependency package was updated
./env install
```

## THEME SPECIFICATIONS

```bash
# List name of all of themes and it's properties
./ctl list theme
```

To modify theme specs, inspect [tool/builder.py](../tool/builder.py),
then add new instances of `ThemeSpec` follow format.

- First argument is name of theme
- Second argument is front color, use to display text, border.
It is hex code in RGB format
- Third argument is back color, use for background
- Fourth argument is danger color, use for warning, error text

```python
THEME_SPECS = OrderedDict([
    ...
    ('venom-orange', ThemeSpec('venom-orange', '#ff8c00', 'black', 'red')),
    ('venom-red', ThemeSpec('venom-red', '#ff0000', 'black', 'red'))
])
```

## BUILD

```bash
# Build all of themes
# Or build specific themes
./ctl build
./ctl build black green...

# Clean all of themes
# Or clean specific themes
./ctl build --clean
./cll build --clean black green...

```

## TEST

```bash
# Run all of unit tests
./ctl test

# Run specify unit test
pytest test/<unit-test>.py
```


## PACK

```bash
# Pack theme into debian package format
# result is put into 'dist/venom_<version>_all.deb'
./ctl dist

# Or clean distribution files
./ctl dist --clean
```

# EXTERNAL SOURCES

Venom use on few of external sources. However, source code was restructured,
and rewritten; image is converted, and some files was removed to reduce size.
List of external sources below:

- GTK3 theme was cloned from
[gtk-3.16/theme/HighContrast](https://github.com/GNOME/gtk/tree/gtk-3-16/gtk/theme/HighContrast)
follow [GNU Library General pubic license](https://www.gnu.org/licenses/old-licenses/lgpl-2.0.en.html)
- Icons theme was cloned from
[Flat-Remix](https://github.com/daniruiz/Flat-Remix)
follow [Createtive Commons Attribution-ShareAlike 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/)

# REFERENCES

- [Debian - Wikipedia](https://en.wikipedia.org/wiki/Debian)
- [GNOME - Wikipedia](https://en.wikipedia.org/wiki/GNOME)
- [Python - Wikipedia](https://en.wikipedia.org/wiki/Python_(programming_language))
- [Virtual Environment - wikipedia](https://en.wikipedia.org/wiki/Virtual_environment_software)
- [Python Virtual Environment](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)
