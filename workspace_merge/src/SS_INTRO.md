# Semsticker

This package is developed for automatically adding semantic building components to coarse 3D city model extruded from building footprint data.

### Table of Content
- <a href="dpdcies">Dependencies</a>
- <a href="configformat">Config File</a>
- <a href="rundemo">Demo</a>

### Dependencies
<div id="dpdcies"></div>
to use this package, the following dependencies need to be installed:
- Python 3.4.9 (and later versions)
- pyproj
```bash
pip install --upgrade pyproj
```
- fiona
```bash
pip install --upgrade fiona
```
- shapely
```bash
pip install --upgrade shapely
```
- OpenCV
```bash
pip install --upgrade opencv
```
- Google Cloud Vision client library
```bash
pip install --upgrade google-cloud-vision
```

### Config Json File
<div id="configformat"></div>
the pipeline uses a configure file to specify the parameters needed

__Authority__

| Keyword      | Description
| ----------- | ----------
|"key_txt"       | directory of txt containing [API key](https://developers.google.com/maps/documentation/streetview/get-api-key) to Google Cloud Platform
|"gg_credential"| directory of [Google Cloud Vsion API credential](https://cloud.google.com/vision/docs/quickstart-client-libraries#client-libraries-install-python#before-you-begin) (json file)

__Input_data__

| Keyword      | Description
| ----------- | ----------
|"input_form"       | string indicating the [data input form](../data/DATA_INPUT.md) chosen
|"url_txt"| directory of txt file containing [Google Earth](https://earth.google.com/web/) URLs
|"ori_gsv_folder"| directory of folder containing pre-dpwnloaded geo-tagged images
|"gsv_info_csv"| directory of csv file with geo-referenced information of images
|"bd_shp"       | directory of folder storing building footprint data (currently only supports Esri shapefile)

__Intm_info__

| Keyword      | Description
| ----------- | ----------
|"img_folder"       | directory of folder to store the downloaded Google Street Views
|"write_Simg_Info"| "Execute" - whether to write semantic image information to CSV
|| "out_folder" - folder directory to output the CSV file
|"write_Bbx_Info"| "Execute" - whether to write bounding box information to CSV
|| "out_folder" - folder directory to output the CSV file

__Output_info__

| Keyword      | Description
| ----------- | ----------
|"result_folder"| folder to store the output of the pipeline
|"output_csv"| name of the output CSV file


__Pros_params__

| Keyword      | Description
| ----------- | ----------
|"sight_distance"| furthest sight distance for detecting objects
|"min_objsep"| minimum distance between two objects to be considered separated
|"object_detection_src"| Object Detection source
|"Image_Segmentation"| "Execute" - whether to execute image segmentation before object detection
|| "min_x" - minimum width for filtering bounding box
|| "min_y" - minimum height for filtering bounding box
|| "min_x" - minimum width/height for filtering bounding box

### Demo
<div id="rundemo"></div>
demo program run in Linux terminal
```bash
python3 demo_main.py
```

__for customized use:__
1. install all the Dependencies
2. change demo_config json file to specify parameters, or create a new config file using the format above.
3. run demo_main.py, or change change the line in demo_main.py where config file directory is specified if new config file is used
