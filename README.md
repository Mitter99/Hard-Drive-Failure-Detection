# Hard Drive Failure Detection using S.M.A.R.T attributes on Backblaze dataset.

### Introduction

Hard drives are the most commonly used and failed components in data centers. The data centers use different varieties of hard drives, like HDD and SSD, with various brands, models, and capacities. The HDD drives are the cheapest available on the market, at approximately $40 per TB have high power consumption, slower read/write speeds, and make noise as it has moving parts, whereas the SSD drives are the most expensive, at around $250 per TB have low power consumption, fast read/write speeds, and are completely noiseless.

### Backblaze

Backblaze is a cloud storage and data backup provider that has shared an enormous dataset collected over several years in open source for research and educational purposes. Backblaze also provides the required information about the SMART attributes, and the dataset is stored in the CSV format (Comma Separated Value).

### Dataset

The data is presented in a csv file for each day. Backblaze provided folders quarterly (3 months, i.e., 90–92 days) with 90–92 csv files in each folder, with the date (YYYY-MM-DD) as each file name and the year with quarter (YYYY_QN) as the folder name. The columns (features) of the dataset contain:

a. Date: the date the drive was recorded in the format YYYY-MM-DD.

b. Serial Number: The manufacturer’s assigned serial number, which is unique for each drive.

c. Model- The manufacturer assigned a model number to the drive. The manufacturer can have several models, and it can also manufacture many drives for that model.

d. Capacity: The drive capacities are in bytes.

e. Failure: “0”-if the drive is fine and running. “1”- if the drive is operational and running on the last day.

f. S.M.A.R.T attributes: There are several attributes in the dataset. Each attribute has a raw value and a normalized value that scales from 1 to 253 (representing 1 as the worst and 253 as the best).

We are picking 2019 dataset from kaggle.

Download:

1. https://www.kaggle.com/jackywangkaggle/hard-drive-data-and-stats
2. https://www.backblaze.com/b2/hard-drive-test-data.html

### S.M.A.R.T. Attributes

Self-Monitoring, Analysis, and Reporting Technology (SMART) is a monitoring system that measures the health status of HDDs and SSDs by collecting various attributes like temperature, rpm, power-cycle, read-write errors, etc., through sensors and counters. These S.M.A.R.T attribute values vary depending upon the different conditions, which could be useful for analyzing and predicting drive failures. There are around 70 SMART attributes present in a hard drive. Backblaze provides both the raw and normalized values in their datasets.

### Feature Selection

There are around 130 columns (features) present in the dataset containing 124 S.M.A.R.T attributes, including raw and normalized values. Raw values are preferred over normalized as the normalization is done by the hard drive manufacturer, so it varies with each manufacturer. Domain/Expert knowledge suggested to use S.M.A.R.T.- 5, 9, 187, 188, 193, 194, 197, 198, 241 and 242 as they are more prone to detect failure than other attributes.

1. SMART_5- Rellocated Sectors Count : This attribute count the ‘bad sector’, with increase in drive rellocation this value get increase. It also used as life expectancy of drive as its values increase the read/write speed decrease. Lower value is good for the drive.
2. SMART_9- Power on Hours: Count of hours in power-on state. This attribute shows total count of hours (or minutes, or seconds, depending on manufacturer) in power-on state. By default the life expectancy of hard drive is for 5-years if run 24/7 then 43800 hours. Lower is good for the drive.
3. SAMRT_187- Reported Uncorrectable Errors: The number of UNC errors, i.e. read errors which Error Correction Code (ECC) failed to recover. Normally this attribute value should be equal to zero, prefer lower value.
4. SMART_188- Command Timeout: The number of operations which were interrupted due to HDD timeout.
5. SMART_193- Load Cycle Count or Load/Unload Cycle Count: The number of head movement cycles between the data zone and the head parking area or a dedicated unload ramp. Lower is prefer for running drive.
6. SMART_194- Temperature or Temperature Celsius: Temperature, monitored by a sensor somewhere inside the drive. Raw value typically holds the actual temperature (hexadecimal) in its rightmost two digits. Lower is prefer.
7. SAMRT_197- Current Pending Sector Count: The number of unstable sectors which are waiting to be re-tested and possibly remapped. Lower is prefer.
8. SMART_198- Uncorrectable Sector Count: The number of bad sectors which were detected during offline scan of a disk. When idling, a modern disk starts to test itself, the process known as offline scan, in order to detect possible defects in rarely used surface areas. Lower is prefer for running drive.
9. SMART_241- Total LBAs Written: The total number of 512-byte sectors written during the entire lifetime of the device.
10. SMART_242- Total LBAs Read: The total number of 512-byte sectors read during the entire lifetime of the device.

To observe feature importance, the Random Forest model has been used where S.M.A.R.T- 9, 193, 241, and 242 have higher feature importance than the others.
![1_d8I_CLwHZeR9MY7ZI_7P9Q](https://user-images.githubusercontent.com/66559374/159209932-bf8f1efc-2204-4bb8-8a6c-c0af67c9b9b5.png)

### Handling Imbalance Data

The two methods are considered for handling imbalance data:

1. SMOTE: The technique uses oversampling the minority class by adding synthetic data points. The Imblearn library provides the SMOTE technique. It uses K-NN to create the synthetic samples for the dataset.
2. Smoothing (Backtracking) method: This method is used to smooth the failure status. Here, we go back n days (5,10,15 days, etc.) and alter the failure status of those failed drives from running to fail (0->1). The advantage of using this method is that we can control the number of class-1 (fail) data points. In our case we have 387 class-1 (fail) data points, for n = 5 days there are 1,853 class-1 data points, for n = 10 days there are 3,613 class-1 data points, and for 15 days there are 5,642 class-1 data points. We can choose the same amount of class-0 (running) data points at random to create a balanced dataset. So, for a specific failed drive that has appeared multiple times in the dataset, we simply change their status for a few days without adding any synthetic data.

### Machine Learning

I have used Decision Tree, Random Forest, Light GBM and Custom made model using Stacking method where all the model gave a satisfactory performance, but we chose Light-GBM as our model for deployment.

![1_BJxbUZjxAILqVcFs2Fw9yw](https://user-images.githubusercontent.com/66559374/159210798-af5d8aaf-757b-4321-a606-a8aff337df09.jpg)

## Blog: https://medium.com/@ayaanmitra/hard-drive-failure-detection-7ab7729be0c
## Heroku app: https://harddrive-api.herokuapp.com/index

