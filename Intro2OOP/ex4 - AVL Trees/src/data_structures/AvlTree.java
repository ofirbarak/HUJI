package oop.ex4.data_structures;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * Class that implements an AVL Tree data structure.
 */
public class AvlTree implements Iterable<Integer>{
    private Node _root; // The root of the tree.

    /* -- Methods -- */
    /** Constructors */
    /**
     * The default constructor.
     */
    public AvlTree(){
        _root = null;
    }

    /**
     * A constructor that builds a new AVL tree containing all unique values in the input array.
     * @param data the values to add to tree.
     */
    public AvlTree(int[] data){
        if (data != null)
            BuildAvl(data, 0);
    }

    private void BuildAvl(int[] data, int start){
        if (start < data.length) {
            add(data[start]);
            BuildAvl(data, start+1);
        }
    }

    /**
     * A copy constructor that creates a deep copy of the given AvlTree. The new tree contains all the
     * values of the given tree, but not necessarily in the same structure.
     * @param tree The AVL tree to be copied.
     */
    public AvlTree(AvlTree tree){
        if (tree != null)
            buildCopyAvlTreeHelper(tree._root);
    }

    private void buildCopyAvlTreeHelper(Node node){
        if (node != null) {
            add(node.getKey());
            buildCopyAvlTreeHelper(node.getLeftChild());
            buildCopyAvlTreeHelper(node.getRightChild());
        }
    }

    /** Instance methods */
    /**
     * Add a new node with the given key to the tree.
     * @param newValue the value of the new node to add.
     * @return true if the value to add is not already in the tree and it was successfully added,
     *  false otherwise.
     */
    public boolean add(int newValue){
        try {
            _root = insertNewNode(_root, newValue);
            return true;
        }
        catch (Exception e){
            return false;
        }
    }

    private Node insertNewNode(Node currentNode, int newValue) throws Exception {
        if (currentNode == null)
            return new Node(newValue);
        if (currentNode.compareTo(newValue) == 0)
            throw new Exception();
        else if (currentNode.compareTo(newValue) < 0)
            currentNode.setNewRightChild(insertNewNode(currentNode.getRightChild(), newValue));
        else
            currentNode.setNewLeftChild(insertNewNode(currentNode.getLeftChild(), newValue));
        // Checking balanced factor
        return checkBalancedFactor(currentNode);
    }

    private Node checkBalancedFactor(Node node){
        if (Math.abs(node.getBalanceFactor()) <= 1)
            return node;
        if (node.getBalanceFactor() > 0) { // Violation in the right subTree
            Node rightChild = node.getRightChild();
            if (rightChild.getBalanceFactor() < 0)
                rightRotate(rightChild);
            return leftRotate(node);
        }
        else { // Violation in the left subTree
            Node leftChild = node.getLeftChild();
            if (leftChild.getBalanceFactor() > 0)
                leftRotate(leftChild);
            return rightRotate(node);
        }
    }

    private Node leftRotate(Node node){
        Node nodeParent = node.getParent();
        Node newSubRoot = node.getRightChild();
        node.setNewRightChild(newSubRoot.getLeftChild());
        newSubRoot.setNewLeftChild(node);
        newSubRoot.setNewParent(nodeParent);
        return newSubRoot;
    }

    private Node rightRotate(Node node){
        Node nodeParent = node.getParent();
        Node newSubRoot = node.getLeftChild();
        node.setNewLeftChild(newSubRoot.getRightChild());
        newSubRoot.setNewRightChild(node);
        newSubRoot.setNewParent(nodeParent);
        return newSubRoot;
    }

    /**
     * Check whether the tree contains the given input value.
     * @param searchVal value to search for
     * @return if val is found in the tree, return the depth of the node (0 for the root) with the given
     *  value if it was found in the tree, -1 otherwise.
     */
    public int contains(int searchVal){
        try {
            return containsHelper(searchVal, _root);
        }
        catch (Exception e) {
            return -1;
        }
    }

    private int containsHelper(int searchVal, Node node) throws Exception{
        if (node == null)
            throw new NoSuchElementException();
        if (node.compareTo(searchVal) == 0)
            return 0;
        if (node.compareTo(searchVal) < 0)
            return containsHelper(searchVal, node.getRightChild()) + 1;
        else
            return containsHelper(searchVal, node.getLeftChild()) + 1;
    }

