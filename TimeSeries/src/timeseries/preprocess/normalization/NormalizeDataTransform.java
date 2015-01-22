package timeseries.preprocess.normalization;

import timeseries.IDataTransform;
import timeseries.TransformParameters;
import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Normalize;

public class NormalizeDataTransform implements IDataTransform {

	public Instances process(Instances instances, TransformParameters parameters) {
		Normalize norm = new Normalize();
		try {
			norm.setInputFormat(instances);
			
			if(parameters != null && parameters.getParameters() != null && parameters.getParameters().length > 0) {
				norm.setScale(parameters.getParameters()[0]);
			}
			
			if(parameters != null && parameters.getParameters() != null && parameters.getParameters().length > 1) {
				norm.setTranslation(parameters.getParameters()[1]);
			}
			
			if(parameters == null || parameters.getParameters() == null) {
				norm.setScale(2.0);
				norm.setTranslation(-1.0);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		Instances processed = instances;
		try {
			processed = Filter.useFilter(instances, norm);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		return processed;
	}
}
