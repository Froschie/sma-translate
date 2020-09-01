# sma-translate
Script to query all possible codes from SMA Inverter WebConnect Interface and translate them into readable description with actual values.

SMA Inverter uses codes to query informations via JSON WebConnect Interface.
They are not publically documented.
However the SMA Inverter WebGUI itself is providing a dictionary for translating the different codes to a name with additional informations like unit.

The translation can be done by the `ObjectMetadata_Istl.json` file from the SMA Inverter WebGUI and a language specific translation file provided by the SMA Inverter WebGUI.

## SMA Supported Languages

| Language | File |
| --- | --- |
| English | en-US.json |
| German | de-DE.json |
| Czech | cs-CS.json |
| Greek | el-EL.json |
| Spanish | es-ES.json |
| French | fr-FR.json |
| Italian | it-IT.json |
| Japanese | ja-JP.json |
| Korean | ko-KR.json |
| Dutch | nl-NL.json |
| Polish | pl-PL.json |
| Portuguese | pt-PT.json |
| Thai | th-TH.json |

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


## SMC WebConnect Code Example

The code `6100_40263F00` described the current power generated.
