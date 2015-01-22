package timeseries.flow;

import java.io.File;
import java.util.ArrayList;

import timeseries.DataSink;
import timeseries.DiscretClassNextDaysTransformer;
import timeseries.IDataTransform;
import timeseries.TransformParameters;
import timeseries.model.DataToInstances;
import timeseries.preprocess.analitics.ADDataTransformer;
import timeseries.preprocess.analitics.CCIDataTransformer;
import timeseries.preprocess.analitics.EMADataTransformer;
import timeseries.preprocess.analitics.MACDDataTransformer;
import timeseries.preprocess.analitics.MomentumDataTransformer;
import timeseries.preprocess.analitics.ROCDataTransformer;
import timeseries.preprocess.analitics.RSIDataTransformer;
import timeseries.preprocess.analitics.SMADataTransformer;
import timeseries.preprocess.analitics.StochasticDataTransformer;
import timeseries.preprocess.analitics.WMADataTransformer;
import timeseries.preprocess.analitics.WilliamsRDataTransformer;
import timeseries.preprocess.attributeselection.AttributeSelection;
import timeseries.preprocess.normalization.NormalizeDataTransform;
import weka.classifiers.trees.J48;
import weka.core.Instances;

public class AttributeAssembleAndSelectFlow extends AFlow {
	
	public AttributeAssembleAndSelectFlow(TransformParameters parameters) {
		this.parameters = parameters;
	}
	
	@Override
	public void start(String fileName) {
		try {
			DataToInstances csvToWeka = new DataToInstances();
			initialInstances = csvToWeka.getInstancesFromFile(fileName);

			IDataTransform normalize = new NormalizeDataTransform();
			IDataTransform discretize = new DiscretClassNextDaysTransformer();
			
			IDataTransform adTransform = new ADDataTransformer();
			IDataTransform cciTransform = new CCIDataTransformer();
			IDataTransform emaTransform = new EMADataTransformer();
			IDataTransform macdTransform = new MACDDataTransformer();
			IDataTransform momTransform = new MomentumDataTransformer();
			IDataTransform rocTransform = new ROCDataTransformer();
			IDataTransform rsiTransform = new RSIDataTransformer();
			IDataTransform smaTransform = new SMADataTransformer();
			IDataTransform stochTransform = new StochasticDataTransformer();
			IDataTransform wRTransform = new WilliamsRDataTransformer();
			IDataTransform wmaTransform = new WMADataTransformer();
			
			IDataTransform attributeSelection = new AttributeSelection(new J48());
			
			if(queue == null) {
				queue = new ArrayList<IDataTransform>();
			}
			
			queue.add(normalize);
			queue.add(discretize);
			queue.add(adTransform);
			queue.add(cciTransform);
			queue.add(emaTransform);
			queue.add(macdTransform);
			queue.add(momTransform);
			queue.add(rocTransform);
			queue.add(rsiTransform);
			queue.add(smaTransform);
			queue.add(stochTransform);
			queue.add(wRTransform);
			queue.add(wmaTransform);
			queue.add(attributeSelection);
			
			if(iterator == null) {
				iterator = queue.iterator();
			}
			
			Instances instances = initialInstances;
			while( iterator.hasNext() ) {
				next(instances);
			}
			
			DataSink.write("out" + File.separator + fileName + ".arff", instances);
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	
}
