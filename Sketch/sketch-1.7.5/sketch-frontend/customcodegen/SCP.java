package customcodegen;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.TreeSet;
import java.util.Vector;
import java.util.List;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.io.OutputStream;
import java.io.PrintWriter;

import sketch.compiler.ast.core.FEReplacer;
import sketch.compiler.passes.printers.CodePrinter;
import sketch.compiler.ast.core.Annotation;
import sketch.compiler.ast.core.FieldDecl;
import sketch.compiler.ast.core.Function;
import sketch.compiler.ast.core.Function.LibraryFcnType;
import sketch.compiler.ast.core.Function.PrintFcnType;
import sketch.compiler.ast.core.Package;
import sketch.compiler.ast.core.stmts.*;
import sketch.compiler.ast.core.typs.StructDef;
import sketch.compiler.ast.core.typs.StructDef.StructFieldEnt;
import sketch.compiler.ast.cuda.stmts.CudaSyncthreads;
import sketch.compiler.ast.promela.stmts.StmtFork;
import sketch.compiler.ast.spmd.stmts.SpmdBarrier;
import sketch.compiler.ast.spmd.stmts.StmtSpmdfork;
import sketch.util.annot.CodeGenerator;
import sketch.compiler.ast.core.exprs.*;
import sketch.compiler.ast.core.Parameter;


@CodeGenerator
public class SCP extends FEReplacer
{
	boolean outtags = false;
	private static final int	tabWidth	= 2;
	protected final PrintWriter	out;
	protected int	indent	= 0;
	protected String	pad	= "";


	// Variables by priyan
	protected String currentOut;
	protected String emptyListCheck;
	protected HashMap<String, String> variableMap;
	protected HashSet<String> outSet;
	protected String inputParamName;

	// Constants by Priyan
	protected static final String IS_EMPTY_LIST_FUNC = "isEmptyList";
	protected static final String HEAD_LIST_FUNC = "head@list";
	protected static final String TAIL_LIST_FUNC = "tail";
	protected static final String EMPTY_LIST_FUNC = "empty_list";
	protected static final String ADD_LIST_FUNC = "add@list";
	protected static final String Max_FUNC = "max";
	protected static final boolean PRINT_ACTUAL_CODE = false;
	protected static final List<String> SUPPORTED_FUNCTIONS = Arrays.asList("list_method", "int_method", "list_to_list");

	protected final boolean printLibraryFunctions;
	public SCP outputTags(){

		outtags = true;
		return this;
	}

	public SCP() {
		out = new PrintWriter(System.out);
		printLibraryFunctions = false;
		variableMap = new HashMap<String, String>();
		outSet = new HashSet<String>();
	}

	protected void printTab () {
		if(indent*tabWidth!=pad.length()) {
			StringBuffer b=new StringBuffer();
			for(int i=0;i<indent*tabWidth;i++)
				b.append(' ');
			pad=b.toString();
		}
		out.print(pad);
	}

	protected void print (String s) {
		out.print (s);
	}

	protected void printLine (String s) {
		printTab();
		out.println(s);
		out.flush();
	}

	protected void printIndentedStatement (Statement s) {
		if(s==null) return;
		if(s instanceof StmtBlock)
			s.accept(this);
		else {
			indent++;
			s.accept(this);
			indent--;
		}
	}


	public Object visitFunction(Function func)
	{
		if(!SUPPORTED_FUNCTIONS.contains(func.getName())){
			return func;
		}

		// priyan
		List<Parameter> params = func.getParams();
		if(params.size() > 0 && params.get(params.size() - 1).isParameterOutput()){
			currentOut = params.get(params.size() - 1).getName();
		}

		inputParamName = params.get(0).getName();

		if(outtags && func.getTag() != null){ out.println("T="+func.getTag()); }
		printTab();
//		out.println("/*" + func.getCx() + "*/");
		printTab();
		//From the custom code generator you have access to any annotations attached to the function.
		//You can use these annotations to pass information to your code generator.
		for (Entry<String, Vector<Annotation>> anitv : func.annotationSet()) {
			for (Annotation anit : anitv.getValue()) {
				out.print(anit.toString() + " ");
			}
		}
		out.print("\n");
		// Priyan: prints the function header
		out.println("fun " + func.getName() + "(" + inputParamName + "):");
//		out.println((func.getInfo().printType == PrintFcnType.Printfcn ? "printfcn " : "") + func.toString());
		try {
			super.visitFunction(func);
		}
		catch (Exception e){
			printLine(e.getStackTrace()[0].toString());
		}
		out.println("end");
		out.flush();
		return func;
	}


