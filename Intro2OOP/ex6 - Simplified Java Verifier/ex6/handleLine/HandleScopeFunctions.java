//package oop.ex6.handleLine;
//
//import oop.ex6.scope.FunctionScope;
//import oop.ex6.scope.MainScope;
//import oop.ex6.scope.SavedParameter;
//import oop.ex6.scope.Scope;
//
//import java.util.List;
//
///**
// * Handle scope functions.
// */
//public class HandleScopeFunctions {
//    private static Scope _scope;
//
//    public static void updateScope(Scope newScope){
//        _scope = newScope;
//    }
//
//    public static Scope getScope(){
//        return _scope;
//    }
//
//    static boolean saveOrUpdateRunningScope(List<SavedParameter> parametersToSave,
//                                       boolean toUpdate) throws Exception {
//        if (parametersToSave != null) {
//            for(SavedParameter param: parametersToSave)
//                if (toUpdate)
//                    updateVariableValue(param);
//                else
//                    addNewVariable(param);
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
//        if (_scope.isVariableExists(parameter.getname()) &&  // todo: make this more readable
//                !_scope.getVariable(parameter.getname()).getType().equals(HandleSJavaType.FINAL))
//            _scope.updateVariable(parameter);
//        else
//            throw new Exception();
//    }
//
//    /*
//    Check that a given variable is defined, and if yes returns the value, if not returns null.
//     */
//    public static String getValue(String variableName){
//        try {
//            return _scope.getVariable(variableName).getValue();
//        }catch (NullPointerException e){
//            return null;
//        }
//    }
//
//    public static String getVariableType(String variable){
//        return _scope.getVariable(variable).getType();
//    }
//
//    // --------------------------- Methods -------------------------------------------------
//
//    static void addNewMethod(FunctionScope newFunction) throws Exception {
//        if (_scope instanceof MainScope) {
//            newFunction.setParentScope(_scope);
//            ((MainScope) _scope).addFunction(newFunction);
//        }
//        else
//            throw new Exception();
//    }
//
//    static boolean isMethodExists(FunctionScope function){
//        if (_scope instanceof MainScope) {
//            ((MainScope) _scope).isMethodExists(function);
//            return true;
//        }
//        return false;
//    }
//
//}
