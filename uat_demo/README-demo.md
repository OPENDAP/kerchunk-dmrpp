# Demo of the DMR++ GeoTiff
This is an enabler objective for the EED-3 PI 26.1

## Build the DMR++
Use the notebook `virtual-tiff.ipynb` to make the DMR++ files.

This was done separately and used output from the now-deprecated Kerchunk project. (8/4/26)

## Serve data using DMR++ and file:// URLS
Copy the *.dmrpp and matching *.tif files from `output_files` and `input_files`, respectively, to
this directory. 

### Get a Hyrax server container
Get the latest Hyrax container (`latest` is the latest _release_, the most recent _build_ is `snapshot`): 

```bash
docker run -d -h hyrax -p 8080:8080 --name=hyrax opendap/hyrax:latest
```

Test the server with `http://localhost:8080/opendap`

To run Hyrax/Docker andd serve these data (i.e., the data in this directory):
```bash
export prefix=/Users/jhrg/src/opendap/kerchunk-dmrpp/geotiff_demo
docker run -d -h hyrax -p 8080:8080 --name=hyrax --volume $prefix:/usr/share/hyrax opendap/hyrax:latest
```

### Edit the DMR++ file

Add/Edit the `dmrpp:href` attribute to the <Dataset/> element at the top level. For the `HLS_L30_T56NQK_2026109T235750_v2_0_B11.tif` DMR++, I used
`dmrpp:href="file:///usr/share/hyrax/HLS_L30_T56NQK_2026109T235750_v2_0_B11.tif"`
This is needed because the DMR++ needs to know where the data are located. 

About the pathname prefix to the tiff file: In the container we're using for
this demo, the default 'data root directory' for the server is
`/usr/share/hyrax/` and that is why we use `file://` URLs with that prefix. See
the [Hyrax server configuration
guide](https://opendap.github.io/hyrax_guide/Master_Hyrax_Guide.html) for help
understanding this somewhat esoteric point. If it help, think Unix `chroot`.
Effectively, Hyrax can see only the part of its local filesystem rooted at the
data root directory. This is a common security feature used by data servers to
limit data that are exposed to the network.

### Restart Hyrax
Run `docker rm -f hyrax` and then rerun the above `docker run ...` command. The 
DMR++ files you edited should now work.

### If you are using a data file in an S3 bucket...

>[!NOTE]
> For `file://` URLs, ignore this bit about the `site.conf file.
If these are accessed using HTTP/HTTPS, then you need to use the site.conf to set AllowedHosts to
permit access to the remote site. For `file://` URLs, you don't need to set AllowedHosts, but you
do need to make sure the URLs start with the dataset root (the default for the hyrax Docker container
is `/usr/share/hyrax`).

The `site.conf` would look like:
```bash
# AllowedHosts value for the https URLs
AllowedHosts += ^https://.*\.tif$
```
Which is OK for this setup, but never use that permissive a regex on a production server.

When you start the server using docker, use this option (with the previous value of `$prefix`) like this
`--volume $prefix/site.conf:/etc/bes/site.conf`. The complete docker command becomes:
```bash
docker run -d -h hyrax -p 8080:8080 --name=hyrax --volume $prefix:/usr/share/hyrax --volume $prefix/site.conf:/etc/bes/site.conf opendap/hyrax:latest
```
