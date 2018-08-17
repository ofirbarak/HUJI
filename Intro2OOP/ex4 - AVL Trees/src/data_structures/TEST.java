package oop.ex4.data_structures;

import java.util.Iterator;

/**
 * Created by Meital on 4/19/2016.
 */
public class TEST {
    public static void main(String[] args){
        int [] arr = {};
        AvlTree avl = new AvlTree(arr);
        //int [] arr = null;//2,3,8,4,1,6,5,7};
        /*System.out.println(arr);

        System.out.println(avl.size());
        System.out.println(avl.contains(1));
        System.out.println(avl.contains(2));
        System.out.println(avl.contains(3));
        System.out.println(avl.contains(4));
        System.out.println(avl.contains(5));
        System.out.println(avl.contains(6));
        System.out.println(avl.contains(7));
        System.out.println(avl.contains(8));

        System.out.println(avl.findMinNodes(10));*/
        avl.add(5);
        avl.add(7);
        avl.add(3);
        avl.add(4);
        avl.add(8);
        avl.add(6);
        avl.add(9);
        avl.delete(7);
        System.out.print(AvlTree.findMinNodes(10));
    }
}


