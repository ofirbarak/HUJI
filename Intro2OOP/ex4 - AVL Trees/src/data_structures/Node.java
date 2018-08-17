package oop.ex4.data_structures;

/**
 * Class that represents a Node in a tree. Every node contains 3 pointers - parent, and the children
 */
class Node implements Comparable<Integer>{
    private Node _parent;
    private Node _leftChild;
    private Node _rightChild;
    private Integer _key;
    private int _height;

    /*
     * Creates an empty new Node.
     */
    Node(int keyNode) {
        _parent = null;
        _leftChild = null;
        _rightChild = null;
        _key = keyNode;
        _height = 0;
    }

    /*
     * Sets the node a new parent.
     * @param newParent the new parent.
     */
    void setNewParent(Node newParent){
        if (newParent != null) {
            if (newParent._leftChild == _parent)
                newParent.setNewLeftChild(this);
            else
                newParent.setNewRightChild(this);
        }
        else
            _parent = null;
    }

    /*
     * Change the right child.
     * @param newRightChild the new right child.
     */
    void setNewRightChild(Node newRightChild){
        if (newRightChild != null) {
            _rightChild = newRightChild;
            newRightChild._parent = this;
        }
        else
            _rightChild = null;
        updateHeight();
    }

    /*
     * Change the left child.
     * @param newLeftChild the new left child.
     */
    void setNewLeftChild(Node newLeftChild){
        if (newLeftChild != null) {
            _leftChild = newLeftChild;
            newLeftChild._parent = this;
        }
        else
            _leftChild = null;
        updateHeight();
    }

    /*
     * Returns the node's key.
     * @return node's key.
     */
    int getKey(){
        return _key;
    }

    Node getLeftChild(){
        return _leftChild;
    }

    Node getRightChild(){
        return _rightChild;
    }

    Node getParent(){
        return _parent;
    }

    boolean isALeaf(){
        return _rightChild == null && _leftChild == null;
    }

    /*
    Returns +1 for right
            -1 for left
            0 for balanced
     */
    int getBalanceFactor() {
        int rightChildHeight = _rightChild == null ? -1 : _rightChild._height;
        int leftChildHeight = _leftChild == null ? -1 : _leftChild._height;
        return rightChildHeight - leftChildHeight;
    }

    void updateHeight(){
        if (isALeaf())
            _height = 0;
        else {
            int rightChildHeight = _rightChild == null ? -1 : _rightChild._height;
            int leftChildHeight = _leftChild == null ? -1 : _leftChild._height;
            _height = Math.max(leftChildHeight, rightChildHeight) + 1;
        }
    }

    @Override
    public int compareTo(Integer o) {
        return _key.compareTo(o);
    }
}
