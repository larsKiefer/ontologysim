Logger
===================

* 2 types: **summarized logger**, **time logger**
    * for each logger, there is the possebility, to log the summarized kpi over the complete production time or every x seconds (time intervall)
        * the results of the time intervalls, where saved in an extra sub folder
* for each type, each instance is logged and also an average of the instances is calculated

**important:** 
Only tasks with the logging type: "logging" are considered

the kpi's are based on:

* A Hierarchical structure of key performance indicators for operation management and continuous improvement in production systems
    * Ningxuan Kang,Cong Zhao,Jingshan Li &John A. Horst, 2016
    * [Paper](https://www.tandfonline.com/doi/full/10.1080/00207543.2015.1136082)
* for a full describition please view this paper


Machine logger
--------------------

Folder name: machine

Summarized CSV name: machine_logger.csv

**Support kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| TTFp           | Time to failure in percent |  ration |
| TTRp  | Time to repair in percent  | ration |
| FE | Failure event  | number |
| CMTp | Corrective maintenance time in percent  | ration |
| AUPTp | Actual unit processing time in percent | ration |
| APTp | Actual production time in percent | ration |
| AUSTp | Actual unit setup time in percent | ration |
| ADOTp | Actual unit down time in percent | ration |
| AUITp | Actual unit idle time in percent | ration |
| AUBTp |  Actual unit busy time in percent | ration |
| AUSTTp | Actual unit starviation time in percent | ration |
| AUBLTp | Actural unit bloccking time in percent | ration |
| PBTp | Planned busy time | ratio |
| PRIp | Planned run time per item * items | ratio |
| E     | Effectiveness | percentage |
| OEE   | Overall equipment effectiveness | percentage |
| NEE   | Net equipment effectiveness | percentage |

* ratio: KPI value / simulation time (time interval)

**Basic kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| A           | Availability |  percentage |
| AE   | Allocation efficiency  | percentage |
| TE | Technical efficiency  | number |
| SeRp | Setup ratio  | percentage |
| UE | Utilization efficiency | percentage |



Transporter logger
--------------------

Folder name: transporter

Summarized CSV name:transporter_logger.csv

**Support kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| TTFp           | Time to failure in percent |  ration |
| TTRp   | Time to repair in percent  | ration |
| FE | Failure event  | number |
| CMTp | Corrective maintenance time in percent  | ration |
| AUSTp | Actual unit setup time in percent | ration |
| ADOTp | Actual unit down time in percent | ration |
| AUITp | Actual unit idle time in percent | ration |
| AUTTp |  Actual unit transportation time in percent | ration |

* ratio: KPI value / simulation time (time interval)

**Basic kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| A           | Availability |  percentage |
| AE   | Allocation efficiency  | percentage |
| TE | Technical efficiency  | number |
| SeR | Setup ratio  | percentage |
| UE | Utilization efficiency | percentage |


Queue fill level logger
-------------------------

Folder name: queue 

Summarized CSV name: queue_logger.csv

**Support kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| FillLevel    | Fill level |  percentage |

Transporter distribution logger
----------------------------------

Folder name: transporter_distribution
Summarized Csv name: transporter_distribution_logger.csv

**Support kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
|   | Distribution of travel between locations |  percentage |

Product analyse logger
-------------------------

Folder name: product

Summarized CSV name: product_logger.csv

**Support kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| WIP  | Work in process  | percentage |
| ATTp | Actual unit transportation time  | ratio |
| AQMTp | Actual unit queue machine time  | ratio |
| AUSTp | Actual unit setup time | ratio |
| APTp | Actual production time | ratio |
| AUSTnpp | Actual unit setup time not production | ratio |
| AUTTp |  Actual unit transportation time | ratio |
| PBTp |  Planned busy time | ratio |
| AOET | Actual unit order time | time |

AUST: The time used for the preparation, i.e. setup, of an order on a machine.
AUSTnpp: The time used for the preparation for loading and unloading a transporter.

* ratio: KPI value / AOET

**Basic kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| TR          | Throughput rate |  percentage |

**Info:**
 additional to the summarized and time logger, for every producted part the support kpis where calculated and saved under: `all_product_logger.csv`


Simulation logger
-------------------

Folder name: product

Summarized CSV name: product_logger.csv

**Support kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| WIP  | Work in process  | percentage |
| logging_time | logging time | time |


**Basic kpis**

| Abbreviation | Name  | Measurement |
| ------------ | ----  | ----------- |
| AR         | Allocation ratio |  percentage |
| PR         | Production process ratio |  percentage |


Event logger
-------------

> columns: ['name','time', 'time_diff', 'type_logger', 'additional_type', 'product',
                'position', 'position_info', 'machine', 'transport', 'process_id', 'location', 'task',
                'number_of_parts']

