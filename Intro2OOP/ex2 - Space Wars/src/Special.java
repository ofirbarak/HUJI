/*
This class represents a special ship. (smart one)
 */
public class Special extends SpaceShip {
    /* The maximal distance that ship is not teleporting */
    private static double MAX_DISTANCE_FROM_ANOTHER_SHIP = 0.09;

    /* The maximal angle to try to shot */
    private static double MAX_ANGLE_FOR_SHOT = 0.21;

    /* Methods */
    /* Constructor */
    public Special(){
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
        if (_spaceShipPhysics.distanceFrom(closetShip.getPhysics()) <= MAX_DISTANCE_FROM_ANOTHER_SHIP)
            _isShieldUp = true;
        double angleFromClosetShip = _spaceShipPhysics.angleTo(closetShip.getPhysics());
        if (Math.abs(angleFromClosetShip) < MAX_ANGLE_FOR_SHOT)
            _isShoot = true;
        if (angleFromClosetShip > 0)
            _isLeftTurn = true;
        else if (angleFromClosetShip < 0)
            _isRightTurn = true;
        super.doAction(game);
    }
}
