# Demo of the DMR++ GeoTiff
This is an enabler objective for the EED-3 PI 26.1

## Build the DMR++
Use the notebook `virtual-tiff.ipynb` to make the DMR++ files.

This was done for us (8/4/26)

## Serve data using DMR++ and file:// URLS
Copy the *.dmrpp and matching *.tif files from `output_files` and `input_files`, respectively, to
this directory. 

Edit the file:// URL so that it uses the prefix `/Users/jhrg/src/opendap/kerchunk-dmrpp`.

First get the latest Hyrax container (`latest` is the latest _release_, the most recent _build_ is `snapshot`): 

```bash
docker run -d -h hyrax -p 8080:8080 --name=hyrax opendap/hyrax:latest
```

>[!NOTE]
>Panoply needs Java 11 OSX 26.5 doesn't have that - brew?

To run Hyrax/Docker andd serve these data:

```bash
export prefix=/Users/jhrg/src/opendap/kerchunk-dmrpp/geotiff_demo
docker run -d -h hyrax -p 8080:8080 --name=hyrax --volume $prefix:/usr/share/hyrax --volume $prefix/site.conf:/etc/bes/site.conf opendap/hyrax:latest
```

Add the `dmrpp:href` attribute to the <Dataset/> element at the top level. for our data I used
`dmrpp:href="file:///usr/share/hyrax/HLS_L30_T56NQK_2026109T235750_v2_0_B11.tif"`

If these are accessed using HTTP/HTTPS, then you need to use the site.conf to set AllowedHosts to
permit access to the remote site. For `file://` URLs, you don't need to set AllowedHosts, but you
do need to make sure the URLs start with the dataset root (the default for the hyrax Docker container
is `/usr/share/hyrax`).

The `site.conf` looks like:

```bash
# AllowedHosts value for the https URLs
# AllowedHosts += ^https://.*/stuff.tif$
```

When you start the server using docker, use this option (with the previous value of `$prefix`):
```bash
--volume $prefix/site.conf:/etc/bes/site.conf
```
