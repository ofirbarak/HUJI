/*
This class represents a aggressive ship.
This ship pursues other ships and tries to fire at them. It will always accelerate,
and turn towards the nearest ship. When its angle to the nearest ship is less than 0.21
radians, it will try to fire.
 */
public class Aggressive extends SpaceShip{
    /* Maximum angle to nearest ship */
    private static double MAX_ANGLE_TO_NEAREST_SHIP = 0.21;

    /* Methods */
    /* Constructor */
    public Aggressive(){
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
        if (Math.abs(angleFromClosetShip) < MAX_ANGLE_TO_NEAREST_SHIP)
            _isShoot = true;
        if (angleFromClosetShip > 0)
            _isLeftTurn = true;
        else if (angleFromClosetShip < 0)
            _isRightTurn = true;
        super.doAction(game);
    }
}
