/*
This class represents a "Basher" spaceship.
This ship attempts to collide with other ships. It will always accelerate, and will
constantly turn towards the closest ship. If it gets within a distance of 0.19 units (inclusive)
from another ship, it will attempt to turn on its shields.
 */
public class Basher extends SpaceShip{
    /* The maximal distance that ship is not turning on it's shield */
    private static double MAX_DISTANCE_FROM_ANOTHER_SHIP = 0.19;

    /* Methods */
    /* Constructor */
    public Basher(){
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
        _isAccelerate = true;
        _isLeftTurn = false;
        _isRightTurn = false;
        double angleFromClosetShip = _spaceShipPhysics.angleTo(closetShip.getPhysics());
        if (_spaceShipPhysics.distanceFrom(closetShip.getPhysics()) <= MAX_DISTANCE_FROM_ANOTHER_SHIP)
            _isShieldUp = true;
        if (angleFromClosetShip > 0)
            _isLeftTurn = true;
        else if (angleFromClosetShip < 0)
            _isRightTurn = true;
        super.doAction(game);
    }
}
