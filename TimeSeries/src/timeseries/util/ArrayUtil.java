package timeseries.util;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

public class ArrayUtil {

	/**
	 * Extrai um campo do objeto dentro do array,
	 * @throws InvocationTargetException 
	 * @throws NoSuchMethodException 
	 **/
	public static List<String> getDoubleArrayToStringArray(double[] d) {
		List<String> s = new ArrayList<String>();

		for (int i = 0; i < s.size(); i++) {
			s.add(String.valueOf(d[i]));
		}
		
		return s;
	}
	/**
	 * Extrai um campo do objeto dentro do array,
	 * @throws InvocationTargetException 
	 * @throws NoSuchMethodException 
	 **/
	public static double[] getDoubleFromObjectCol(Object[] arr, String col) throws SecurityException, NoSuchFieldException, IllegalArgumentException, IllegalAccessException, InvocationTargetException, NoSuchMethodException {
		
		if(arr == null || arr.length == 0) {
			return null;
		}
		
		double[] valores = new double[arr.length];
		
		String methodName = "get" + col.substring(0,1).toUpperCase() + col.substring(1);
		Class clazz = arr[0].getClass();
		Method method = clazz.getMethod(methodName, null);
		
		for (int i = 0; i < arr.length; i++) {
			double value = (Double) method.invoke(arr[i], null);
			valores[i] = value;
		}
		
		return valores;
	}
}
