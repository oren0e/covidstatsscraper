echo "changing permissions to file"
chmod +x covids.py
echo "copying to /usr/local/bin"
sudo cp ./covids.py /usr/local/bin
echo "creating symbolic link..."
sudo ln -s /usr/local/bin/covids.py /usr/local/bin/covids
echo "done!"