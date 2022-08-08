# A Demo for Multi-dimensional Query

## Introduction
This is an implementation of the paper [SIGMOD'19_Answering multi-dimensional analytical queries under local differential privacy](https://par.nsf.gov/servlets/purl/10194803).
We build a demo for the users to get started. 

## About Demo
The demo includes configuration, running scripts and dataset.

### Configuration
The demo is consisted of one server and three clients.
The configuration is placed in `federatedscope/db/demo/mda/${role}.yaml`, where `${role}` is the name of the participant, and you can choose from `server`, `client1`, `client2` and `client3`. 
You can run them by the following command
```bash
bash run.sh ${role}
```
Note that we should first run the server to setup the service.

### Dataset
For simplicity, we provide scripts for data generation. 
Specifically, run the following command to generate dataset
```bash
python generator.py
```
The dataset is generated in csv format, and named by the `${role}` of the participants. 
You can find the in `federatedscope/db/demo/mda/data/`. 
Except the dataset for different participants, we also generate a dataset named `dataset.csv`, which is the global dataset without local differential privacy. 
You can find the ground truth easily by executing query on this dataset. 

The schema of the server dataset is as follows
```
| id | activatetime | purchase |
```
`id` is the primary key, `activatetime` and `purchase` is the time and money that the users spend on the service.
The schema of the clients are 
```
| id | age | salary | state | os |
```