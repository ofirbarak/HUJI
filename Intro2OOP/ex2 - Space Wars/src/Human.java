import oop.ex2.*;

/*
This is a class that represents spaceship that controlled by human.
It controlled by the user. The keys are: left-arrow and right-arrow to
turn, up-arrow to accelerate, ’d’ to fire a shot, ’s’ to turn on the shield, ’a’ to teleport.
You can assume there will be at most one human controlled ship in a game, but you’re not
required to enforce this.
 */
public class Human extends SpaceShip {
    /* Methods */
    /* Constructor */
    public Human(){
        super();
        _isEnemy = false;
    }

    /**
     * Gets the values from users and perform them.
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game){
        GameGUI gameGUI = game.getGUI(); // Create a pointer to game GUI object.
        _isAccelerate = gameGUI.isUpPressed();
        _isLeftTurn = gameGUI.isLeftPressed();
        _isRightTurn = gameGUI.isRightPressed();
        if (_isLeftTurn && _isRightTurn){
            _isLeftTurn = false;
            _isRightTurn = false;
        }
        _isTeleport = gameGUI.isTeleportPressed();
        _isShieldUp = gameGUI.isShieldsPressed();
        _isShoot = gameGUI.isShotPressed();
        super.doAction(game);
    }


}
