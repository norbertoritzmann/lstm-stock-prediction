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

public class MACDDataTransformer implements IDataTransform {

	private Core lib = new Core();
	private MInteger outBegIdx = new MInteger();
	private MInteger outNBElement = new MInteger();
	
	@Override
	public Instances process(Instances instances, TransformParameters params) {
		int outLength = instances.size() - params.getPeriods();
		String attributeName = "MACD";
		
		try {
			double[] prices = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.ADJ_CLOSE));
			double[] outMACD = new double[outLength];
			double[] outMACDSignal = new double[outLength];
			double[] outMACDHist = new double[outLength];
			RetCode ret = lib.macd(0, outLength, prices, params.getMacdFastPeriods(), params.getMacdSlowPeriods(), params.getPeriods(), outBegIdx, outNBElement, outMACD, outMACDSignal, outMACDHist);
			
			List<String> strMACD = ArrayUtil.getDoubleArrayToStringArray(outMACD);
			List<String> strMACDSignal = ArrayUtil.getDoubleArrayToStringArray(outMACDSignal);
			List<String> strHist = ArrayUtil.getDoubleArrayToStringArray(outMACDHist);
			instances.insertAttributeAt(new Attribute(attributeName, strMACD), instances.numAttributes());
			instances.insertAttributeAt(new Attribute(attributeName+"Signal", strMACDSignal), instances.numAttributes());
			instances.insertAttributeAt(new Attribute(attributeName+"Hist", strHist), instances.numAttributes());
			
			return instances;
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		}
		
		return null;
	}

}
