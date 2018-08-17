

*****
Comments:
The obvious guideline is to organize the block in an ascending order
that it could sum up easy with less moves. We choose to use the snake,
which means the weights of the weight matrix are ascending along the
snakes' shape, starting bottom left as the lowest and the top left as
the highest. This matrix multiplied by the board contribute the most
score.
Moreover if we detect a violation in the first row the weight matrix 
is changed to be like conos pointed to the top left tile. The think
behind that is that if there is a violation in the first row (this is
the row that all the maximum tiles are should be) it is important that
we will fix it, but we don't want to harm the general shape. A conos
like matrix will do the work because it keeps the rule that every row
is less the one below it, and the columns are organized like that the
first oen is the highest, which means we still want to get the top left
corner.