	@Override
	public Object visitPackage(Package spec)
	{

		//The name resolver is used to find functions and structs matching a particular name.
		nres.setPackage(spec);
//		printLine("/* BEGIN PACKAGE " + spec.getName() + "*/");

		for (StructDef tsOrig : spec.getStructs()) {
			StructDef ts = (StructDef) tsOrig.accept(this);
		}

		for (Iterator iter = spec.getVars().iterator(); iter.hasNext(); )
		{
			FieldDecl oldVar = (FieldDecl)iter.next();
			FieldDecl newVar = (FieldDecl)oldVar.accept(this);

		}
		int nonNull = 0;

		TreeSet<Function> orderedFuncs = new TreeSet<Function>(new Comparator<Function>()
		{
			public int compare(Function o1, Function o2) {
				final int det_order =
						o1.getInfo().determinsitic.compareTo(o2.getInfo().determinsitic);
				return det_order + (det_order == 0 ? 1 : 0) *
						o1.getName().compareTo(o2.getName());
			}
		});
		orderedFuncs.addAll(spec.getFuncs());

		for (Function oldFunc : orderedFuncs) {
			if (oldFunc.getInfo().libraryType != LibraryFcnType.Library || printLibraryFunctions) {
				Function newFunc = (Function) oldFunc.accept(this);
			}
		}
//		printLine("/* END PACKAGE " + spec.getName() + "*/");
		return spec;
	}



	public Object visitStmtFor(StmtFor stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		printLine("for(" + stmt.getInit() + "; " + stmt.getCond() + "; " +
				stmt.getIncr() + ")" + (stmt.isCanonical() ? "/*Canonical*/" : ""));
		printIndentedStatement(stmt.getBody());
		return stmt;
	}

	public Object visitStmtSpmdfork(StmtSpmdfork stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		printLine("spmdfork("+stmt.getNProc() + ")");
		printIndentedStatement(stmt.getBody());
		return stmt;
	}

	public Object visitSpmdBarrier(SpmdBarrier stmt)
	{
		printLine("spmdbarrier();");
		return stmt;
	}

	@Override
	public Object visitStmtIfThen(StmtIfThen stmt)
	{
		if(PRINT_ACTUAL_CODE) {
			if (outtags && stmt.getTag() != null) {
				out.println("T=" + stmt.getTag());
			}
			printLine("if(" + stmt.getCond() + ")/*" + stmt.getCx() + "*/");
			printIndentedStatement(stmt.getCons());
			if (stmt.getAlt() != null) {
				printLine("else");
				printIndentedStatement(stmt.getAlt());
			}
		}
		else {
			if(stmt.getCond() instanceof ExprVar){
				// Most probably check for empty list
				// Todo: Check if the condition is for empty list
				printLine("cases (list) " + inputParamName + ":");
				indent++;
				printLine("| empty =>");
				printIndentedStatement(stmt.getCons());
				if(stmt.getAlt() != null){
					printLine("| link(head, tail) => ");
					printIndentedStatement(stmt.getAlt());
				}
				indent--;
				printLine("end");
				return stmt;

			}
			else if(stmt.getCond() instanceof ExprBinary){
				if(((ExprBinary)stmt.getCond()).getLeft() instanceof  ExprVar){
					// We have something better to print
					String condVar = ((ExprVar)((ExprBinary)stmt.getCond()).getLeft()).toString();
					String condStr = stmt.getCond().toString().replace(condVar, variableMap.get(condVar));
					printLine("if " + condStr + ":");
					printIndentedStatement(stmt.getCons());
					if (stmt.getAlt() != null) {
						printLine("else:");
						printIndentedStatement(stmt.getAlt());
					}
					printLine("end");
					return stmt;
				}
			}
			if (outtags && stmt.getTag() != null) {
				out.println("T=" + stmt.getTag());
			}
			printLine("if(" + stmt.getCond() + ")");
			printIndentedStatement(stmt.getCons());
			if (stmt.getAlt() != null) {
				printLine("else");
				printIndentedStatement(stmt.getAlt());
			}
		}
		return stmt;
	}

