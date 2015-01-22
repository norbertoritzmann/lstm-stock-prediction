package timeseries.preprocess.analitics;

import java.util.List;
import java.util.logging.Logger;

import timeseries.IDataTransform;
import timeseries.TransformParameters;
import timeseries.model.CSVFields;
import timeseries.util.ArrayUtil;
import weka.core.Attribute;
import weka.core.Instances;

import com.tictactec.ta.lib.Core;
import com.tictactec.ta.lib.MInteger;
import com.tictactec.ta.lib.RetCode;

public class MomentumDataTransformer implements IDataTransform {

	private Logger log = Logger.getLogger(this.getClass().getCanonicalName());
	private Core lib = new Core();
	private MInteger outBegIdx = new MInteger();
	private MInteger outNBElement = new MInteger();
	
	@Override
	public Instances process(Instances instances, TransformParameters params) {
		int outLength = instances.size() - params.getPeriods();
		String attributeName = "Momentum" + params.getMomentumPeriods();
		log.info(attributeName);
		
		try {
			double[] prices = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.ADJ_CLOSE));
			double[] outReal = new double[outLength];
			
			RetCode ret = lib.mom(0, outLength, prices, params.getMomentumPeriods(), outBegIdx, outNBElement, outReal);
			
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
