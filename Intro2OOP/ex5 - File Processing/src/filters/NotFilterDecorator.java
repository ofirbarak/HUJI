package filters;

/**
 * Decorator class for filtering. if we wan't to implement another filter option we just
 * need to extend this class.
 */
class NotFilterDecorator{
    private boolean _isNotFiltering;

    NotFilterDecorator(boolean isNot){
        _isNotFiltering = isNot;
    }

    boolean getResult(boolean variable){
        if (_isNotFiltering)
            return !variable;
        else
            return variable;
    }
}
