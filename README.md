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
- name: pkg-jq
  image: coderus/sailfishos-platform-sdk
  user: root
  commands:
  - cp -R ~nemo/.scratchbox2/ /root
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl zypper -n in git flex bison gcc libtool
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl rpm -i ./RPMS/*.rpm
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl rpmbuild -bb SPECS/jq.spec
  - sb2 -R -t SailfishOS-3.4.0.22-armv7hl cp -R /root/rpmbuild/RPMS/ ./
  when:
    target:
      - production
```

First command is to put scratchbox2 config from nemo user into root user (you have to build stuff as root). The next line is to add the required packages for building like git, devel-packages aso. On the third line you are going to install build-time depencencies, like RPMs build on a previous set. On the fourth line you are going to rpmbuild a binary file using the given spec file for creating RPMs. Please note that I slightly modified the spec file to clone the needed git repository using the rpmbuild process. The last line copies the RPM files from root rpmbuild dir into the workspace for later usage in build steps or to upload all RPMs into some repository like Github release page or S3 storage.

