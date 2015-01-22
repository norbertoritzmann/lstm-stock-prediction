package timeseries.model;

import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class DataToInstances {

	
	public Instances getInstancesFromFile(String strFile) throws Exception {
		DataSource source = new DataSource(strFile);
		Instances instances = source.getDataSet();
		
		return instances;
	}
	
	
}
