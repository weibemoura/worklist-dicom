# Worklist-Dicom
Dicom worklist generator compatible with wlmscpfs (dcmtk)

# Run project in development

```bash
# create file webapp/.env
CACHE_FILE=contrib/cache.bin
HEADER_FILE=contrib/header.bin

WORKLIST_ADDRESS=dicom.weibe.com.br
WORKLIST_PORT=105
WORKLIST_DIR=/data/worklist/FINDSCU
CALLING_AE_TITLE=FINDSCU
CALLED_AE_TITLE=ANY-SCP

# create python virtualenv
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip3 install -r webapp/requirements-dev.txt

# run application
python3 app.py
```

# Run wlmscpfs

```bash
# download dcmtk
wget ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk363/bin/dcmtk-3.6.3-linux-x86_64-static.tar.bz2

# extract files
tar -xvjf dcmtk-3.6.3-linux-x86_64-static.tar.bz2 

# run
export PATH=$PATH:$(pwd)/dcmtk-3.6.3-linux-x86_64-static/bin
export DCMDICTPATH=$(pwd)/dcmtk-3.6.3-linux-x86_64-static/share/dcmtk/dicom.dic
chmod +x ./dcmtk-3.6.3-linux-x86_64-static/bin/*

mkdir -p /data/worklist/FINDSCU
wlmscpfs -d -dfp "/data/worklist/FINDSCU" 105
```

# Run production project

```bash
# deploy using docker compose
docker-compose up --build
```