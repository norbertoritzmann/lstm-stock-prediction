package timeseries.preprocess.attributeselection;

import java.util.Random;

import timeseries.IDataTransform;
import timeseries.TransformParameters;
import weka.attributeSelection.CfsSubsetEval;
import weka.attributeSelection.GreedyStepwise;
import weka.classifiers.AbstractClassifier;
import weka.classifiers.Evaluation;
import weka.classifiers.meta.AttributeSelectedClassifier;
import weka.core.Instances;


public class AttributeSelection implements IDataTransform {

	private AbstractClassifier classifier;
	
	public AttributeSelection(AbstractClassifier classifier) {
		this.classifier = classifier;
	}
	
	@Override
	public Instances process(Instances instances, TransformParameters params) {
		AttributeSelectedClassifier attributeSelection = new AttributeSelectedClassifier();
		CfsSubsetEval eval = new CfsSubsetEval();
	    GreedyStepwise search = new GreedyStepwise();
	    search.setSearchBackwards(true);
	    
	    attributeSelection.setClassifier(this.classifier);
	    attributeSelection.setEvaluator(eval);
	    attributeSelection.setSearch(search);
	    Evaluation evaluation;
		
	    try {
			evaluation = new Evaluation(instances);
			evaluation.crossValidateModel(attributeSelection, instances, 10, new Random(1));
			System.out.println(evaluation.toSummaryString());
		} catch (Exception e) {
			e.printStackTrace();
		}
	    
		return instances;
	}

}
