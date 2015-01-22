package timeseries;

import java.util.ArrayList;
import java.util.List;

import timeseries.model.CSVFields;
import weka.core.Attribute;
import weka.core.Instances;

public class DiscretClassNextDaysTransformer implements IDataTransform {

	private final String WILL_DOWN = "0";
	private final String WILL_UP = "1";
	
	@Override
	public Instances process(Instances instances, TransformParameters params) {
		int outLength = instances.size() - params.getPeriods();
		String attributeName = "Class" + params.getFutureClassPeriods() + "Day";
		
		try {
			List<String> futureClass = new ArrayList<String>(outLength);
			double[] pricesClose = instances.attributeToDoubleArray(params.getFieldMapping().getAttributeIndex(CSVFields.ADJ_CLOSE));
			
			for (int i = 0; i < outLength; i++) {
				if(pricesClose[ i ] >= pricesClose[ i + params.getFutureClassPeriods() ]) {
					futureClass.add( WILL_UP );
				} else {
					futureClass.add( WILL_DOWN );
				}
			}
			
			instances.insertAttributeAt(new Attribute(attributeName, futureClass), instances.numAttributes());
			
			return instances;
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		}
		
		return null;
	}

}
