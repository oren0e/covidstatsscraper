echo "changing permissions to file"
chmod +x ./covids.py

echo "copying to /usr/local/bin/covid_stats"
mkdir -p /usr/local/bin/covid_stats/core_files
sudo cp -a ./covids.py /usr/local/bin/covid_stats/
sudo cp -a ./core_files/backend.py /usr/local/bin/covid_stats/core_files/

echo "adding to PATH"
echo 'export PATH=/usr/local/bin/covid_stats/:$PATH' >>~/.bash_profile

echo "creating symbolic link..."
sudo ln -s /usr/local/bin/covid_stats/covids.py /usr/local/bin/covid_stats/covids

echo "done!"