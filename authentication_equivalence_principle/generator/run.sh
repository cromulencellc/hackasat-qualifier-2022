cd build
./gen
mkdir temp
strip authenticator
cp authenticator temp
cp authdata.bin temp
cp key.txt temp
cd temp
tar -czvf /data/equivalence.tar.gz *
echo "/data/equivalence.tar.gz"