	@Override
	public Object visitStmtWhile(StmtWhile stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		printLine("while(" + stmt.getCond() + ")");
		printIndentedStatement(stmt.getBody());
		return stmt;
	}

	@Override
	public Object visitStmtDoWhile(StmtDoWhile stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		printLine("do");
		printIndentedStatement(stmt.getBody());
		printLine("while(" + stmt.getCond() + ")");
		return stmt;
	}

	@Override
	public Object visitStmtLoop(StmtLoop stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		printLine("loop(" + stmt.getIter() + ")");
		printIndentedStatement(stmt.getBody());
		return stmt;
	}
	@Override
	public Object visitStmtFork(StmtFork stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		printLine("fork(" +  stmt.getLoopVarDecl() + "; "  + stmt.getIter() + ")");
		printIndentedStatement(stmt.getBody());
		return stmt;
	}

	@Override
	public Object visitStmtBlock(StmtBlock stmt)
	{
		String tempOut = currentOut;

		// Statement block processing
		List<Statement> stmts = stmt.getStmts();
		if(stmts.size() > 0){
			// Find the out statement
			Statement last_stmt = stmts.get(stmts.size() - 1);
			if(last_stmt instanceof StmtAssign){
				ChangeCurrentOutputFromStmtAssign((StmtAssign)last_stmt);
			}
			else if(last_stmt instanceof StmtReturn && stmts.size() > 1){
				Statement sec_last_stmt = stmts.get(stmts.size() - 2);
				if(sec_last_stmt instanceof StmtAssign){
					ChangeCurrentOutputFromStmtAssign((StmtAssign)sec_last_stmt);
				}
			}
		}

		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		if(PRINT_ACTUAL_CODE) {
			printLine("{");
		}
		indent++;
		this.visitStmtBlockSuper(stmt);
//		super.visitStmtBlock(stmt);
		indent--;
		if(PRINT_ACTUAL_CODE) {
			printLine("}");
		}
		out.flush();
		currentOut = tempOut;
		return stmt;
	}

	public void ChangeCurrentOutputFromStmtAssign(StmtAssign stmtAssign){
		Expression lhs, rhs;
		lhs = stmtAssign.getLHS();
		rhs = stmtAssign.getRHS();

		// Only change if lhs matches current out
		if(lhs instanceof ExprVar && rhs instanceof ExprVar && ((ExprVar)lhs).getName().equals(currentOut)){
			currentOut = ((ExprVar)rhs).getName();
		}
	}

	public Object visitStmtBlockSuper(StmtBlock stmt)
	{
		List<Statement> oldStatements = newStatements;
		newStatements = new ArrayList<Statement>();
		boolean changed = false;
		int i=0;
		for (Iterator iter = stmt.getStmts().iterator(); iter.hasNext();++i )
		{
			Statement s = (Statement)iter.next();
			// completely ignore null statements, causing them to
			// be dropped in the output
			if (s == null)
				continue;
			try{
				doStatement(s);
				if (!(newStatements.size() == i + 1 && newStatements.get(i) == s)) {
					changed = true;
				}
				if (i < newStatements.size() &&
						newStatements.get(i) instanceof StmtReturn)
				{
					if (iter.hasNext()) {
						changed = true;
						break;
					}
				}
				/*
				 * Statement tmpres = (Statement)s.accept(this); if (tmpres != null)
				 * addStatement(tmpres);
				 */
			}catch(RuntimeException e){
				newStatements = oldStatements;
				throw e;
			}
		}
		if(!changed){
			newStatements = oldStatements;
			return stmt;
		}
		Statement result = new StmtBlock(stmt, newStatements);
		newStatements = oldStatements;
		return result;
	}

	@Override
	public Object visitStmtAssert(StmtAssert stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		printLine(stmt.toString() + ";" + " //" + stmt.getMsg());
		return super.visitStmtAssert(stmt);
	}

