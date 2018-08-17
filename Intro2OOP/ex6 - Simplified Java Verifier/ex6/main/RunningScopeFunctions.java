//package oop.ex6.main;
//
//import oop.ex6.scope.FunctionParameter;
//import oop.ex6.scope.SavedParameter;
//import oop.ex6.scope.Scope;
//
//import java.util.List;
//
///**
// * The methods of the scope's running class.
// */
//public class RunningScopeFunctions {
//    private static Scope _scope;
//
//    public static void updateScope(Scope scope){
//        _scope = scope;
//    }
//
//    public static boolean saveOrUpdate(List<SavedParameter> parametersToSave,
//                                       boolean toUpdate) throws Exception {
//        if (parametersToSave != null) {
//            for(SavedParameter param: parametersToSave)
//                if (toUpdate)
//                    RunningScopeFunctions.updateVariableValue(param);
//                else
//                    RunningScopeFunctions.addNewVariable(param);
//            return true;
//        }
//        else
//            return false;
//    }
//
//    private static void addNewVariable(SavedParameter parameterToSave) throws Exception {
//        _scope.addVariable(parameterToSave);
//    }
//
//    private static void updateVariableValue(SavedParameter parameter) throws Exception {
//        if (_scope.isVariableExists(parameter.getname()))
//            _scope.updateVariable(parameter);
//        else
//            throw new Exception();
//    }
//
//    /*
//    Check that a given variable is defined, and if yes returns the value, if not returns null.
//     */
//    public static String getValue(String variableName){
//        return _scope.getVariableValue(variableName);
//    }
//
//    public static String getVariableType(String variable){
//        return _scope.getVariableType(variable);
//    }
//
//     ------------------------- Methods functions ---------------------------
//    public static void addNewMethod(FunctionParameter newFunction) throws Exception {
//        if (_scope.isAMethodScope())
//            throw new Exception();
//        newFunction.setFunctionScope(new Scope(_scope));
//        Scope.addFunction(newFunction);
//    }
//
//    public static FunctionParameter isMethodExists(FunctionParameter function){
//        return Scope.isMethodExists(function);
//    }
//
//     -------------------------- General Scope Function-----------------------
//    public static Scope getScope() {
//        return _scope;
//    }
//
//    public static boolean isScopeEnded(){
//        return _scope.isScopeEnded();
//    }
//
//    public static void increaseNumberOfClosedBrackets(){
//        _scope.increaseNumberOfClosedBrackets();
//    }
//}
//