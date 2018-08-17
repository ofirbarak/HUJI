
/*
This is a class represents a runner spaceship.
This spaceship attempts to run away from the fight. It will always accelerate, and
wil constantly turn away from the closest ship. If the nearest ship is closer than 0.25 units,
and if its angle to the Runner is less than 0.23 radians, the Runner feels threatened and will
attempt to teleport.
 */
public class Runner extends SpaceShip{
    /* The maximal distance that ship is not teleporting */
    private static double MAX_DISTANCE_FROM_ANOTHER_SHIP = 0.25;

    /* The maximal angle to try to teleporting */
    private static double MAX_ANGLE_FOR_TELEPORT = 0.23;

    /* Methods */
    /* Constructor */
    public Runner(){
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
        if (_spaceShipPhysics.distanceFrom(closetShip.getPhysics()) < MAX_DISTANCE_FROM_ANOTHER_SHIP &&
                Math.abs(angleFromClosetShip) < MAX_ANGLE_FOR_TELEPORT){
            _isTeleport = true;
        }
        else {
            if (angleFromClosetShip > 0)
                _isRightTurn = true;
            else if (angleFromClosetShip < 0)
                _isLeftTurn = true;
        }
        super.doAction(game);
    }
}
