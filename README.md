# Introduction
This project is a tool for lazy hackers. It has been done to automate some tasks with a tool easy to use with a web interface. 
# Component of this project
## OSINT tool
One of the component of this tool is a tool to make osint easyer.
You can set-up and automate and schedule multiple OSINT tasks like:
- Google search
- PGP key search
- DNS lookup
- Crawl websites
- Certificate Transparency logs search
- Shodan search

The web interface show the results in a way to make the analysis, correlation, and export of the datas as easy as possible.
### Example:
If you want to gather information about a domain name called example.com for example. You can set up 3 tasks:
- A DNS lookup on the domain example.com
- a Certificate Transparency search on example.com

Once those 2 tasks are created, you can run them imediatly. Or to follow changes on the infrastructure of thoses domains, you can create a job that will launch thoses 2 tasks every day.

When you need to look at the gathered data, you can view results of each task in the Results cathegory, or view all the data gathered in the Item cathegory.
In the Item cathegory, you can filter interesting data by type, date, or query.
Then you can launch other task from a data in Item, for example a shodan search on a domain obtained by DNS lookup.

After filtering for interesting data, you can export it in csv or pdf to share it to people or use the data in other tools.
## Search in local datasets tools
This component is to make the search in local dataset easy and fast. 
This tool use the sift program to run a fast search in text files (https://sift-tool.org/). sift is a tool that search much faster than grep.
### Example
If you have collected leaked databases in text format, you can put them in a folder in /usr/share/datasets/ folder.
Then just add a file called info.json in the folder of your added dataset, in this file keep metadata in json format about your dataset. ( you can see an example in example-db )

Then, in the tool you can refresh the datasets, it will show you the dataset you just added.
In the Search cathegory you can then search for a query and select in what dataset you want your search to be done.

As soon as the search end, the result will be available in the Result cathegory, with the metadata associated with the dataset where you found a result, letting you know for example what is the cipher algorithm for the hash found for example.

# Installation

