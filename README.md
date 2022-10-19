# Basalt_test
## Reuirments
1. Firstly if not installed, you need to install python3 and bash on your machine
```
sudo apt-get install python3
sudo apt-get install bash
```
2. After that you need to create environment in python
```
python3 -m venv env
source env/bin/activate
```
3. Install libraries to virtual environment
```
pip install requirments.txt
```
## Launching
2 ways to launch
1. 
```
bash run_package_manager.sh
```
2. If it's the first run
```
chmod +x run_package_manager.sh
```
Then
```
./run_package_manager
```
## Output
You will get the json with fields Extra packages sisyphus (packages that are in sisyphus and not in p10),
Extra packages p10 (packages that are in p10 and not in sisyphus),
Latest packages sisyphus (packages that have bigger release-version in sisyphus)


