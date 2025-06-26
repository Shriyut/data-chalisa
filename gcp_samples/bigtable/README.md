# Notes related to bigtable

A single value in each row in indexed by rowkey

Bigtable is ideal for storing large amounts of single-keyed data with low latency

Each node in the cluster handles a subset of the requests to the cluster. By adding nodes to a cluster, you can increase the number of simultaneous requests that the cluster can handle. Adding nodes also increases the maximum throughput for the cluster. If you enable replication by adding additional clusters, you can also send different types of traffic to different clusters. Then if one cluster becomes unavailable, you can fail over to another cluster.

A Bigtable table is sharded into blocks of contiguous rows, called tablets, to help balance the workload of queries. (Tablets are similar to HBase regions.) Tablets are stored on Colossus, Google's file system, in SSTable format. An SSTable provides a persistent, ordered immutable map from keys to values, where both keys and values are arbitrary byte strings. Each tablet is associated with a specific Bigtable node. In addition to the SSTable files, all writes are stored in Colossus's shared log as soon as they are acknowledged by Bigtable, providing increased durability.

Columns that are not used in a Bigtable row don't take up any space in that row. Each row is essentially a collection of key-value entries, where the key is a combination of the column family, column qualifier and timestamp. If a row does not include a value for a specific column, the key-value entry is not present.

Each Bigtable zone is managed by a primary process, which balances workload and data volume within clusters. This process splits busier or larger tablets in half and merges less-accessed/smaller tablets together, redistributing them between nodes as needed. If a certain tablet gets a spike of traffic, Bigtable splits the tablet in two, then moves one of the new tablets to another node. Bigtable manages the splitting, merging, and rebalancing automatically, saving you the effort of manually administering your tablets.

By default, Bigtable uses cluster nodes for both storage and compute. For high-throughput read jobs, you can use Data Boost for Bigtable for compute. Data Boost lets you send large read jobs and queries using serverless compute while your core application continues using cluster nodes for compute. 

Bigtable periodically rewrites your tables to remove deleted entries, and to reorganize your data so that reads and writes are more efficient. This process is known as a compaction. There are no configuration settings for compactions—Bigtable compacts your data automatically.

Column qualifiers take up space in a row, since each column qualifier used in a row is stored in that row. As a result, it's often efficient to use column qualifiers as data.


Mutations, or changes, to a row take up extra storage space, because Bigtable stores mutations sequentially and compacts them only periodically. When Bigtable compacts a table, it removes values that are no longer needed. If you update the value in a cell, both the original value and the new value will be stored on disk for some amount of time until the data is compacted.

Deletions also take up extra storage space, at least in the short term, because deletions are actually a specialized type of mutation. Until the table is compacted, a deletion uses extra storage rather than freeing up space.

- Random data cannot be compressed as efficiently as patterned data. Patterned data includes text, such as the page you're reading right now.
- Compression works best if identical values are near each other, either in the same row or in adjoining rows. If you arrange your row keys so that rows with identical chunks of data are next to each other, the data can be compressed efficiently.
- Bigtable compresses values that are up to 1 MiB in size. If you store values that are larger than 1 MiB, compress them before writing them to Bigtable, so you can save CPU cycles, server memory, and network bandwidth.

Single-cluster Bigtable instances provide strong consistency. By default, instances that have more than one cluster provide eventual consistency, but for some use cases they can be configured to provide read-your-writes consistency or strong consistency, depending on the workload and app profile settings.

By default, all data stored within Google Cloud, including the data in Bigtable tables, is encrypted at rest using the same hardened key management systems that we use for our own encrypted data.

Bigtable provides change data capture (CDC) in the form of change streams. Change streams let you capture and stream out data changes to a table as the changes happen. You can read a change stream using a service such as Dataflow to support use cases including data analytics, audits, archiving requirements, and triggering downstream application logic. 

App profile routing policies let you control which clusters handle incoming requests from your applications. Options for routing policies include the following:

- Single-cluster routing: sends all requests to a single cluster.
- Multi-cluster routing to any cluster: sends requests to the nearest available cluster in an instance, including the following options:
- - Any cluster: any cluster in the instance can receive requests.
- - Cluster group routing: a specified group of clusters in the instance can receive requests.

If you need interactive querying in an online analytical processing (OLAP) system, consider BigQuery.
If you must store highly structured objects in a document database, with support for ACID transactions and SQL-like queries, consider Firestore.
For in-memory data storage with low latency, consider Memorystore.
To sync data between users in real time, consider the Firebase Realtime Database.

