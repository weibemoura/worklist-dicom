FROM debian:jessie-slim

RUN apt-get update -y \
&& apt-get install curl wget bzip2 rsync -y

RUN cd /opt \
&& wget -q ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk363/bin/dcmtk-3.6.3-linux-x86_64-static.tar.bz2 \
&& tar -xvjf dcmtk-3.6.3-linux-x86_64-static.tar.bz2 \
&& cd dcmtk-3.6.3-linux-x86_64-static \
&& chmod +x bin/* && rsync -rtv bin/ /usr/bin \
&& rsync -rtv etc/ /etc \
&& rsync -rtv share/ /usr/share

