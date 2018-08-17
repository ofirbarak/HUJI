/**
 * The Move class represents a move in the Nim game.
 */
public class Move {

    /*  The row of which to applied */
    private int boardRow;

    /* The left bound */
    private int leftBoardBound;

    /* The right bound */
    private int rightBoardBound;

    /* Constructors methods */

    /**
     * The class constructor, which receives the parameters defining the move.
     * @param inRow - The row of which to applied
     * @param inLeft - The left bound
     * @param inRight - The right bound
     */
    public Move(int inRow,int inLeft,int inRight){
        boardRow = inRow;
        leftBoardBound = inLeft;
        rightBoardBound = inRight;
    }

    /* Instance methods */

    /**
     * Returns a string representation of the move. For example, if the row for the move is 2, the left
     * bound is 3 and the right bound is 5, this method will return the string ”2:3-5” (without any spaces).
     * @return - a string representation of the move.
     */
    public String toString(){
        return Integer.toString(boardRow) + ':' + Integer.toString(leftBoardBound) + '-' +
                Integer.toString(rightBoardBound);
    }

    /**
     * Returns the row on which the move is performed.
     * @return - the row on which the move is performed.
     */
    public int getRow(){
        return boardRow;
    }

    /**
     * Returns the left bound of the stick sequence to mark.
     * @return - the left bound of the stick sequence to mark.
     */
    public int getLeftBound(){
        return leftBoardBound;
    }

    /**
     * Returns right bound of the stick sequence to mark.
     * @return - right bound of the stick sequence to mark.
     */
    public int getRightBound(){
        return rightBoardBound;
    }
}
