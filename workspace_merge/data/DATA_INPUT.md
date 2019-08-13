## Data Input

#### File Structure

| Folder      | Description
| ----------- | ----------
|building_footprint/        | Building footprint data for extruding 3D building models
|gge_url/ |  Google Earth Online URLs used to specify Google Street View(GSV) parameters for download GSV. Only used in 'gge_url_txt' input mode
|gsv_para_csv/      | CSV file storing GSV parameters for downloading GSV. Only used in 'gsv_para_csv' input mode
|pre_download_info/         | Storing pre-download geo-tagged images in ./image/ folder, alongside a csv file specifying geo-referenced information and image filename. Only used in 'gsvImg_and_infoCsv' input mode

#### Image Input Modes

image input mode is specified in the json config file by keyword "input_data" - "input_form"

- __gge_url_txt__:  
use a txt file ([demo](gge_url/demo_gge_url.txt)) containing urls copied and pasted from [Google Earth Online](https://earth.google.com/web/) to specify the geo-referenced parameters for downloading GSV. This input mode allows users to preview GSV in browser and download according to need. This also lower the risk of camera location snapping due to missing GSV image in specified camera locations

- __gsv_para_csv__:  
use a csv file with [particular format]() to specify parameters for downloading GSV. This mode has higher risk of resulting in camera location snapping by [Google Street View Javascript API](https://developers.google.com/maps/documentation/streetview/intro#optional-parameters "GSV parameters"), and therefore needs double check on the camera coordinate before downloading process

- __gsvImg_and_infoCsv__:  
use pre-download images and a [csv file](gsv_para_csv/demo_gsv_paras.csv) storing the geo-referenced information for each image as input. This input mode does not requires Google Cloud Platform API key for downloading GSV images, and would be suitable for using customize geo-tagged image as input.