    /**
     * Removes the node with the given value from the tree, if it exists.
     * @param toDelete the value to remove from the tree.
     * @return true if the given value was found and deleted, false otherwise.
     */
    public boolean delete(int toDelete){
       try {
           _root = deleteHelper(_root, toDelete);
           return true;
       }
       catch (Exception e){
           return false;
       }
    }

    private Node deleteHelper(Node currentNode, int toDelete) throws Exception{
        if (currentNode == null)
            throw new NoSuchElementException();
        if (currentNode.compareTo(toDelete) == 0)
            return deleteNodeHelper(currentNode);
        else if (currentNode.compareTo(toDelete) < 0)
            currentNode.setNewRightChild(deleteHelper(currentNode.getRightChild(), toDelete));
        else
            currentNode.setNewLeftChild(deleteHelper(currentNode.getLeftChild(), toDelete));
        // Checking balanced factor
        return checkBalancedFactor(currentNode);
    }

    // returns the replacing node
    private Node deleteNodeHelper(Node nodeToDelete){
        if (nodeToDelete.isALeaf())
            return null;
        else if (nodeToDelete.getRightChild() == null) // If node has one children
            return nodeToDelete.getLeftChild();
        else if (nodeToDelete.getLeftChild() == null)  // If node has one children
            return nodeToDelete.getRightChild();
        else {
            /* Successor exists because nodeToDelete has 2 children */
            Node successor = extractSuccessor(nodeToDelete);
            successor.setNewLeftChild(nodeToDelete.getLeftChild());
            successor.setNewRightChild(nodeToDelete.getRightChild());
            return successor;
        }
    }

    private Node successor(Node node){
        return findMinimum(node.getRightChild());
    }

    private Node extractSuccessor(Node node){
        Node successor = successor(node);
        if (successor.getParent() == node)
            node.setNewRightChild(successor.getRightChild());
        else
            successor.getParent().setNewLeftChild(successor.getRightChild());
        return successor;
    }

    private Node findMinimum(Node node){
        if (node.getLeftChild() == null)
            return node;
        return findMinimum(node.getLeftChild());
    }

    /**
     * Returns the number of nodes in the tree.
     * @return the number of nodes in the tree.
     */
    public int size(){
        return sizeHelper(_root);
    }

    private int sizeHelper(Node node){
        if (node == null)
            return 0;
        return sizeHelper(node.getRightChild()) + sizeHelper(node.getLeftChild()) + 1;
    }

    private ArrayList<Node> inOrderTravel(Node node){
        if (node == null)
            return new ArrayList<>();
        ArrayList<Node> arrayList = new ArrayList<>();
        arrayList.addAll(inOrderTravel(node.getLeftChild()));
        arrayList.add(node);
        arrayList.addAll(inOrderTravel(node.getRightChild()));
        return arrayList;
    }

    /**
     * @return an iterator for the Avl Tree. The returned iterator iterates over the tree nodes in an
     *  ascending order, and does NOT implement the remove() method.
     */
    public Iterator<Integer> iterator(){
        return new AvlIterator();
    }

    private final class AvlIterator implements Iterator<Integer>{
        private int _index;
        private ArrayList<Node> _nodes;

        private AvlIterator(){
            _index = 0;
            _nodes = inOrderTravel(_root);
        }

        @Override
        public boolean hasNext() {
            return _index < _nodes.size();
        }

        @Override
        public Integer next() throws NoSuchElementException{
            return _nodes.get(_index++).getKey();
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException();
        }
    }

    /* Static methods -- */
    /**
     * Calculates the minimum number of nodes in an AVL tree of height h.
     * @param h the height of the tree (a non-negative number) in question.
     * @return the minimum number of nodes in an AVL tree of the given height.
     */
    public static int findMinNodes(int h){
        return (int)(Math.round(((Math.sqrt(5)+2)/
                Math.sqrt(5))*Math.pow((1+
                Math.sqrt(5))/2,h)-1));
    }
}
