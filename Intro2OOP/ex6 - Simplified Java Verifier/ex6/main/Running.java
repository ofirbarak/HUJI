//package oop.ex6.main;
//
//import oop.ex6.general.GeneralHelpFunctions;
//import oop.ex6.handleLine.HandleSJavaType;
//import oop.ex6.handleLine.HandleSavedParam;
//import oop.ex6.handleLine.ScopeHandler;
//import oop.ex6.scope.FunctionParameter;
//import oop.ex6.scope.Scope;
//
//import java.io.*;
//
//
///**
// * Connecting variables class to scope.
// */
//public class Running {
//    private static Scope _currentScope;
//    private static FileInputStream _fileInputStream;
//    private static LineNumberReader _reader;
//
//    public static void run(FileInputStream fileInputStream, String arg) throws Exception {
//        _fileInputStream = fileInputStream;
//        LineNumberReader reader = new LineNumberReader(new InputStreamReader(new FileInputStream(arg)));
//        _reader = reader;
//        Scope mainScope = new Scope(); // Main scope
//        updateScope(mainScope);
//        reader = actionsWhenNewScopeGenerated(reader);
//        String line;
//        while ( (line = reader.readLine()) != null) { // Parse all file
//            reader = runALine(line, reader);
//            if (_currentScope != mainScope && _currentScope.isScopeEnded())
//                updateScope(_currentScope.getParentScope());
//        }
//    }
//
//    private static LineNumberReader runALine(String line, LineNumberReader reader) throws Exception {
//        if (line == null)
//            return reader;
//        boolean isAKnownSJavaWord, isVariableAssign;
//        FunctionParameter function;
//        isAKnownSJavaWord = isAKnownSJavaWord(line);
//        if (!isAKnownSJavaWord) {
//            isVariableAssign = isSavedVariable(line);
//            if (!isVariableAssign){
//                function = HandleSavedParam.checkAMethodCall(line);
//                if (function == null)
//                    throw new Exception();
//            }
//        }
//        return reader;
//    }
//
//    /*
//    Check if line starts with known s-java word (Including Empty line - just spaces ), if yes do the checks.
//    Otherwise returns false.
//     */
//    private static boolean isAKnownSJavaWord(String line) throws Exception {
//        if (GeneralHelpFunctions.isOnlySpacesInTheString(line))
//            return true;
//        if (HandleSJavaType.isLineIsCloseBracket(line)) {
//            if (_currentScope != null)
//                _currentScope.increaseNumberOfClosedBrackets();
//            return true;
//        }
//        String[] split = GeneralHelpFunctions.getsFirstWordAndTheRestOfTheString(line);
//        if (split[0] == null)
//            return false;
//        if (isPassed(split[0])) // If it is a variable, we already checked it.
//            return true;
//        Scope scopeToUpdate = HandleSJavaType.getScope(split[0], split[1]);
//        if (scopeToUpdate != null){
//            updateScope(scopeToUpdate);
//            return true;
//        }
//        boolean isAKnownWord = HandleSJavaType.checkExpression(split[0], split[1]);
//        if (isAKnownWord){ // Check if new scope was generated
//            Scope scope = ScopeHandler.getScope();
//            if (_currentScope != scope)
//                actionsWhenNewScopeGenerated(_reader);
//        }
//        return isAKnownWord;
//    }
//
//    /*
//    Check if it is call to method or assign a value to an exists variable.
//     */
//    private static boolean isSavedVariable(String line) throws Exception {
//        return HandleSavedParam.checkAssigningValueToVariable(line);
//    }
//
//    private static void updateScope(Scope newScope){
//        _currentScope = newScope;
//        ScopeHandler.updateScope(newScope);
//    }
//
//     ---------------------------- First actions for parsing new section ----------------------------------
//    private static LineNumberReader actionsWhenNewScopeGenerated(LineNumberReader reader) throws Exception {
//        _currentScope = ScopeHandler.getScope();
//        ScopeHandler.updateScope(_currentScope);
//        int rememberLineNumber = reader.getLineNumber();
//        passAllScopeFirstly(reader);
//        _currentScope.resetNumberBrackets();
//        return skipLines(rememberLineNumber); // Returns the starting scope point
//    }
//
//     Pass all the scope and adds to the main scope methods declaration and variables appeared
//     in the main scope.
//    private static void passAllScopeFirstly(LineNumberReader reader) throws Exception {
//        String line;
//        while ((line = reader.readLine()) != null) {
//            SKIPisAKnownSJavaWord(line, reader);
//        }
//    }
//
//
//    private static LineNumberReader skipLines(int numberOfLinesToSkip) throws IOException {
//        LineNumberReader reader = new LineNumberReader(new InputStreamReader(_fileInputStream));
//        for (int i=0; i < numberOfLinesToSkip; i++)
//            reader.readLine();
//        return reader;
//    }
//
//
//    private static boolean SKIPisAKnownSJavaWord(String line, LineNumberReader  reader) throws Exception {
//        if (GeneralHelpFunctions.isOnlySpacesInTheString(line))
//            return true;
//        if (HandleSJavaType.isLineIsCloseBracket(line)) {
//            if (_currentScope != null)
//                _currentScope.increaseNumberOfClosedBrackets();
//            return true;
//        }
//        String[] split = GeneralHelpFunctions.getsFirstWordAndTheRestOfTheString(line);
//        if (split[0] == null)
//            return false;
//        boolean isAKnownWord = HandleSJavaType.checkExpression(split[0], split[1]);
//        if (isAKnownWord){ // Check if new scope was generated
//            if (split[0].equals("void"))
//               skipSectionContent(ScopeHandler.getScope(), reader);
//        }
//        return isAKnownWord;
//    }
//
//    private static void skipSectionContent(Scope scope, LineNumberReader reader) throws Exception {
//        String line;
//        while (!scope.isScopeEnded() && (line = reader.readLine()) != null){
//            if (line.matches(".*[{]\\s*"))
//                scope.increaseNumberOfOpenBrackets();
//            if (line.matches("\\s*}\\s*"))
//                scope.increaseNumberOfClosedBrackets();
//        }
//        scope.resetNumberBrackets();
//    }
//
//
//}
