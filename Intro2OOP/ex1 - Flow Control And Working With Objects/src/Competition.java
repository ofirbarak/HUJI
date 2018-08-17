import org.omg.CORBA.PRIVATE_MEMBER;

import java.util.Scanner;

/**
 * The Competition class represents a Nim competition between two players, consisting of a given number of rounds. 
 * It also keeps track of the number of victories of each player.
 */
public class Competition {

    /* The Player objects representing the first player. */
    private Player player1;

    /* The Player objects representing the second player. */
    private Player player2;

    /* Victories of player 1 */
    private int player1Victories;

    /* Victories of player 2 */
    private int player2Victories;

    /* A flag indicating whether game play messages should be printed to the console. */
    private boolean displayMessage;

    /* Messages */
    private static final String STARTING_MESSAGE = "Starting a Nim competition of X rounds between a " +
            "TYPE1 player and a TYPE2 player.";
    private final String WELCOME_MESSAGE = "Welcome to the sticks game!";
    private final String PLAYER_TURN = "Player X, it is now your turn!";
    private final String ILIGAL_MOVE = "Invalid move. Enter another:";
    private final String MADE_MOVE = "Player X made the move: MOVE";
    private final String WON_MESSAGE = "Player X won!";
    private static final String RESAULT_MESSAGE = "The results are wins1:wins2";

	/* Constructor method */

    /**
     * Receives two Player objects, representing the two competing opponents, and a flag determining whether
     * messages should be displayed.
     * @param player1 - The Player objects representing the first player.
     * @param player2 - The Player objects representing the second player.
     * @param displayMessage - a flag indicating whether game play messages should be printed to the console.
     */
    Competition(Player player1, Player player2, boolean displayMessage){
        this.player1 = player1;
        this.player2 = player2;
        this.displayMessage = displayMessage;
        player1Victories = 0;
        player2Victories = 0;
    }

	/*
	 * Returns the integer representing the type of player 1; returns -1 on bad
	 * input.
	 */
	private static int parsePlayer1Type(String[] args){
		try{
			return Integer.parseInt(args[0]);
		} catch (Exception E){
			return -1;
		}
	}
	
	/*
	 * Returns the integer representing the type of player 2; returns -1 on bad
	 * input.
	 */
	private static int parsePlayer2Type(String[] args){
		try{
			return Integer.parseInt(args[1]);
		} catch (Exception E){
			return -1;
		}
	}
	
	/*
	 * Returns the integer representing the type of player 2; returns -1 on bad
	 * input.
	 */
	private static int parseNumberOfGames(String[] args){
		try{
			return Integer.parseInt(args[2]);
		} catch (Exception E){
			return -1;
		}
	}

	/**
	 * The method runs a Nim competition between two players according to the three user-specified arguments. 
	 * (1) The type of the first player, which is a positive integer between 1 and 4: 1 for a Random computer
	 *     player, 2 for a Heuristic computer player, 3 for a Smart computer player and 4 for a human player.
	 * (2) The type of the second player, which is a positive integer between 1 and 4.
	 * (3) The number of rounds to be played in the competition.
	 * @param args an array of string representations of the three input arguments, as detailed above.
	 */
	public static void main(String[] args) {
		
		int p1Type = parsePlayer1Type(args);
		int p2Type = parsePlayer2Type(args);
		int numGames = parseNumberOfGames(args);
        /* Create competition and players */
        Scanner scanner = new Scanner(System.in);
        Player player1 = new Player(p1Type, 1, scanner);
        Player player2 = new Player(p2Type, 2, scanner);
        Competition competition;
        if (p1Type == Player.HUMAN || p2Type == Player.HUMAN)
            competition = new Competition(player1, player2, true);
        else
            competition = new Competition(player1, player2, false);
        /*  Print 'Welcome' message
            Replace "X" in number of rounds,
            Replace "TYPE1" in player 1 type,
            Replace "TYPE2" in player 2 type
            And print it
         */
        System.out.println(STARTING_MESSAGE.replaceFirst("X", Integer.toString(numGames))
                .replaceFirst("TYPE1", player1.getTypeName()).replaceFirst("TYPE2", player2.getTypeName()));
        /* Runs N rounds */
        while (numGames > 0){
            int wonPlayerId = competition.fullSingleRound(competition, scanner);
            if (wonPlayerId == 1) {
                competition.player1Victories++;
            }
            else {
                competition.player2Victories++;
            }
            numGames--;
        }
        System.out.println(RESAULT_MESSAGE.replaceFirst("wins1",
                        Integer.toString(competition.player1Victories)).replaceFirst("wins2",
                        Integer.toString(competition.player2Victories)));
        scanner.close();
    }

    /**
     * Runs a full single round
     * @param competition competition object
     * @param scanner Scanner object
     * @return Id's player won
     */
    private int fullSingleRound(Competition competition, Scanner scanner){
        Board board = new Board(); // Create a board object
        if(displayMessage)
            System.out.println(WELCOME_MESSAGE);
        /* A flag indicating which player is playing this turn, true for player1, false for player 2 */
        boolean playerTurn = true;
        while(board.getNumberOfUnmarkedSticks() > 0){
            singleTurn(board, scanner, playerTurn);
            playerTurn = !playerTurn;
            //System.out.println(board.toString());
        }
        /* Print which player was won */
        if(displayMessage){
            int wonPlayerId = 1;
            if(!playerTurn)
                wonPlayerId = 2;
            System.out.println(WON_MESSAGE.replaceFirst("X", Integer.toString(wonPlayerId)));
        }
        if(playerTurn)
            return 1;
        else
            return 2;
    }

    /**
     * Runs a single turn
     * @param board game board
     * @param scanner Scanner object
     */
    private void singleTurn(Board board, Scanner scanner, boolean playerTurn){
        /* Print player turn*/
        if(this.displayMessage){
            String playerId;
            if(playerTurn)
                playerId = Integer.toString(player1.getPlayerId());
            else
                playerId = Integer.toString(player2.getPlayerId());
            System.out.println(PLAYER_TURN.replaceFirst("X", playerId));
        }
        /*
        Runs a loop until user gives a legal move
         */
        Move currentMove = (Move)null;
        int moveStatus = 0;
        do {
            if(moveStatus == -1 || moveStatus == -2)
                if(displayMessage)
                    System.out.println(ILIGAL_MOVE);
            if (playerTurn)
                currentMove = player1.produceMove(board);
            else
                currentMove = player2.produceMove(board);
            moveStatus = board.markStickSequence(currentMove);
        }
        while (moveStatus != 0);

        /* Print move */
        if(this.displayMessage){
            String playerId;
            if(playerTurn)
                playerId = Integer.toString(player1.getPlayerId());
            else
                playerId = Integer.toString(player2.getPlayerId());
            System.out.println(
                    MADE_MOVE.replaceFirst("X", playerId).replaceFirst("MOVE", currentMove.toString()));
        }
    }
}