	@Override
	public Object visitStmtAssume(StmtAssume stmt) {
		if (outtags && stmt.getTag() != null) {
			out.println("T=" + stmt.getTag());
		}
		printLine(stmt.toString() + ";" + " //" + stmt.getMsg());
		return super.visitStmtAssume(stmt);
	}

	@Override
	public Object visitStmtAssign(StmtAssign stmt)
	{
		// Out variable assignment
		String lhs, rhs;

		lhs = stmt.getLHS().toString();
		if(stmt.getRHS() instanceof ExprBinary){
			ExprBinary rhsExpr = (ExprBinary)stmt.getRHS();
			String rightStr = rhsExpr.getRight().toString();
			String leftStr = rhsExpr.getLeft().toString();
			if(rhsExpr.getRight() instanceof ExprVar && variableMap.containsKey(rightStr)){
				rightStr = variableMap.get(rightStr);
			}
			if(rhsExpr.getLeft() instanceof ExprVar && variableMap.containsKey(leftStr)){
				leftStr = variableMap.get(leftStr);
			}

			rhs = ExprBinaryString(rhsExpr, leftStr, rightStr);
		}
		else {
			rhs = stmt.getRHS().toString();
		}

		if(! outSet.contains(rhs)){
			// Print stuff
			outSet.add(lhs.toString());
			printLine(variableMap.getOrDefault(rhs, rhs));
//			if(variableMap.containsKey(rhs)) {
//				printLine(variableMap.get(rhs));
//			}
//			else{
//				printLine(rhs);
//			}
		}

		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		if(PRINT_ACTUAL_CODE){
			printLine(stmt.toString()  + ';');
		}

		return super.visitStmtAssign(stmt);
	}

	public String ExprBinaryString(ExprBinary expr, String leftStr, String rightStr)
	{
		String theOp = expr.getOpString();
		String lstr, rstr;
		if(expr.getLeft() instanceof ExprConstInt || expr.getLeft() instanceof ExprVar){
			lstr = leftStr;
		}else{
			lstr = "(" + leftStr + ")";
		}
		if(expr.getRight() instanceof ExprConstInt || expr.getRight() instanceof ExprVar){
			rstr = rightStr;
		}else{
			rstr = "(" + rightStr + ")";
		}
		return lstr + " " + theOp + " " + rstr;
	}

	@Override
	public Object visitStmtBreak(StmtBreak stmt)
	{
		printLine(stmt.toString());
		return super.visitStmtBreak(stmt);
	}

	@Override
	public Object visitStmtContinue(StmtContinue stmt)
	{
		printLine(stmt.toString());
		return super.visitStmtContinue(stmt);
	}

	@Override
	public Object visitStmtEmpty(StmtEmpty stmt)
	{
		printLine(stmt.toString());
		return super.visitStmtEmpty(stmt);
	}

