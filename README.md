# sma-translate
Script to query all possible codes from SMA Inverter WebConnect Interface and translate them into readable description with actual values.

SMA Inverter uses codes to query informations via JSON WebConnect Interface.
They are not publically documented.
However the SMA Inverter WebGUI itself is providing a dictionary for translating the different codes to a name with additional informations like unit.

The translation can be done by the `ObjectMetadata_Istl.json` file from the SMA Inverter WebGUI and a language specific translation file provided by the SMA Inverter WebGUI.

For example the code `6100_40263F00` describes the current power generated.

## SMA Supported Languages

| Language | File | Code |
| --- | --- | --- | 
| English | en-US.json | en |
| German | de-DE.json | de |
| Czech | cs-CS.json | cs |
| Greek | el-EL.json | el |
| Spanish | es-ES.json | es |
| French | fr-FR.json | fr |
| Italian | it-IT.json | it |
| Japanese | ja-JP.json | ja |
| Korean | ko-KR.json | ko |
| Dutch | nl-NL.json | nl |
| Polish | pl-PL.json | pl |
| Portuguese | pt-PT.json | pt |
| Thai | th-TH.json | th |

*Note: actual support might be different based on SMA Inverter Model and Firmware version!*

## ObjectMetadata_Istl.json File Example

```json
{"6100_00416C00":{"Prio":2,"TagId":350,"TagIdEvtMsg":11549,"Unit":13,"DataFrmt":7,"Scale":1.0,"Typ":0,"WriteLevel":5,"TagHier":[830,267],"Min":true,"Max":true,"Avg":true,"Cnt":true,"MinD":true,"MaxD":true},
"6180_08419000":{"Prio":2,"TagId":814,"TagIdEvtMsg":10003,"DataFrmt":18,"Typ":1,"WriteLevel":5,"TagHier":[830,309,3409]}}
```
*Note: only first 2x items listed.*

Each code contains certain valued. The TagId, TagIdEvtMsg and TagHier fields can be translated from language file.


## ObjectMetadata_Istl.json File Example
```json
{"350":"Waiting time until feed-in",
"11549":"Waiting time until feed-in",
"830":"Status",
"267":"Inverter",
"814":"MPP search status",
"10003":"MPP scan procedure completed successfully",
"309":"Operation",
"3409":"Active power reserve"}
```
*Note: only values used in above ObjectMetadata Example.*


## Script Execution Options

Start the script with python3 and "requests" module installed:

`python WebConnectCodes.py <options>`

| Script Option | Description |
| --- | --- |
| __`--sma_ip=<IP>`__ | IP of SMA Inverter, __Mandatory parameter__! |
| __`--sma_pw=<PW>`__ | PW for User Login in SMA Inverter, __Mandatory parameter__! |
| *`--nossl=True`* | Connect via HTTP instead of HTTPS, *Optional parameter*. |
| *`--csv=True`* | Write complete output to CSV file "*WebConnectCodes.csv*" instead of output to console, *Optional parameter*. |  
| *`--live=no`* | Disable query for actual SMA Inverter data, *Optional parameter*. | 
| *`--onlylive=yes`* | Show only the entries which returned data from SMA Inverter. Total amount of entries 2411, only 294 with data. *Optional parameter*. | 
| *`--lang=en`* | Language selection, *Optional parameter*. Default = de, for possible values see table "*SMA Supported Languages*" above. | 

*Note: on console only minimal output of ID and TagId + the live value if available will be shown!*


## Script Example Output

Minimal command options. Only ID, TagId and the current value will be shown:

`python WebConnectCodes.py --sma_ip=<IP> --sma_pw=<PW>`
```
ID             TagId                                          Query Value                                    Query Result
-------------  ---------------------------------------------  ---------------------------------------------  ------------------------------
6100_00416C00  Wartezeit bis Einspeisung
6180_08419000  Status MPP Suche
6180_08414D00  Zustand
6180_08414E00  Temperatur
6100_40412100  Ok
6180_08414B00  Fehlerbehebungsmaßnahme                        keine                                          [{'val': [{'tag': 885}]}]
6100_00418000  Ereignisnr. Hersteller                         None                                           [{'val': None}]
```



Minimal command options with english language:

`python WebConnectCodes.py --sma_ip=<IP> --sma_pw=<PW> --lang=en`
```
ID             TagId                                          Query Value                                    Query Result
-------------  ---------------------------------------------  ---------------------------------------------  ------------------------------
6100_00416C00  Waiting time until feed-in
6180_08419000  MPP search status
6180_08414D00  Condition
6180_08414E00  Temperature
6100_40412100  Ok
6180_08414B00  Fault correction measure                       none                                           [{'val': [{'tag': 885}]}]
6100_00418000  Event number manufacturer                      None                                           [{'val': None}]
```



Export all data to CSV file:

`python WebConnectCodes.py --sma_ip=<IP> --sma_pw=<PW> --lang=en --csv=True`
```csv
sep=;
"ID";"Prio";"TagId";"TagIdEvtMsg";"Unit";"DataFrmt";"Scale";"Typ";"WriteLevel";"TagHier";"Min";"Max";"Avg";"Cnt";"MinD";"MaxD";"Sum";"SumD";"Deprecated";"Len";"Hidden";"GridGuard";"AvgD";"GroupChange";"Query Value";"Query Result"
"6100_00416C00";"2";"Waiting time until feed-in";"Waiting time until feed-in";"s";"7";"1.0";"0";"5";"Status Inverter";"True";"True";"True";"True";"True";"True";"";"";"";"";"";"";"";"";"";"";
"6180_08419000";"2";"MPP search status";"MPP scan procedure completed successfully";"";"18";"";"1";"5";"Status Operation Active power reserve";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";
"6180_08414D00";"2";"Condition";"Battery status";"";"18";"";"1";"5";"Status Operation Battery";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";
"6180_08414E00";"2";"Temperature";"Battery temp.";"";"18";"";"1";"5";"Status Operation Battery";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"";
"6100_40412100";"2";"Ok";"Power of all battery inverters in OK status";"W";"0";"1.0";"0";"5";"Status Operation Battery status";"True";"True";"True";"True";"";"";"True";"True";"";"";"";"";"";"";"";"";
"6180_08414B00";"2";"Fault correction measure";"Fault correction measure";"";"18";"";"1";"5";"Status Operation Current event";"";"";"";"";"";"";"";"";"";"";"";"";"";"";"none";"[{'val': [{'tag': 885}]}]";
"6100_00418000";"2";"Event number manufacturer";"Current event number for manufacturer";"";"0";"1.0";"0";"5";"Status Operation Current event";"True";"True";"";"True";"True";"True";"";"";"";"";"";"";"";"";"None";"[{'val': None}]";
```
