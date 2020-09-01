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


## SMC WebConnect Code Example

The code `6100_40263F00` described the current power generated.
