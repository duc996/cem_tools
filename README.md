# CEM Tools
Some tools for CEM Instruments devices.\
I got got my hand on a CEM multimeter, a 9519BT. This respository is a collection of tools releated to it.

# cem_logger
BLE data logger
This command line tool connects to the CEM bluetooth module (if I remeber correctly it's some TI CC25xx module) and can log received data to a file.

## usage

### First time
I recommand using venv. The first time using it you have to create it:
```
python3 -m venv .venv
```

### Load the virtual environement and install needed modules
```
source .venv/bin/activate
pip install -r requirements.txt
```

### Start the script
```
cem_logger.py -b [your_bluetooth_device_address] -o output_file.csv
```
