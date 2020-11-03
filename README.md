## SailfishOS OSM Scout Server CI/CD pipeline ##
This is a POC for building the very best mapping application ever created by Rinigus using docker-based CI/CD tooling.

As noticed in a past SailfishOS meeting OBS will be shut done in the mid-term so a new way building things needs to be used.

Based on the perfect fitting SailfishOS docker images by CodeRUS I have written a small build-pipeline using Drone.io CI/CD to build the final RPMs.

It is not a replacement for the functionality OBS offers for building Linux specific RPMs, but on the other hand is it a clean and simple setup and will get things done so updated mapping packages will be available ASAP a new SDK had been release by Jolla.

Based on the OBS spec files I slightly modified them to clone the needed git repository from Rinigus instead of using archive files.

### How to use Drone.io CI/CD ###
Here are the basic steps you need to implement to build __any__ SailfishOS package using Drone.io. 

```yaml
kind: pipeline
type: docker
name: default

workspace:
 base: /home/nemo/rpmbuild

steps:
- name: download-artifacts
    image: rclone/rclone
    environment:
      RCLONE_S3_PROVIDER: Minio
      RCLONE_S3_ACCESS_KEY_ID:
        from_secret: s3_access_key
      RCLONE_S3_SECRET_ACCESS_KEY:
        from_secret: s3_secret_key
      RCLONE_S3_ENDPOINT:
        from_secret: s3_endpoint
    commands:
      - rclone copy :s3:cache/RPMS ./RPMS

- name: pkg-jq
  image: coderus/sailfishos-platform-sdk
  user: root
  commands:
  - cp -R ~nemo/.scratchbox2/ /root
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl zypper -n in git flex bison gcc libtool
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl rpm -i ./RPMS/armv7hl/*.rpm
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl rpmbuild -bb SPECS/jq.spec
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl cp -R /root/rpmbuild/RPMS/ ./
  when:
    target:
      - production

  - name: upload-artifacts
    image: rclone/rclone
    environment:
      RCLONE_S3_PROVIDER: Minio
      RCLONE_S3_ACCESS_KEY_ID:
        from_secret: s3_access_key
      RCLONE_S3_SECRET_ACCESS_KEY:
        from_secret: s3_secret_key
      RCLONE_S3_ENDPOINT:
        from_secret: s3_endpoint
    commands:
      - rclone copy ./RPMS :s3:cache/RPMS
```
There are three parts in the build pipeline: 

1. download artifacts from external storage
2. build package 
3. upload artifacts to external storage for later re-use.

In the build step basically the following is done: 
- First command is to put scratchbox2 config from nemo user into root user (you have to build stuff as root). 
- The next line is to add the required packages for building like git, devel-packages aso. 
- On the third line you are going to install build-time depencencies, like RPMs build on a previous set. 
- On the fourth line you are going to rpmbuild a binary file using the given spec file for creating RPMs. 

Please note that I slightly modified the spec file to clone the needed git repository using the rpmbuild process. The last line copies the RPM files from root rpmbuild dir into the workspace for later usage in build steps or to upload all RPMs into some repository like S3 storage.

### There might be dragons ... ###
To speed up compilation times I parallelized root pipelines. However later pipelines need RPM artifacts build earlier so the artifacts must be persisted. I used S3 storage for this. Please keep in mind that Drone's S3 sync plugin sucks so better use rclone docker image for this.


