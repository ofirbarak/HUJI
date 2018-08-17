import java.util.Map;
import java.util.Random;

/*
This class represents a drunkard ship.
Its pilot had a tad too much to drink.
Accelerate - randomizes
Movement - get a random value between 2pi. If is more than current angel turn left,
else turn right.
Shield - activate shield when the distance from the nearest ship is less than 0.1
 */
public class Drunkard extends SpaceShip{
    /* The maximal distance that ship is not turning on it's shield */
    private static double MAX_DISTANCE_FROM_ANOTHER_SHIP = 0.1;

    /* Methods */
    /* Constructor */
    public Drunkard(){
        super();
        _isEnemy = true;
    }

    /**
     * Does the actions of this ship for this round. Uses the super doAction method.
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game){
        SpaceShip closetShip = game.getClosestShipTo(this);
        Random random = new Random();
        _isAccelerate = random.nextBoolean();
        _isLeftTurn = false;
        _isRightTurn = false;
        double angleFromClosetShip = _spaceShipPhysics.angleTo(closetShip.getPhysics());
        double randomAngelDegrees = random.nextDouble() * (2*Math.PI);
        if (_spaceShipPhysics.distanceFrom(closetShip.getPhysics()) < MAX_DISTANCE_FROM_ANOTHER_SHIP)
            _isShieldUp = true;
        if (angleFromClosetShip < randomAngelDegrees)
            _isLeftTurn = true;
        else if (angleFromClosetShip < 0)
            _isRightTurn = true;
        super.doAction(game);
    }
}
