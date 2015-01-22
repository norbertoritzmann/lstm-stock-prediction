package timeseries;

import java.util.Iterator;

import timeseries.flow.AttributeAssembleAndSelectFlow;
import timeseries.model.CSVFields;
import timeseries.model.DataToInstances;
import timeseries.model.FieldMapping;
import weka.core.Instance;
import weka.core.Instances;

public class MainTest {

	public static void main(String[] args) {
//		CSVQuoteParser transform = new CSVQuoteParser();
//		
//		List<Quote> quotes = transform.transform("petr4.csv");
//		SMATransformer sma = new SMATransformer();
//		TransformParameters params = new TransformParameters();
//		params.setPeriods(10);
//		double[] sma5 = sma.transform(quotes, params);
//		
//		for (int i = 0; i < sma5.length; i++) {
//			System.out.print(", " + quotes.get(i).getDateAsString() + "= " + sma5[i]);
//		}
		
		String stock = "petr4.csv";
		AttributeAssembleAndSelectFlow preprocessFlow = new AttributeAssembleAndSelectFlow(new TransformParameters(stock));
		
		preprocessFlow.start(stock);
		
//		try {
//            FieldMapping fieldMapping = new FieldMapping(stock);
//            
//			DataToInstances csvToWeka = new DataToInstances();
//			Instances instances;
//			instances = csvToWeka.getInstancesFromFile(stock);
//		
//			Iterator<Instance> it = instances.listIterator();
//			
//			while(it.hasNext()) {
//				Instance ins = it.next();
//				double value = ins.value(fieldMapping.getAttributeIndex(CSVFields.ADJ_CLOSE));
//				System.out.println("VAL: "+value);
//			}
//		} catch (Exception e) {
//			
//			e.printStackTrace();
//		}
	}

}