	@Override
	public Object visitStmtExpr(StmtExpr stmt)
	{
		ExprFunCall exprFunCall = (ExprFunCall)stmt.getExpression();
		List<Expression> params = exprFunCall.getParams();

		// Priyan: check if it assigns isEmptyList() => if it is, then set it as empty list check
		if(exprFunCall.getName().equals(IS_EMPTY_LIST_FUNC)){
			emptyListCheck = params.get(params.size() - 1).toString();
		}

		String lastParamString = params.get(params.size() - 1).toString();
		String funcName = exprFunCall.getName();

		// Test print
		try {
			List<String> paramStrList = new ArrayList<String>();
			for (Expression p : params) {
				// Do nothing
				String pStr = p.toString();
				if (!pStr.startsWith("_out")) {
					paramStrList.add(pStr);
					continue;
				} else if (pStr.equals(lastParamString)) {
					continue;
				}
				paramStrList.add(variableMap.get(pStr));
			}

			String paramStr = String.join(",", paramStrList);

			if(funcName.equals(HEAD_LIST_FUNC)){
				String fStr = "head";
				variableMap.put(lastParamString, fStr);
			}
			else if(funcName.equals(TAIL_LIST_FUNC)){
				String fStr = "tail";
				variableMap.put(lastParamString, fStr);
			}
			else if(funcName.equals(EMPTY_LIST_FUNC)){
				String fStr = "empty";
				variableMap.put(lastParamString, fStr);
			}
			else if(funcName.equals(ADD_LIST_FUNC)){
				Collections.reverse(paramStrList);
				paramStr = String.join(",", paramStrList);
				String fStr = "link(" + paramStr + ")";
				variableMap.put(lastParamString, fStr);
			}
			else if(funcName.equals(Max_FUNC)){
				if(paramStr.equals("0,0")){
					String fStr = "0";
					variableMap.put(lastParamString, fStr);
				}
				else {
					String fStr = "" + "num-max" + "(" + paramStr + ")";
					variableMap.put(lastParamString, fStr);
				}
			}
			else {
				String fStr = "" + funcName + "(" + paramStr + ")";
				variableMap.put(lastParamString, fStr);
			}
		}
		catch (Exception e){
			printLine(e.toString());
		}


		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }
		{
			if(PRINT_ACTUAL_CODE){
				printLine(stmt.toString() + ";");
			}
		}
		return stmt;
	}

	public Object visitStmtFunDef(StmtFunDecl stmt) {
		printLine(stmt.toString());
		return stmt;
	}

	@Override
	public Object visitStmtReturn(StmtReturn stmt)
	{
		// priyan edit: Don't print return statement
		if(PRINT_ACTUAL_CODE){
			printLine(stmt.toString());
		}
		return super.visitStmtReturn(stmt);
	}

	// @Override
	// public Object visitStmtAngelicSolve(StmtAngelicSolve stmt) {
	// printLine("angelic_solve");
	// return super.visitStmtAngelicSolve(stmt);
	// }

	@Override
	public Object visitStmtVarDecl(StmtVarDecl stmt)
	{
		if(outtags && stmt.getTag() != null){ out.println("T="+stmt.getTag()); }

		for (int i = 0; i < stmt.getNumVars(); i++) {
			variableMap.put(stmt.getName(i), stmt.getInit(i).toString());
//			printLine("" + stmt.getName(i) + ": " + stmt.getInit(i).toString());
			String str = stmt.getType(i) + " " + stmt.getName(i);
			if (stmt.getInit(i) != null) {
				str += " = " + stmt.getInit(i);
			}

			if(PRINT_ACTUAL_CODE){
				printLine(str + ";");
			}
		}

		return stmt;
	}

	@Override
	public Object visitFieldDecl(FieldDecl field)
	{
		printLine(field.toString());
		return super.visitFieldDecl(field);
	}

	public Object visitStmtReorderBlock(StmtReorderBlock block){
		printLine("reorder");
		block.getBlock().accept(this);
		return block;
	}

	public Object visitStmtInsertBlock (StmtInsertBlock sib) {
		printLine ("insert");
		sib.getInsertStmt ().accept (this);
		printLine ("into");
		sib.getIntoBlock ().accept (this);
		return sib;
	}

	public Object visitStmtAtomicBlock(StmtAtomicBlock block){
		if(outtags && block.getTag() != null){ out.println("T="+block.getTag()); }
		if(block.isCond()){
			printLine("atomic(" + block.getCond().accept(this) + ")");
		}else{
			printLine("atomic");
		}
		visitStmtBlock (block.getBlock());
		return block;
	}

	@Override
	public Object visitStructDef(StructDef ts) {
		return  ts;
//		printLine("struct " + ts.getName() + " {");
//		for (StructFieldEnt ent : ts.getFieldEntriesInOrder()) {
//			printLine("    " + ent.getType().toString() + " " + ent.getName() + ";");
//		}
//		for (Entry<String, Vector<Annotation>> at : ts.annotationSet()) {
//			for (Annotation ann : at.getValue()) {
//				printLine("    " + ann);
//			}
//		}
//		printLine("}");
//		return ts;
	}

	@Override
	public Object visitStmtMinLoop(StmtMinLoop stmtMinLoop) {
		printTab();
		print("minloop");
		printIndentedStatement(stmtMinLoop.getBody());
		return stmtMinLoop;
	}

	@Override
	public Object visitStmtMinimize(StmtMinimize stmtMinimize) {
		printLine("minimize(" + stmtMinimize.getMinimizeExpr().accept(this) + ")");
		return stmtMinimize;
	}

	@Override
	public Object visitCudaSyncthreads(CudaSyncthreads cudaSyncthreads) {
		printLine("__syncthreads();");
		return cudaSyncthreads;
	}
}
