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
- **Analytics Engineering:** Implement dimensional modelling using dbt to create fact and dimension tables that are optimized for analytics.
- **Real-time Data Streaming:** Build a streaming data pipeline with Google Pub/Sub to handle incoming data streams in real-time.
- **Orchestration:** Orchestrate the pipelines with Mage deployed to Google Cloud Run.
- **Visualization:** Use Google Looker Studio for batch data and Grafana for data streams.

## Instructions
---
## 1. Set up Infrastructure using Terraform
Set up a Google Cloud Platform project and service account following the instructions [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md#initial-setup).

## 2. Deploy Mage to GCP with Terraform
Following the instructions from [Mage docs](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup). Make sure you have installed:
- terraform
- gcloud CLI

1. Clone [mage-ai-terraform-templates github repo](https://github.com/mage-ai/mage-ai-terraform-templates) and edit the /gcp/variables.tf file with your specific project details.

2. Change directory
<pre>
$ cd gcp
</pre>
3. Initialize Terraform
<pre>
$ terraform init
</pre>
4. Deploy
<pre>
$ terraform apply
</pre>
You will see a notification here if you have not enabled any Google Cloud API or resource. To do so, log in to your Cloud Console and use the search bar to find the resource you need to enable. Before retrying steps 3 and 4, make sure you:
<pre>
$ terraform destroy
</pre>
At this stage we can visit [Cloud Run](https://console.cloud.google.com/run?referrer=search&project=gothic-avenue-412217) on Google Cloud to view our Mage app. For this project, we have allowed all users to access our service [here](https://mage-tlblwyjvja-wl.a.run.app/overview), however we can whitelist only specific IPs.

As a final step, we can configure our Mage service to use our project's <code>GOOGLE APPLICATION CREDENTIALS</code> as a secret, using Google's Secret Manager and then allowing cloud run to access the secret, as described [here](https://cloud.google.com/run/docs/configuring/services/secrets#mounting-secrets-service).

## 3. Mage Pipelines
We can now create our **batch** load pipeline in Mage UI, that will generate synthetic data related to orders an online ecommerce marketplace receives. We name the pipeline <code>load_batch_to_bq</code>. [The pipeline](https://github.com/ManosPra/ecommerce_marketplace_data_pipeline/tree/main/mage_pipelines/batch_load) consists of a:
- Data Loader
- Transformer
- Data Exporter

that essentially are python files that generate synthetic data, then perform some data quality checks and finally load a dataframe to BigQuery.

We can now schedule this pipeline to run every day, simulating an end-to-end pipeline that loads raw data to our data lake.

## 4. Dimensional Modelling
At this stage of the project we are going to use dbt cloud to create fact and dimension tables based on the raw table we ingested to BigQuery with the batch load pipeline. More on dimensional modelling [here](https://docs.getdbt.com/terms/dimensional-modeling).
In dbt we initially create 4 models:
- [fact_orders](https://github.com/ManosPra/ecommerce_marketplace_data_pipeline/blob/main/dbt_modelling/models/fact_dimensions_modelling/fact_orders.sql) 
- [dim_customers](https://github.com/ManosPra/ecommerce_marketplace_data_pipeline/blob/main/dbt_modelling/models/fact_dimensions_modelling/dim_customers.sql)
- [dim_vendors](https://github.com/ManosPra/ecommerce_marketplace_data_pipeline/blob/main/dbt_modelling/models/fact_dimensions_modelling/dim_vendors.sql)
- [dim_products](https://github.com/ManosPra/ecommerce_marketplace_data_pipeline/blob/main/dbt_modelling/models/fact_dimensions_modelling/dim_products.sql)

forming a star-schema for our data-warehoue.
On top of these models, we are also creating an [orders daily aggregated table](https://github.com/ManosPra/ecommerce_marketplace_data_pipeline/blob/main/dbt_modelling/models/daily_agg/orders_daily_agg.sql) that holds information on orders pre-aggregated on a daily level, partitioned on <code>order_date</code>.

This type of modeling facilitates analytics queries and distinguishes the raw orders table we loaded in the previous step with the 5 tables we mentioned that are optimized for analysis purposes.
#### Generating Synthetic Data

The first pipeline generates synthetic ecommerce data. Here's an example of the data generation process:
