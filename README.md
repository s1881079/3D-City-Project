# 3D City Project

This repository stores the codes and demo in a master dissertation project. A python package __Semsticker__ is developed for attaching semantic building components to coarse 3D city models extruded from building footprint data.

### Semsticker

1.  [General introduction](src/SS_INTRO.md)
2.  [Workspace file structure](src/FILE_STRUC.md)
3. [Demo](https://github.com/s1881079/3D-City-Project/blob/branch-bkup/workspace_merge/src/SS_INTRO.md#rundemo)


### Dissertation information

__Title:__
Application of Geo-tagged Images for Automated Attribution of 3D City  
__Abstract:__
In recent years, growing applications of three-dimenstional city models have brought new challenges to the construction of 3D city models, requiring the models to be large-scaled as well as semantically enriched. Existing methods, however, show a general trade-off between the scale and granularity of the resulting models: constructions of detailed models rely heavily on manual work while large-scaled, auto-generated models lack detailed features. Interests in increasing level of detail (LoD) of auto-generated city models have grown continuously over these years. One of the shared essential focus of these researches is the addition of entrances to the buildings. The attachment of entrance attributes to buildings in a 3D model can largely increase its interactivity and have potential implementations in gaming, item delivery, escape route planning and automatic navigation in both indoor and outdoor environments. This project aims to build a pipeline for automated attachment of entrances attributes to buildings in an existed, relatively coarse 3D city model. It uses geo-tagged images and building footprint data as input and automatically generates 3D city model with entrance data attached to buildings. Entrances of buildings in geo-tagged images were recognized through computer vision techniques and their 3D locations were calculated using photogrammetric algorithms. The resulting 3D city was presented in CityGML format. According to experimental validation, the pipeline is considered relatively efficient positional accurate. However, the data completeness of the result is yet to be improved. In future study, this pipeline has the potential of adapting to larger varieties of building components and further enriching the semantic details of 3D city models.
