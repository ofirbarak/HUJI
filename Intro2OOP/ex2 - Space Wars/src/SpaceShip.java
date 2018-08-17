import java.awt.Image;
import oop.ex2.*;

/**
 * This class represent a minimal behaviors every ship have.
 */
public abstract class SpaceShip{
    /* Begin maximal energy level */
    private static final int maxBeginEnergyLevel = 210;

    /* Energy cost for teleporting */
    private static final int energyForTeleporting = 140;

    /* Reduce energy while the shield is down */
    private static final int reduceEnergyWhileShieldIsDown = 10;

    /* Energy cost for shot */
    private static final int energyForShot = 19;

    /* Increase in energy in case of collide ot shot while the shield is up */
    private static final int increaseEnergyWhileShieldUp = 18;

    /* Energy cost for shield */
    private static final int energyForShield = 3;

    /* Energy increase per round */
    private static final int increaseEnergyPerRound = 1;

    /* Begin energy level */
    private static final int beginEnergyLevel = 190;

    /* Begin health level */
    private static final int beginHealthLevel = 22;

    /* Number of round between fires. */
    private static final int numberOfRoundBetweenShots = 7;

    /* Reduced Health while being shot. */
    private static final int reduceHealthWhileBeingShot = 1;

    /* A SpaceShipPhysics object (from the helper package), that represents the position, direction
        and velocity of the ship. */
    protected SpaceShipPhysics _spaceShipPhysics;

    /* Is spaceship wants to turn left. */
    protected boolean _isLeftTurn;

    /* Is spaceship wants to turn right. */
    protected boolean _isRightTurn;

    /* Is spaceship wants to make shield up */
    protected boolean _isShieldUp;

    /* Is spaceship wants to teleport */
    protected boolean _isTeleport;

    /* Is spaceship wants to shoot */
    protected boolean _isShoot;

    /* Is spaceship is enemy */
    protected boolean _isEnemy;

    /* Is spaceship accelerating */
    protected boolean _isAccelerate;

    /* A current energy level, which is between 0 and the maximal energy level. */
    private int currentEnergyLevel; // --------------------------

    /* A maximal energy level. */
    private int maxEnergyLevel;

    /* A Health level between 0 and 22. */
    private int healthLevel;

    /* Counting number of rounds to fire again. */
    private int numberOfRoundsUntilNextFire;

    /* Constructor */
    protected SpaceShip(){
        reset(); // Call this method that init the ship
    }

    /* Methods */
    /**
     * Does the actions of this ship for this round. 
     * This is called once per round by the SpaceWars game driver.
     * @param game the game object to which this ship belongs.
     */
    public void doAction(SpaceWars game) {
        /* Check if number of rounds until next fire needs to decrease */
        if (numberOfRoundsUntilNextFire > 0)
            numberOfRoundsUntilNextFire--;
        /* Check if key pressed and preform the action */
        /* 1. Check if teleport key was pressed. */
        if (_isTeleport)
            teleport();
        /* 2. Check accelerator or turning key. If no one was pressed so consider it like accelerate
            key was pressed */
        turnAndAccelerate();
        /* 3. Check if turn on shield key pressed */
        if (_isShieldUp)
            shieldOn();
        /* 4. Check if fire key was pressed */
        if (_isShoot)
            fire(game);
        /* Increase energy level by 1 if current energy level is less than the maximum */
        if (currentEnergyLevel < maxEnergyLevel)
            currentEnergyLevel += increaseEnergyPerRound;
    }

    /**
     * Does the acceleration and turning.
     */
    private void turnAndAccelerate(){
        int turn = 0;
        if (_isLeftTurn)
            turn = 1;
        else if (_isRightTurn)
            turn = -1;
        _spaceShipPhysics.move(_isAccelerate, turn);
    }

    /**
     * This method is called every time a collision with this ship occurs 
     */
    public void collidedWithAnotherShip(){
        if (!bushing())
            gotHit();
    }

