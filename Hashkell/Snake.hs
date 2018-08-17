module Snake where

import Data.List  
import Control.Monad
import Control.Applicative
import System.IO (hFlush, stdout)
import Control.Monad.State
import Graphics.Gloss.Interface.Pure.Game as Game
import System.Random as Random





main :: IO ()
main = do
    putStrLn "Press 1 for Easy Game, 2 for Medium Game, 3 for Hard Game"
    hFlush stdout
    input <- readLn
    seed <- Random.randomIO
    let world = start seed
        speed = level (input)
    
    Game.play
        Game.FullScreen
        Game.blue
        speed
        world
        drawWorld
        eventSolver
        singleClick


instance Functor World where
    fmap f w = w {snake = fmap (\(x,y) -> (f x, f y)) (snake w)}


instance Applicative World where
    pure a = World { resolution = (1920, 850) 
    , direction = North
    , snake_scale = 45
    , snake = [(a,a)]
    , isStuck = False
    , food = (0, 0)
    , superFood = (3000,3000)
    , poison = (4000,4000)
    }
    
    (<*>) (World { resolution = (1920, 850) 
    , direction = North
    , snake_scale = 45
    , snake = [(f,g)]
    , isStuck = False
    , food = (0, 0)
    , superFood = (3000,3000)
    , poison = (4000,4000)
    }) secondFunc = f <$> secondFunc

instance Monad World where
    return a = pure a
    (>>=) (World { resolution = (1920, 850) 
    , direction = North
    , snake_scale = 45
    , snake = [(f,g)]
    , isStuck = False
    , food = (0, 0)
    , superFood = (3000,3000)
    , poison = (4000,4000)
    }) func = func f

data World a = World
    { resolution :: (Int, Int)
    , direction :: Snake_direction
    , snake_scale :: Int
    , snake :: [(a, a)]
    , isStuck :: Bool
    , gen :: Random.StdGen
    , food :: (Int, Int)
    , superFood :: (Int, Int)
    , poison :: (Int, Int)
    } deriving (Read, Show) 

data Snake_direction
    = North
    | East
    | South
    | West
    deriving (Bounded, Enum, Eq, Ord, Read, Show)
	 
level :: Int -> Int
level a = a * 10



start :: Int -> World Int
start seed = changeFoodLocation World
    { resolution = (1920, 850) 
    , direction = North
    , snake_scale = 45
    , snake = [(0, 2), (0, 1), (0, 0), (0, -1), (0, -2)]
    , isStuck = False
    , gen = Random.mkStdGen seed
    , food = (0, 0)
    , superFood = (3000,3000)
    , poison = (4000,4000)
    }

drawWorld :: World Int -> Game.Picture
drawWorld world = Game.pictures
    [ drawBounds world
    , drawFood world
    , drawSnake world
    , drawScore world
    , drawSuperFood world
    , drawPoison world
    , drawLegend world
    , drawGameOver world
    ]

eventSolver :: Game.Event -> World Int-> World Int
eventSolver event world = case event of
    Game.EventResize newResolution -> handleResize newResolution world
    Game.EventKey key state _ _ -> if isStuck world
        then handleKey key state world
        else handleKey key state world
    _ -> world

