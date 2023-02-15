package org.example.Flink;

import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;

import java.util.List;

public class FlinkMain {
    public static void main(String[] args) throws Exception {
        //flink transformations are lazy i.e. they are not executed until a sink operation is invoked
        ExecutionEnvironment env
                = ExecutionEnvironment.getExecutionEnvironment();

        DataSet<Integer> amounts = env.fromElements(1, 29, 40, 50);

        int threshold = 30;
        List<Integer> collect = amounts
                .filter(a -> a > threshold)
                //.reduce((integer, t1) -> integer + t1)
                .collect();



        System.out.print(collect);
    }
}
