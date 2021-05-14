# README #

This repo is developed in two phases including research and code implementation. The research phase is to look for ideas of how the report will be constructed. The code-implementation phase is to develop the report from the research ideas. 

### A. REASEARCH ###
To find ideas of how the report will be, there are three relevant readings as follows:

1. AI and Machine Learning in Medical Devices by FDA, October 2020 ([link](https://en.calameo.com/read/00634950448209b7afde0)):
    * Most devices that rely on AI/ML fall into the category that the FDA calls Software as a Medical Device, or SaMD (p.2).
    * AI/ML is categorised based on risk of the devices, or SaMD, from lowest (I) to highest risk (IV) (pp.9-10).

2. FDA permitted first medical device, IDx-DR, using AI to detect diabetic retinopathy, April 2018 ([link](https://www.fda.gov/news-events/press-announcements/fda-permits-marketing-artificial-intelligence-based-device-detect-certain-diabetes-related-eye)):
    * IDx-DR was to detect one of two possible results: (1) more than mild diabetic retinopathy (mtmDR) detected and (2) negative for more than mild diabetic retinopathy. 
    * IDx-DR was reviewed under the FDA’s De Novo premarket review pathway. 
    * The FDA is permitting marketing of IDx-DR to IDx LLC.

3. De Novo classification reqest for IDx-DR, January 2018 ([link](https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN180001.pdf)):
    * This is the technical report done by De Novo summarising key performance metrics of IDx-DR then concluding that IDx-DR was granted. 
    * Test samples: 900 patients enrolled in 10 care sites. However, only 819 patients were fully tested. 
    * Positive class: mtmDR vs. Negative class: not mtmDR.
    * Primary metrics: sensitivity (87%), specificity (90%), positive predicted value (73%) & negative predicted value (96%). 
    * Precision Study: conducting a separate reproducibility and repeatability (precision) study on a smaller subset of patients to tell if the results were consistent. There was almost complete agreement (99.6%) of IDx-DR outputs across repeats.
    * Two major risks: False positive resutls and false negative results. 
    * IDx-DR was classified as class II.

### B. CODE IMPLEMENTATION ###

#### B.1. The directory
    .
    ├── test                      # folder containing test images used for report.py         
    │   ├── 0_1.png   
    │   ├── 0_2.png                   
    │   ├── ...           
    ├── report.py    	          # spinning up container / making predictions for images in test / measuring performance / stopping container 
    ├── report_per_image.json     # json report of predictions for individual images
    ├── report_performance.json   # json report of sensitivity & specificity for individual classes
    └── README.md

#### B.2. Descriptions
- The whole repo was written as Ed suggested. Code is put in separate fuctions. `if __name__== "__main__":` is used. 
- Line 180, `time.sleep(3)`, in `report.py` is to delay the execution in 3 seconds to wait for the docker container to be completely spinned up. Otherwise, errors would occur. Although there were other attempts of using different ways to check the running docker container, they were not successful. Nonehtheless, this will be investigated in future code implementations/experiments.