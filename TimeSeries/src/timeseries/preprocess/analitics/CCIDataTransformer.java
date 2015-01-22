package timeseries.preprocess.analitics;

import java.util.List;

import timeseries.IDataTransform;
import timeseries.TransformParameters;
import timeseries.model.CSVFields;
import timeseries.util.ArrayUtil;
import weka.core.Attribute;
import weka.core.Instances;

import com.tictactec.ta.lib.Core;
import com.tictactec.ta.lib.MInteger;
import com.tictactec.ta.lib.RetCode;

public class CCIDataTransformer implements IDataTransform {

	private Core lib = new Core();
	private MInteger outBegIdx = new MInteger();
	private MInteger outNBElement = new MInteger();
	
	@Override
	public Instances process(Instances instances, TransformParameters params) {
		int outLength = instances.size() - params.getPeriods();
		String attributeName = "CCI" + params.getPeriods();
		
		try {
			double[] pricesClose = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.ADJ_CLOSE));
			double[] pricesHigh = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.HIGHT));
			double[] pricesLow = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.LOW));
			double[] outReal = new double[outLength];
			
			RetCode ret = lib.cci(0, outLength, pricesHigh, pricesLow, pricesClose, params.getPeriods(), outBegIdx, outNBElement, outReal);
			
			List<String> strValues = ArrayUtil.getDoubleArrayToStringArray(outReal);
			instances.insertAttributeAt(new Attribute(attributeName, strValues), instances.numAttributes());
			
			return instances;
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		}
		
		return null;
	}

}
