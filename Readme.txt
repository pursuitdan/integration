#ReadMe

filedata.txt contains 30secs of filesink data converted to text file using the following command
tshark -i lo -q -T fields -e wlan.ra -e wlan.ta -e rftap.snr > filedata.txt

filedata.txt contains 3 columns
Receiver MAC     Transmitter MAC   SNR_signal


Edge cases: Maybe few lines have 2 columns: need to identify them properly, Some lines may have no data(not WiFi frame)

###############################################################

pythonpowwow.py

Takes care of the edge cases and find the unique MAC address among the RX and TX and stores in a temporary dictionary and then uploads in Elastic Search

###############################################################

The dictionary value is stored in the Elastic search database
