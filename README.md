# DataTalks.Club Data Engineering Zoomcamp
Final Project 2024 Cohort

**Note:** This project was developed as the final step for the completion of the Data Engineering Zoomcamp offered by DataTalksClub.

---

## Ecommerce Marketplace Data Engineering Pipeline

Ecommerce marketplaces generate vast amounts of data daily, including customer transactions, product information, and user interactions. Managing and analyzing this data efficiently is crucial for optimizing business operations, understanding customer behavior, and driving growth. 

The goal of this project is to design and implement a data engineering pipeline tailored for an ecommerce marketplace. This pipeline should efficiently handle both batch and streaming data processing, ensuring data quality. Additionally, it should support the creation of analytics-ready datasets and facilitate insights generation for stakeholders.

Key aspects to address include:

- **Data Generation:** Generate realistic synthetic data representative of ecommerce transactions, customer interactions, and product catalog changes.
- **Data Processing:** Implement a batch processing pipeline to handle large volumes of historical data efficiently and load in a Google BigQuery data lake.
- **Analytics Engineering:** Implement dimensional modelling using dbt to create fact and dimension tables.
- **Real-time Data Streaming:** Build a streaming data pipeline with Google Pub/Sub to handle incoming data streams in real-time.
- **Orchestration:** Orchestrate the pipelines with Mage deployed to Google Cloud Run.
- **Visualization:** Use Google Looker Studio for batch data and Grafana for data streams.

## Instructions
---
## 1. Set up Infrastructure using Terraform
Set up a Google Cloud Platform project and service account following the instructions [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md#initial-setup)

## 2. Deploy Mage to GCP with Terraform
Following the instructions from [Mage docs](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup). Make sure you have installed:
- terraform
- gcloud CLI

**1.** Clone [mage-ai-terraform-templates github repo](https://github.com/mage-ai/mage-ai-terraform-templates) and edit the /gcp/variables.tf file with your specific project details.

**2.** Change directory
<pre>
$ cd gcp
</pre>
**3.** Initialize Terraform
<pre>
$ terraform init
</pre>
**4.** Deploy
<pre>
$ terraform apply
</pre>
You will see a notification here if you have not enabled any Google Cloud API or resource. To do so, log in to your Cloud Console and use the search bar to find the resource you need to enable. Before retrying steps 3 and 4, make sure you:

At this stage we can visit 
<pre>
$ terraform destroy
</pre>


#### Generating Synthetic Data

The first pipeline generates synthetic ecommerce data. Here's an example of the data generation process:
