import java.util.Objects;
import java.util.Random;
import java.util.Scanner;


/**\
 * The Player class represents a player in the Nim game, producing Moves as a response to a Board state. Each player 
 * is initialized with a type, either human or one of several computer strategies, which defines the move he 
 * produces when given a board in some state. The heuristic strategy of the player is already implemented. You are 
 * required to implement the rest of the player types according to the exercise description.
 * @author OOP course staff
 */
public class Player {

	//Constants that represent the different players.
	/** The constant integer representing the Random player type. */
	public static final int RANDOM = 1;
	/** The constant integer representing the Heuristic player type. */
	public static final int HEURISTIC = 2;
	/** The constant integer representing the Smart player type. */
	public static final int SMART = 3;
	/** The constant integer representing the Human player type. */
	public static final int HUMAN = 4;

	/* Used by produceHeuristicMove() for binary representation of board rows. */
	private static final int BINARY_LENGTH = 4;
	
	private final int playerType;
	private final int playerId;
	private Scanner scanner;

    /* Messages */
    private final String DISPLAY_MESSAGE = "Press 1 to display the board. Press 2 to make a move:";
    private final String ENTER_A_ROW_NUMBER = "Enter the row number:";
    private final String ENTER_RIGHTMOST_STICK = "Enter the index of the rightmost stick:";
    private final String ENTER_LEFTMOST_STICK = "Enter the index of the leftmost stick:";
    private final String UNSUPPORTED_CMD_MESSAGE = "Unsupported command";
	
	/**
	 * Initializes a new player of the given type and the given id, and an initialized scanner.
	 * @param type The type of the player to create.
	 * @param id The id of the player (either 1 or 2).
	 * @param inputScanner The Scanner object through which to get user input
	 * for the Human player type. 
	 */
	public Player(int type, int id, Scanner inputScanner){		
		// Check for legal player type (we will see better ways to do this in the future).
		if (type != RANDOM && type != HEURISTIC 
				&& type != SMART && type != HUMAN){
			System.out.println("Received an unknown player type as a parameter"
					+ " in Player constructor. Terminating.");
			System.exit(-1);
		}		
		playerType = type;	
		playerId = id;
		scanner = inputScanner;
	}
	
	/**
	 * @return an integer matching the player type.
	 */	
	public int getPlayerType(){
		return playerType;
	}

	/**
	 * @return the players id number.
	 */	
	public int getPlayerId(){
		return playerId;
	}
	
	
	/**
	 * @return a String matching the player type.
	 */
	public String getTypeName(){
		switch(playerType){
			
			case RANDOM:
				return "Random";			    
	
			case SMART: 
				return "Smart";	
				
			case HEURISTIC:
				return "Heuristic";
				
			case HUMAN:			
				return "Human";
		}
		//Because we checked for legal player types in the
		//constructor, this line shouldn't be reachable.
		return "UnknownPlayerType";
	}
	
	/**
	 * This method encapsulates all the reasoning of the player about the game. The player is given the 
	 * board object, and is required to return his next move on the board. The choice of the move depends
	 * on the type of the player: a human player chooses his move manually; the random player should 
	 * return some random move; the Smart player can represent any reasonable strategy; the Heuristic 
	 * player uses a strong heuristic to choose a move. 
	 * @param board - a Board object representing the current state of the game.
	 * @return a Move object representing the move that the current player will play according to his strategy.
	 */
	public Move produceMove(Board board){
		
		switch(playerType){
		
			case RANDOM:
				return produceRandomMove(board);				
				    
			case SMART: 
				return produceSmartMove(board);
				
			case HEURISTIC:
				return produceHeuristicMove(board);
				
			case HUMAN:
				return produceHumanMove(board);

			//Because we checked for legal player types in the
			//constructor, this line shouldn't be reachable.
			default: 
				return null;			
		}
	}
	
	/*
	 * Produces a random move.
	 */
	private Move produceRandomMove(Board board){
		Random randomObject = new Random();
        int numberOfRows = board.getNumberOfRows();
        int randomRow;
        int numberOfSticksInRandomRow;
        int randomLeftBound;
        int randomRightBound;
        do {
            randomRow = randomObject.nextInt(numberOfRows) + 1;
            numberOfSticksInRandomRow = board.getRowLength(randomRow);
            randomLeftBound = randomObject.nextInt(numberOfSticksInRandomRow) + 1;
            if (randomLeftBound == numberOfSticksInRandomRow)
                randomRightBound = randomLeftBound;
            else
                if (numberOfSticksInRandomRow - randomLeftBound == 0)
                    randomRightBound = randomLeftBound;
                else
                    randomRightBound =
                            randomObject.nextInt(numberOfSticksInRandomRow - randomLeftBound + 1) +
                                    randomLeftBound;
        }
        while(checkAllSticksNotMarked(board, randomRow, randomLeftBound, randomRightBound));
        return new Move(randomRow, randomLeftBound, randomRightBound);
	}

    /**
     * Check if the boundaries are valid
     * @param board Board object
     * @param row row number
     * @param leftBound start marked move
     * @param rightBound end marked move
     * @return true - if the move is legal, false otherwise.
     */
    private boolean checkAllSticksNotMarked(Board board, int row, int leftBound, int rightBound){
        boolean isMarked = false;
        for(int i=leftBound; i <= rightBound && !isMarked; i++)
            isMarked = board.isStickUnmarked(row, i);
        return !isMarked;
    }
	
	/*
	 * Produce some intelligent strategy to produce a move
	 */
    private Move produceSmartMove(Board board) {
        boolean isSecondPlayer = this.getPlayerId() == 2;
        /* Calc the number of areas */
        int areas = 0;
        for (int row = 1; row <= board.getNumberOfRows(); row++) {
            for (int cell = 1; cell <= board.getRowLength(row); cell++) {
                if (board.isStickUnmarked(row, cell)) {
                    areas++;
                    while (board.isStickUnmarked(row, cell) && cell <= board.getRowLength(row))
                        cell++;
                }
            }
        }
        int rowNumberSize1 = 1; // row number in case of all areas = 1
        int leftBoundSize1 = 1; // left bound number in case of all areas = 1
        int rowNumber = 0; // row number to area > 1
        int leftBound = 1; // left bound to maybe an area > 1
        int length = 0; // length of bound to maybe an area > 1
        int lengths = 0; // length of the area > 1
        int leftBounds = 0; // left bound to maybe the area > 1
		/* Try to find area of size>1 */
        for (int row = 1; row <= board.getNumberOfRows() && rowNumber == 0; row++) {
            for (int cell = 1; cell <= board.getRowLength(row) && rowNumber == 0; cell++) {
                if (board.isStickUnmarked(row, cell)) {
                    length++;
                    if (length > 1 && rowNumber == 0) {
                        rowNumber = row;
                        leftBounds = cell - 1;
                        while (board.isStickUnmarked(row, cell) && cell <= board.getRowLength(row)) {
                            length++;
                            cell++;
                        }
                        lengths = length - 1;
                        break;
                    } else {
                        rowNumberSize1 = row;
                        leftBoundSize1 = cell;
                    }
                } else {
                    length = 0;
                    leftBound++;
                }
            }
            length = 0;
            leftBound = 1;
        }
        /*
        Check if we found an area > 1, if not it doesn't matter which one we choose
        if yes, check if our's Id = 2, if yes, check if number of areas are odd, if yes - do a move that
        won't change the parity number of areas, the opposite for even number of areas.
        All above happen opposite if our's Id = 1
         */
        if (lengths > 1) {
            if (isSecondPlayer) {
                if (areas % 2 != 0)
                    return new Move(rowNumber, leftBounds, leftBounds);
                else
                    return new Move(rowNumber, leftBounds, leftBounds + lengths - 1);
            } else {
                if (areas % 2 != 0)
                    return new Move(rowNumber, leftBounds, leftBounds);
                else
                    return new Move(rowNumber, leftBounds, leftBounds + lengths - 1);
            }
        }
        else
            return new Move(rowNumberSize1, leftBoundSize1, leftBoundSize1);
    }

	/*
	 * Interact with the user to produce his move.
	 */
	private Move produceHumanMove(Board board){
        int userCommand;
        int userRow;
        int userLeftBound;
        int userRightBound;
        System.out.println(DISPLAY_MESSAGE);
        userCommand = scanner.nextInt();
        while (userCommand != 2){ // Runs until user press 2 for enter a move
            if (userCommand == 1)
                System.out.println(board.toString());
            else
                System.out.println(UNSUPPORTED_CMD_MESSAGE);
            System.out.println(DISPLAY_MESSAGE);
            userCommand = scanner.nextInt();
        }
        /* Save the move */
        System.out.println(ENTER_A_ROW_NUMBER);
        userRow = scanner.nextInt();
        System.out.println(ENTER_LEFTMOST_STICK);
        userLeftBound = scanner.nextInt();
        System.out.println(ENTER_RIGHTMOST_STICK);
        userRightBound = scanner.nextInt();
        return new Move(userRow, userLeftBound, userRightBound);
    }
	
	/*
	 * Uses a winning heuristic for the Nim game to produce a move.
	 */
	private Move produceHeuristicMove(Board board){

		int numRows = board.getNumberOfRows();
		int[][] bins = new int[numRows][BINARY_LENGTH];
		int[] binarySum = new int[BINARY_LENGTH];
		int bitIndex,higherThenOne=0,totalOnes=0,lastRow=0,lastLeft=0,lastSize=0,lastOneRow=0,lastOneLeft=0;
		
		for(bitIndex = 0;bitIndex<BINARY_LENGTH;bitIndex++){
			binarySum[bitIndex] = 0;
		}
		
		for(int k=0;k<numRows;k++){
			
			int curRowLength = board.getRowLength(k+1);
			int i = 0;
			int numOnes = 0;
			
			for(bitIndex = 0;bitIndex<BINARY_LENGTH;bitIndex++){
				bins[k][bitIndex] = 0;
			}
			
			do {
				if(i<curRowLength && board.isStickUnmarked(k+1,i+1) ){
					numOnes++;
				} else {
					
					if(numOnes>0){
						
						String curNum = Integer.toBinaryString(numOnes);
						while(curNum.length()<BINARY_LENGTH){
							curNum = "0" + curNum;
						}
						for(bitIndex = 0;bitIndex<BINARY_LENGTH;bitIndex++){
							bins[k][bitIndex] += curNum.charAt(bitIndex)-'0'; //Convert from char to int
						}
						
						if(numOnes>1){
							higherThenOne++;
							lastRow = k +1;
							lastLeft = i - numOnes + 1;
							lastSize = numOnes;
						} else {
							totalOnes++;
						}
						lastOneRow = k+1;
						lastOneLeft = i;
						
						numOnes = 0;
					}
				}
				i++;
			}while(i<=curRowLength);
			
			for(bitIndex = 0;bitIndex<BINARY_LENGTH;bitIndex++){
				binarySum[bitIndex] = (binarySum[bitIndex]+bins[k][bitIndex])%2;
			}
		}
		
		
		//We only have single sticks
		if(higherThenOne==0){
			return new Move(lastOneRow,lastOneLeft,lastOneLeft);
		}
		
		//We are at a finishing state				
		if(higherThenOne<=1){
			
			if(totalOnes == 0){
				return new Move(lastRow,lastLeft,lastLeft+(lastSize-1) - 1);
			} else {
				return new Move(lastRow,lastLeft,lastLeft+(lastSize-1)-(1-totalOnes%2));
			}
			
		}
		
		for(bitIndex = 0;bitIndex<BINARY_LENGTH-1;bitIndex++){
			
			if(binarySum[bitIndex]>0){
				
				int finalSum = 0,eraseRow = 0,eraseSize = 0,numRemove = 0;
				for(int k=0;k<numRows;k++){
					
					if(bins[k][bitIndex]>0){
						eraseRow = k+1;
						eraseSize = (int)Math.pow(2,BINARY_LENGTH-bitIndex-1);
						
						for(int b2 = bitIndex+1;b2<BINARY_LENGTH;b2++){
							
							if(binarySum[b2]>0){
								
								if(bins[k][b2]==0){
									finalSum = finalSum + (int)Math.pow(2,BINARY_LENGTH-b2-1);
								} else {
									finalSum = finalSum - (int)Math.pow(2,BINARY_LENGTH-b2-1);
								}
								
							}
							
						}
						break;
					}
				}
				
				numRemove = eraseSize - finalSum;
				
				//Now we find that part and remove from it the required piece
				int numOnes=0,i=0;
				while(numOnes<eraseSize){

					if(board.isStickUnmarked(eraseRow,i+1)){
						numOnes++;
					} else {
						numOnes=0;
					}
					i++;
					
				}
				return new Move(eraseRow,i-numOnes+1,i-numOnes+numRemove);
			}
		}
		
		//If we reached here, and the board is not symmetric, then we only need to erase a single stick
		if(binarySum[BINARY_LENGTH-1]>0){
			return new Move(lastOneRow,lastOneLeft,lastOneLeft);
		}
		
		//If we reached here, it means that the board is already symmetric, and then we simply mark one
		// stick from the last sequence we saw:
		return new Move(lastRow,lastLeft,lastLeft);		
	}
	
	
}
