# bvg-transport-csv-exporter

All the configurations are kept in **config.ini** file.
The binary file is present in dist directory.

User need to change **output_directory** prpoerty in **config.ini** to the location of path where user wants to write the CSV files.

**Other configuration varaibles**:

**url** : Address of the BVG transport URL from where the data is to be pulled.

**output_directory** : Location of the directory where CSV files are created.

**execution_time_interval_in_seconds** : Interval at which user wants to call above url property.

**max_instances** : maximum instances of the program that can be run parallelly. 

**time_till__to_keep_running_in_minutes** : Specifies the time in minutes, after which program will stop fetching the data from url.

