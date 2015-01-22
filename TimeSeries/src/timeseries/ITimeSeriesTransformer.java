package timeseries;

import java.util.List;

import timeseries.model.Quote;

public interface ITimeSeriesTransformer {

	public double[] transform(List<Quote> quotes, TransformParameters parameters);

}
