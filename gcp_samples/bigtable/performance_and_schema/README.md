# Performance and schema design notes

A cluster's performance scales linearly as you add nodes to the cluster

When the amount of data stored in a cluster increases, bigtable optimizes the storage by distributing the amount of data across all the nodes in the cluster.

When storage utilization increases, workloads can experience an increase in query processing latency even if the cluster has enough nodes to meet overall CPU needs. This is because the higher the storage per node, the more background work such as indexing is required. The increase in background work to handle more storage can result in higher latency and lower throughput.

Cold starts and low QPS can increase latency. Bigtable performs best with large tables that are frequently accessed. For this reason, if you start sending requests after a period of no usage (a cold start), you might observe high latency while Bigtable reestablishes connections. Latency is also higher when QPS is low.

igtable shards the data into multiple tablets, which can be moved between nodes in your Bigtable cluster. This storage method enables Bigtable to use two different strategies for optimizing your data over time:

1. Bigtable tries to store roughly the same amount of data on each Bigtable node.
2. Bigtable tries to distribute reads and writes equally across all Bigtable nodes.

Sometimes these strategies conflict with one another. For example, if one tablet's rows are read extremely frequently, Bigtable might store that tablet on its own node, even though this causes some nodes to store more data than others.

As part of this process, Bigtable might also split a tablet into two or more smaller tablets, either to reduce a tablet's size or to isolate hot rows within an existing tablet.

Bigtable shards the table's data into tablets. Each tablet contains a contiguous range of rows within the table. If you have written less than several GB of data to the table, Bigtable stores all of the tablets on a single node within your cluster.

As more tablets accumulate, Bigtable moves some of them to other nodes in the cluster so that the amount of data is balanced more evenly across the cluster.

If you've designed your schema correctly, then reads and writes should be distributed fairly evenly across your entire table. However, there are some cases where you can't avoid accessing certain rows more frequently than others. Bigtable helps you deal with these cases by taking reads and writes into account when it balances tablets across nodes.

If you're running a performance test for an application that depends on Bigtable, follow these guidelines as you plan and execute your test:

- Test with enough data.
  - If the tables in your production instance contain a total of 100 GB of data or less per node, test with a table of the same amount of data.
  - If the tables contain more than 100 GB of data per node, test with a table that contains at least 100 GB of data per node. For example, if your production instance has one four-node cluster, and the tables in the instance contain a total of 1 TB of data, run your test using a table of at least 400 GB.
- Test with a single table.
- Stay below the recommended storage utilization per node. For details, see Storage utilization per node.
- Before you test, run a heavy pre-test for several minutes. This step gives Bigtable a chance to balance data across your nodes based on the access patterns it observes.
- Run your test for at least 10 minutes. This step lets Bigtable further optimize your data, and it helps ensure that you will test reads from disk as well as cached reads from memory.

