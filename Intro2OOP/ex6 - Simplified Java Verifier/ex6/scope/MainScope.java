package oop.ex6.scope;

import java.util.HashMap;
import java.util.Map;

/**
 * Represents the main scope.
 */
public class MainScope extends Scope {
    private static Map<String, FunctionScope> _methods;

    private static MainScope ourInstance = new MainScope();

    /**
     * Gets the main scope
     * @return main scope
     */
    public static MainScope getInstance() {
        return ourInstance;
    }

    private MainScope() {
        super();
        _methods = new HashMap<>();
    }

    /**
     * Generate a new main scope.
     */
    public static void reset(){
        ourInstance = new MainScope();
    }

    /**
     * Add global variable
     * @param savedParameter the parameter to add.
     * @throws Exception
     */
    @Override
    public void addVariable(SavedParameter savedParameter) throws Exception {
        if (_variables.containsKey(savedParameter.getName()) ||
                _methods.containsKey(savedParameter.getName()))
            throw new Exception();
        _variables.put(savedParameter.getName(), savedParameter);
    }

    /**
     * Add new functionParameter to methods.
     * @param functionParameter the parameter to add.
     */
    public void addFunction(FunctionScope functionParameter) throws Exception {
        if (_methods.containsKey(functionParameter.getFunctionName()))
            throw new Exception();
        functionParameter.updateMethodValues();
        _methods.put(functionParameter.getFunctionName(), functionParameter);
    }

    /**
     * Check if method exists
     * @param function method to check
     * @return true if yes, false otherwise
     */
    public boolean isMethodExists(FunctionScope function) {
        try {
            FunctionScope maybeThis = _methods.get(function.getFunctionName());
            return maybeThis.areParamsFitting(function);
        } catch (Exception e){
            return false;
        }
    }

    /**
     * Check is the main scope
     * @param scope scope to check
     * @return true if yes, false otherwise
     */
    public static boolean isMainScope(Scope scope){
        return ourInstance == scope;
    }

    public Scope getFunctionScope(String funcName) {
        return _methods.get(funcName);
    }
}
