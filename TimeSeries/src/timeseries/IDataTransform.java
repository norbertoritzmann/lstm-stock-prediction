package timeseries;

import weka.core.Instances;

public interface IDataTransform {
	public Instances process(Instances instances, TransformParameters params);
	
//	public TransformParameters getParameters();
}