    /**
     * Check if 'Bashing'
     * 'Bashing' is when the ship has its shields up and collides with another ship. When a ship
     'bashes' another, its maximal energy level goes up by 18, and so does the current energy
     level (for example if the ship’s energy is 4 out of 190, colliding with another ship while the
     shields are up brings the energy to 22 out of 208).
     * @return true if "Bashing" occurred, false otherwise.
     */
    private boolean bushing(){
        if (!_isShieldUp)
            return false;
        maxEnergyLevel += increaseEnergyWhileShieldUp;
        currentEnergyLevel += increaseEnergyWhileShieldUp;
        return true;
    }

    /** 
     * This method is called whenever a ship has died. It resets the ship's 
     * attributes, and starts it at a new random position.
     */
    public void reset(){
        _spaceShipPhysics = new SpaceShipPhysics();
        maxEnergyLevel = maxBeginEnergyLevel;
        currentEnergyLevel = beginEnergyLevel;
        healthLevel = beginHealthLevel;
        numberOfRoundsUntilNextFire = 0;
        _isShieldUp = false;
        _isShoot = false;
        _isRightTurn = false;
        _isLeftTurn = false;
        _isTeleport = false;
    }

    /**
     * Checks if this ship is dead.
     * @return true if the ship is dead. false otherwise.
     */
    public boolean isDead() {
        return healthLevel == 0;
    }

    /**
     * Gets the physics object that controls this ship.
     * @return the physics object that controls the ship.
     */
    public SpaceShipPhysics getPhysics() {
        return _spaceShipPhysics;
    }

    /**
     * This method is called by the SpaceWars game object when ever this ship
     * gets hit by a shot.
     */
    public void gotHit() {
        if (!_isShieldUp)
            healthLevel -= reduceHealthWhileBeingShot;
        maxEnergyLevel -= reduceEnergyWhileShieldIsDown;
        if (maxEnergyLevel < 0)
            maxEnergyLevel = 0;
        if (currentEnergyLevel > maxEnergyLevel) {
            currentEnergyLevel = maxEnergyLevel;
        }
    }

    /**
     * Gets the image of this ship. This method should return the image of the
     * ship with or without the shield. This will be displayed on the GUI at
     * the end of the round.
     * 
     * @return the image of this ship.
     */
    public Image getImage(){
        if (_isShieldUp) {
            _isShieldUp = false;
            if (!_isEnemy)
                return GameGUI.SPACESHIP_IMAGE_SHIELD;
            else
                return GameGUI.ENEMY_SPACESHIP_IMAGE_SHIELD;
        }
        else {
            if (!_isEnemy)
                return GameGUI.SPACESHIP_IMAGE;
            else
                return GameGUI.ENEMY_SPACESHIP_IMAGE;
        }
    }

    /**
     * Attempts to fire a shot.
     * 
     * @param game the game object.
     */
    public void fire(SpaceWars game) {
        /* Check if number of rounds from last fire is more than 7 rounds, and there is enough energy (19) */
        if (numberOfRoundsUntilNextFire == 0 && currentEnergyLevel >= energyForShot) {
            game.addShot(_spaceShipPhysics);
            /* Initialize number of round until next fire */
            numberOfRoundsUntilNextFire = numberOfRoundBetweenShots;
            currentEnergyLevel -= energyForShot; // Decrease energy level
        }
        _isShoot = false;
    }

    /**
     * Attempts to turn on the shield.
     */
    public void shieldOn() {
        if (currentEnergyLevel >= energyForShield){
            _isShieldUp = true;
            currentEnergyLevel -= energyForShield;
        }
    }

    /**
     * Attempts to teleport.
     */
    public void teleport() {
        if (currentEnergyLevel >= energyForTeleporting) { // Check if there is enough energy
            _spaceShipPhysics = new SpaceShipPhysics();
            currentEnergyLevel -= energyForTeleporting;
        }
        _isTeleport = false;
    }
    
}
