import java.util.TreeSet;
import java.util.HashSet;
import java.util.LinkedList;

/**
 * has a main method that measures the run-times requested in the
 * “Performance Analysis” section.
 */
public class SimpleSetPerformanceAnalyzer {
    private static final int COLLECTIONS_WARM_UP = 70000;
    private static final int LIST_WARM_UP = 7000;
    private static final int CONVERT_TO_MILI = 1000000;

    public static void main(String args[]){
        SimpleSet[] dataStructures = new SimpleSet[5];
        initializeDataStructures(dataStructures);
        String[] data1 = Ex3Utils.file2array("data1.txt");
        String[] data2 = Ex3Utils.file2array("data2.txt");

        System.out.println("Adding all words from data1.txt");
        //data1
        for (int i=1; i < dataStructures.length; i++)
            printTimeToRunAddOnData(data1, dataStructures[i]);
        initializeDataStructures(dataStructures);

        System.out.println("Adding all words from data2.txt");
        //data2
        for (int i=0; i < dataStructures.length; i++)
            printTimeToRunAddOnData(data2, dataStructures[i]);
        initializeDataStructuresWithData(data1, dataStructures);

        System.out.println("Contains(hi) with initialize data1.txt");
        // Contains("hi")
        for (int i=0; i < dataStructures.length; i++)
            preformContainsString("hi", dataStructures[i]);
        System.out.println("Contains(-13170890158) with initialize data1.txt");
        // Contains("-13170890158")
        for (int i=0; i < dataStructures.length; i++)
            preformContainsString("-13170890158", dataStructures[i]);

        initializeDataStructuresWithData(data2, dataStructures);

        System.out.println("Contains(23) with initialize data2.txt");
        // Contains("23")
        for (int i=0; i < dataStructures.length; i++)
            preformContainsString("23", dataStructures[i]);
        System.out.println("Contains(hi) with initialize data2.txt");
        // Contains("hi")
        for (int i=0; i < dataStructures.length; i++)
            preformContainsString("hi", dataStructures[i]);

    }

    private static void initializeDataStructuresWithData(String[] data, SimpleSet[] dataStructures){
        dataStructures[0] = new OpenHashSet(data);
        dataStructures[1] = new ClosedHashSet(data);
        dataStructures[2] = new CollectionFacadeSet(new TreeSet<>());
        addElements(data, dataStructures[2]);
        dataStructures[3] = new CollectionFacadeSet(new LinkedList<>());
        addElements(data, dataStructures[3]);
        dataStructures[4] = new CollectionFacadeSet(new HashSet<>());
        addElements(data, dataStructures[4]);
    }

    private static void initializeDataStructures(SimpleSet[] dataStructures){
        dataStructures[0] = new OpenHashSet();
        dataStructures[1] = new ClosedHashSet();
        dataStructures[2] = new CollectionFacadeSet(new TreeSet<>());
        dataStructures[3] = new CollectionFacadeSet(new LinkedList<>());
        dataStructures[4] = new CollectionFacadeSet(new HashSet<>());
    }

    private static void addElements(String[] data, SimpleSet set){
        for (int index=0; index < data.length; index++)
            set.add(data[index]);
    }

    private static void printTimeToRunAddOnData(String[] data, SimpleSet set) {
        long timeBefore;
        long timeAfter;
        long timeToRunInMili;
        timeBefore = System.nanoTime();
        addElements(data, set);
        timeAfter = System.nanoTime();
        timeToRunInMili = (timeAfter-timeBefore)/CONVERT_TO_MILI;
        System.out.println(timeToRunInMili);
    }

    private static void preformContainsString(String string, SimpleSet set){
        int warmUp = COLLECTIONS_WARM_UP;
        if (set instanceof LinkedList)
            warmUp = LIST_WARM_UP;
        long timeBeforeWithOutWarmUp = System.nanoTime();
        for (int i=0; i < warmUp; i++)
            set.contains(string);
        long timeBefore = System.nanoTime();
        for (int i=0; i < warmUp; i++)
            set.contains(string);
        long timeAfter = System.nanoTime();
        long timeWithWarmUp = (timeAfter-timeBefore)/warmUp;
        long timeWithoutWarmUp = (timeAfter-timeBeforeWithOutWarmUp)/warmUp;
        System.out.println("Actual: " + timeWithWarmUp +
                ", without warm-up: " + timeWithoutWarmUp +
                ", the difference: " + (timeWithoutWarmUp-timeWithWarmUp));
    }
}
