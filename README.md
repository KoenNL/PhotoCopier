# Photo Copier

A small and simple script to copy your local iCloud Photos library to a simple file structure.

## How to run
Download the latest version.

In your preferred command line tool run `python3 copyPhotos.py C:\path\to\source C:\path\to\destination`.

For additional information run `python3 copyPhotos.py -h`

### Optional arguments
 - --dry-run: boolean, either True or False, default: False
 - --file-structure: string, either dateFilename or yearMonthDirectories

## File structures
### yearMonthDirectories [default]
Creates a directory for each year and each month containing all photos for that given month with their original filename.

Example:
```
/
--/2016
----/01
------/IMG_1548.JPG
------/IMG_1549.JPG
------/IMG_1550.JPG
----/02
------/IMG_1732.JPG
------/IMG_1738.JPG
------/IMG_1741.JPG
...
```
### dateFilename
Puts all photos directly into the destination directory and changes their filename to the appropriate date with format 'YYYY-MM-DD' and appending underscore, followed by the original filename.

Example:
```
/
--/2016-01-05_IMG_1548.JPG
--/2016-01-05_IMG_1549.JPG
--/2016-01-05_IMG_1550.JPG
--/2016-02-14_IMG_1732.JPG
--/2016-02-15_IMG_1738.JPG
--/2016-02-15_IMG_1741.JPG
...
```