import oop.ex2.*;

/* It is used by the supplied driver to create all the spaceship objects
    according to the command line arguments. */
public class SpaceShipFactory {
    /* Key for new Human ship */
    private static final String HUMAN_SPACESHIP = "h";

    /* Key for new Runner ship */
    private static final String RUNNER_SPACESHIP = "r";

    /* Key for new Basher ship */
    private static final String BASHER_SPACESHIP = "b";

    /* Key for new Aggressive ship */
    private static final String AGGRESSIVE_SPACESHIP = "a";

    /* Key for new Drunkard ship */
    private static final String DRUNKARD_SPACESHIP = "d";

    /* Key for new Special ship */
    private static final String SPECIAL_SPACESHIP = "s";

    public static SpaceShip[] createSpaceShips(String[] args) {
        SpaceShip[] spaceShips = new SpaceShip[args.length];
        for (int i = 0; i < args.length; i++){
            switch (args[i]){
                case HUMAN_SPACESHIP:
                    spaceShips[i] = new Human();
                    break;
                case RUNNER_SPACESHIP:
                    spaceShips[i] = new Runner();
                    break;
                case BASHER_SPACESHIP:
                    spaceShips[i] = new Basher();
                    break;
                case AGGRESSIVE_SPACESHIP:
                    spaceShips[i] = new Aggressive();
                    break;
                case DRUNKARD_SPACESHIP:
                    spaceShips[i] = new Drunkard();
                    break;
                case SPECIAL_SPACESHIP:
                    spaceShips[i] = new Special();
                    break;
            }
        }
        return spaceShips;
    }
}
