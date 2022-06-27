python3 bitstream.py --input-file="default_cmds.yml" --output="secure.bit"
cp secure.bit /data/
cp *.md /data/
cd /data

tar -czvf /data/secure.tar.gz *
echo "/data/secure.tar.gz"
