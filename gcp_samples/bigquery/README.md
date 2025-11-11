Most BigQuery resources that you create — including tables, views, functions, and procedures — are created inside a dataset. Connections and jobs are exceptions; these are associated with projects rather than datasets.

A job is always associated with a project, but it doesn't have to run in the same project that contains the data.

Patterns
This section presents two common patterns for organizing BigQuery resources.

- Central data lake, department data marts. The organization creates a unified storage project to hold its raw data. Departments within the organization create their own data mart projects for analysis.

- Department data lakes, central data warehouse. Each department creates and manages its own storage project to hold that department's raw data. The organization then creates a central data warehouse project for analysis.

#### Central data lake, department data marts
In this pattern, you create a unified storage project to hold your organization's raw data. Your data ingestion pipeline can also run in this project. The unified storage project acts as a data lake for your organization.

Each department has its own dedicated project, which it uses to query the data, save query results, and create views. These department-level projects act as data marts. They are associated with the department's billing account.

Advantages of this structure include:

- A centralized data engineering team can manage the ingestion pipeline in a single place.
- The raw data is isolated from the department-level projects.
- With on-demand pricing, billing for running queries is charged to the department that runs the query.
- With capacity-based pricing, you can assign slots to each department based on their projected compute requirements.
- Each department is isolated from the others in terms of project-level quotas.

When using this structure, the following permissions are typical:

- The central data engineering team is granted the BigQuery Data Editor and BigQuery Job User roles for the storage project. These allow them to ingest and edit data in the storage project.
- Department analysts are granted the BigQuery Data Viewer role for specific datasets in the central data lake project. This allows them to query the data, but not to update or delete the raw data.
- Department analysts are also granted the BigQuery Data Editor role and Job User role for their department's data mart project. This allows them to create and update tables in their project and run query jobs, in order to transform and aggregate the data for department-specific usage.

#### Department data lakes, central data warehouse
In this pattern, each department creates and manages its own storage project, which holds that department's raw data. A central data warehouse project stores aggregations or transformations of the raw data.

Analysts can query and read the aggregated data from the data warehouse project. The data warehouse project also provides an access layer for business intelligence (BI) tools.

Advantages of this structure include:

- It is simpler to manage data access at the department level, by using separate projects for each department.
- A central analytics team has a single project for running analytics jobs, which makes it easier to monitor queries.
- Users can access data from a centralized BI tool, which is kept isolated from the raw data.
- Slots can be assigned to the data warehouse project to handle all queries from analysts and external tools.

When using this structure, the following permissions are typical:

- Data engineers are granted BigQuery Data Editor and BigQuery Job User roles in their department's data mart. These roles allow them to ingest and transform data into their data mart.
- Analysts are granted BigQuery Data Editor and BigQuery Job User roles in the data warehouse project. These roles allow them to create aggregate views in the data warehouse and run query jobs.
- Service accounts that connect BigQuery to BI tools are granted the BigQuery Data Viewer role for specific datasets, which can hold either raw data from the data lake or transformed data in the data warehouse project.

