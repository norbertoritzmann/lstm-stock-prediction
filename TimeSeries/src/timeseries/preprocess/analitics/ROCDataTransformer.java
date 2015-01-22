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

public class ROCDataTransformer implements IDataTransform {

	private Core lib = new Core();
	private MInteger outBegIdx = new MInteger();
	private MInteger outNBElement = new MInteger();
	
	@Override
	public Instances process(Instances instances, TransformParameters params) {
		int outLength = instances.size() - params.getPeriods();
		String attributeName = "ROC" + params.getPeriods();
		
		try {
			double[] prices = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.ADJ_CLOSE));
			double[] outReal = new double[outLength];
			RetCode ret = lib.roc(0, outLength, prices, params.getPeriods(), outBegIdx, outNBElement, outReal);
			
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
