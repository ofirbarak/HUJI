//package oop.ex6.scope;
//
//import java.util.Iterator;
//import java.util.List;
//
///**
// * Represents a saved function in the scope methods saved.
// */
//public class FunctionParameter {
//    //public String get_type() {
//        //return _type;
//    //}
//
////    public List<SavedParameter> get_parameters() {
////        return _parameters;
////    }
//
//    public String get_functionName() {
//        return _functionName;
//    }
//
//    //private String _type;
//    private List<SavedParameter> _parameters;
//    private Scope _functionScope;
//    private String _functionName;
//
//    public FunctionParameter(String funcName, List<SavedParameter> params) {
//        //_type = type;
//        _functionName = funcName;
//        _parameters = params;
//        _functionScope = new Scope();
//    }
//
//    public Scope getFunctionScope(){
//        return _functionScope;
//    }
//
//    public void setFunctionScope(Scope scope){
//        _functionScope = scope;
//    }
//
//    public boolean areParamsFitting(FunctionParameter function2){
//        List<SavedParameter> function2Params = function2._parameters;
//        if (_parameters.size() != function2Params.size())
//            return false;
//        Iterator<SavedParameter> it1 = _parameters.iterator();
//        Iterator<SavedParameter> it2 = function2Params.iterator();
//        while (it1.hasNext() && it2.hasNext())
//            if (!it1.next().equals(it2.next()))
//                return false;
//        return true;
//    }
//
//    public void updateMethodValues(FunctionParameter function) throws Exception {
//        for (int i = 0; i < _parameters.size(); i++) {
//            SavedParameter parameter = _parameters.get(i);
//            parameter.setValue(function._parameters.get(i).getValue());
//            _functionScope.addVariable(parameter);
//        }
//    }
//}
