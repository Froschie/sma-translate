# sma-translate
Script to query all possible codes from SMA Inverter WebConnect Interface and translate them into readable description with actual values.

SMA Inverter uses codes to query informations via JSON WebConnect Interface.
They are not publically documented.
However the SMA Inverter WebGUI itself is providing a dictionary for translating the different codes to a name with additional informations like unit.

The translation can be done by the `ObjectMetadata_Istl.json` file from the SMA Inverter WebGUI and a language specific translation file `en-US.json` also provided by the SMA Inverter WebGUI.


## SMC WebConnect Code Example

The code `6100_40263F00` described the current power generated.
