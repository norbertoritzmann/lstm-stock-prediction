package timeseries.preprocess.analitics;

import java.util.List;

import timeseries.IDataTransform;
import timeseries.TransformParameters;
import timeseries.model.CSVFields;
import timeseries.util.ArrayUtil;
import weka.core.Attribute;
import weka.core.Instances;

import com.tictactec.ta.lib.Core;
import com.tictactec.ta.lib.MAType;
import com.tictactec.ta.lib.MInteger;
import com.tictactec.ta.lib.RetCode;

public class StochasticDataTransformer implements IDataTransform {

	private Core lib = new Core();
	private MInteger outBegIdx = new MInteger();
	private MInteger outNBElement = new MInteger();
	
	@Override
	public Instances process(Instances instances, TransformParameters params) {
		int outLength = instances.size() - params.getPeriods();
		String attributeName = "Stoch";
		
		try {
			double[] pricesClose = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.ADJ_CLOSE));
			double[] pricesHigh = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.HIGHT));
			double[] pricesLow = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.LOW));
			double[] outSlowK = new double[outLength];
			double[] outSlowD = new double[outLength];
			
			RetCode ret = lib.stoch(0, outLength, pricesHigh, pricesLow, pricesClose, params.getStochKFastPeriods(), params.getStochKSlowPeriods(), MAType.Sma, params.getStochDSlowPeriods(), MAType.Sma, outBegIdx, outNBElement, outSlowK, outSlowD);
			
			List<String> strValuesK = ArrayUtil.getDoubleArrayToStringArray(outSlowK);
			List<String> strValuesD = ArrayUtil.getDoubleArrayToStringArray(outSlowD);
			instances.insertAttributeAt(new Attribute(attributeName+"K", strValuesK), instances.numAttributes());
			instances.insertAttributeAt(new Attribute(attributeName+"D", strValuesD), instances.numAttributes());
			
			return instances;
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		}
		
		return null;
	}

}