singleClick ::  Float -> World Int -> World Int
singleClick _time world =
    if isStuck world
    then world
    else
        let oldSnake = snake world
            newSnake@((x, y) : _) = init oldSnake
            (x', y') = case direction world of
                North -> (x, y + 1)
                East -> (x + 1, y)
                South -> (x, y - 1)
                West -> (x - 1, y)
        in  if inBounds world (x', y') && not (isSnake world (x', y'))
            then if isFood world (x', y')
                then
		    if mod (length(snake world)) (10) == 0
			then
                    	    let world''' = changeSuperFoodLocation world''
                                world'' = deleteFood world'
                                world' = changePoisonLocation world
                            in  world''' { snake = (x', y') : oldSnake }
		    else
                        let world' = changeFoodLocation world
                        in world' { snake= (x', y') :oldSnake}
		     
	        else if isFood world (x', y') 
		  then
		      let world' = changeFoodLocation world
		      in world' { snake = (x', y'): oldSnake}
                else if isSuperFood world(x', y')
	       	  then
	              let world''' = changeFoodLocation world''
			  world'' = deleteSuperFood world'
                          world' = deletePoisoned world
		      in world''' { snake = (x', y') :(x',y') : oldSnake }
                else if isPoisoned world(x', y')
	       	  then
	              let world'''' = deletePoisoned world'''
                          world''' = fmap poisoning world''
                          world'' = deleteSuperFood world'
                          world' = changeFoodLocation world
		      in world'''' { snake = (x'+ 2, y'+ 2) :(x' + 2, y'+ 2) :(x'+ 2, y'+ 2) : snake world''''}
 		else world { snake = (x', y') : newSnake }
            else world { isStuck = True }


poisoning :: Int -> Int 
poisoning x = x + 2

drawBounds :: World Int -> Game.Picture
drawBounds world =
    let x = size world
    in  Game.rectangleWire x x

 

drawFood :: World Int-> Game.Picture
drawFood world = Game.color Game.green (drawCirc (food world) world)

drawSuperFood :: World Int-> Game.Picture
drawSuperFood world = Game.color Game.yellow (drawCirc (superFood world) world)

drawLegend :: World Int -> Game.Picture
drawLegend world = Game.pictures[Game.color Game.black(Game.translate (-550) (500) (Game.scale 0.15 0.15 (Game.text ("Help: " ++ "\n" ++ " Green Apple - 1 Point" ++"\n" ++ " Yellow Apple - 2 points" ++  "\n" ++ " Red Apple - 3 Points but will change position"))))]

drawPoison :: World Int-> Game.Picture
drawPoison world = Game.color Game.red (drawCirc (poison world) world)

drawScore ::World Int-> Game.Picture
drawScore world = Game.pictures [Game.color Game.black (Game.translate (-450) (470) (Game.scale 0.2 0.2 (Game.text ("score: " ++ show (length (snake world))))))]

deleteSuperFood :: World Int-> World Int
deleteSuperFood  world = world {superFood = (3000,3000)}

deleteFood :: World Int -> World Int
deleteFood world = world {food = (3000,3000)}

deletePoisoned :: World Int -> World Int
deletePoisoned world = world {poison = (4000,4000)}

drawSnake :: World Int -> Game.Picture
drawSnake world = case snake world of
    (p : ps) -> Game.pictures
        ( Game.color Game.black (drawBox p world)
        : map (\ x -> drawBox x world) ps
        )
    _ -> Game.blank

drawCirc :: (Int, Int) -> World Int -> Game.Picture
drawCirc (x, y) world =
    let s = size world / fromIntegral (snake_scale world)
        x' = s * fromIntegral x
        y' = s * fromIntegral y
    in  Game.translate x' y' (Game.circleSolid (s/2))

drawBox :: (Int, Int) -> World Int -> Game.Picture
drawBox (x, y) world =
    let s = size world / fromIntegral (snake_scale world)
        x' = s * fromIntegral x
        y' = s * fromIntegral y
    in  Game.translate x' y' (Game.rectangleSolid s s)

drawGameOver :: World Int -> Game.Picture
drawGameOver world = if isStuck world
    then Game.pictures
        [ Game.color Game.black (Game.scale 0.15 0.15 (Game.text "Game Over - Press Home To Restart"))
        , Game.color Game.black (Game.translate (0) (-50) (Game.scale 0.2 0.2 (Game.text ("score: " ++ show (length (snake world))))))
        ]
    else Game.blank

--

handleResize :: (Int, Int) -> World Int  -> World Int
handleResize newResolution world = world { resolution = newResolution }

handleKey :: Game.Key -> Game.KeyState -> World Int -> World Int
handleKey key state world = case state of
    Game.Down -> case key of
	Game.SpecialKey Game.KeyHome ->
	    world {
   		   direction = North
   		 , snake = [(0, 2), (0, 1), (0, 0), (0, -1), (0, -2)]
   		 , isStuck = False
    		 , food = (0, 0)
  	         , superFood = (3000,3000)
	         , poison = (4000, 4000)
		 }
        Game.SpecialKey Game.KeyUp ->
            world { direction = if direction world == South then South else North }
        Game.SpecialKey Game.KeyDown ->
            world { direction = if direction world == North then North else South }
        Game.SpecialKey Game.KeyRight ->
            world { direction = if direction world == West then West else East }
        Game.SpecialKey Game.KeyLeft ->
            world { direction = if direction world == East then East else West }
        _ -> world
    _ -> world

--


size :: (Num a) => World Int-> a
size world =
    let (width, height) = resolution world
    in  fromIntegral (min width height)

inBounds :: World Int-> (Int, Int) -> Bool
inBounds world (x, y) =
    let s = snake_scale world `div` 2
    in  -s <= x && x <= s && -s <= y && y <= s

isSnake :: World Int-> (Int, Int) -> Bool
isSnake world (x, y) = any (== (x, y)) (snake world)

isFood :: World Int-> (Int, Int) -> Bool
isFood world (x, y) = (x, y) == food world

isSuperFood :: World Int-> (Int, Int) -> Bool
isSuperFood world (x, y) = (x, y) == superFood world

isPoisoned :: World Int-> (Int, Int) -> Bool
isPoisoned world (x, y) = (x, y) == poison world

changeFoodLocation :: World Int-> World Int
changeFoodLocation world =
    let g0 = gen world
        a = snake_scale world `div` 2
        (x, g1) = Random.randomR (-a, a) g0
        (y, g2) = Random.randomR (-a, a) g1
    in  if isSnake world (x, y)
        then changeFoodLocation world { gen = g2 }
        else world { gen = g2 , food = (x, y) }

changeSuperFoodLocation :: World Int-> World Int
changeSuperFoodLocation world =
    let g0 = gen world
        a = snake_scale world `div` 2
        (x, g1) = Random.randomR (-a, a) g0
        (y, g2) = Random.randomR (-a, a) g1
    in  if isSnake world (x, y)
        then changeSuperFoodLocation world { gen = g2 }
        else world { gen = g2 , superFood = (x, y) }

changePoisonLocation :: World Int-> World Int
changePoisonLocation world =
    let g0 = gen world
        a = snake_scale world `div` 2
        (x, g1) = Random.randomR (-a, a) g0
        (y, g2) = Random.randomR (-a, a) g1
    in  if isSnake world (x, y)
        then changePoisonLocation world { gen = g2 }
        else world { gen = g2 , poison = (x, y) }


