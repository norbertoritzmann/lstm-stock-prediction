package timeseries.flow;

import java.util.Iterator;
import java.util.List;

import timeseries.IDataTransform;
import timeseries.TransformParameters;
import weka.core.Instances;

public abstract class AFlow {
	protected List<IDataTransform> queue;
	protected Iterator<IDataTransform> iterator;
	
	protected TransformParameters parameters;
	protected Instances initialInstances;
	
	public abstract void start(String fileName);
	
	public Instances next(Instances instances) {
		IDataTransform dataTransform = iterator.next();
		
		return dataTransform.process(instances, parameters);
	}
}
