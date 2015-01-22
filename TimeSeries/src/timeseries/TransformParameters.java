package timeseries;

import timeseries.model.FieldMapping;

public class TransformParameters {

	private int periods = 10;
	private int futureClassPeriods = 1;
	private int smaPeriods = 10;
	private int emaPeriods = 10;
	private int wmaPeriods = 10;
	private int macdSlowPeriods = 7;
	private int macdFastPeriods = 14;
	private int macdOscilatorPeriods = 14;
	private int stochKSlowPeriods = 7;
	private int stochKFastPeriods = 14;
	private int stochDSlowPeriods = 7;
	private int stochDFastPeriods = 14;
	private int rsiPeriods = 6;
	private int biasPeriods = 7;
	private int williamsRPeriods = 7;
	private int momentumPeriods = 7;
	private FieldMapping fieldMapping;
	private double[] parameters;
	
	public TransformParameters(String stockFile) {
		fieldMapping = new FieldMapping(stockFile);
	}

	public int getPeriods() {
		return periods;
	}

	public void setPeriods(int periods) {
		this.periods = periods;
	}

	public FieldMapping getFieldMapping() {
		return fieldMapping;
	}

	public void setFieldMapping(FieldMapping fieldMapping) {
		this.fieldMapping = fieldMapping;
	}

	public double[] getParameters() {
		return parameters;
	}

	public void setParameters(double[] parameters) {
		this.parameters = parameters;
	}

	public int getSmaPeriods() {
		return smaPeriods;
	}

	public void setSmaPeriods(int smaPeriods) {
		this.smaPeriods = smaPeriods;
	}

	public int getEmaPeriods() {
		return emaPeriods;
	}

	public void setEmaPeriods(int emaPeriods) {
		this.emaPeriods = emaPeriods;
	}

	public int getMacdSlowPeriods() {
		return macdSlowPeriods;
	}

	public void setMacdSlowPeriods(int macdSlowPeriods) {
		this.macdSlowPeriods = macdSlowPeriods;
	}

	public int getMacdFastPeriods() {
		return macdFastPeriods;
	}

	public void setMacdFastPeriods(int macdFastPeriods) {
		this.macdFastPeriods = macdFastPeriods;
	}

	public int getMacdOscilatorPeriods() {
		return macdOscilatorPeriods;
	}

	public void setMacdOscilatorPeriods(int macdOscilatorPeriods) {
		this.macdOscilatorPeriods = macdOscilatorPeriods;
	}

	public int getRsiPeriods() {
		return rsiPeriods;
	}

	public void setRsiPeriods(int rsiPeriods) {
		this.rsiPeriods = rsiPeriods;
	}

	public int getBiasPeriods() {
		return biasPeriods;
	}

	public void setBiasPeriods(int biasPeriods) {
		this.biasPeriods = biasPeriods;
	}

	public int getStochKSlowPeriods() {
		return stochKSlowPeriods;
	}

	public void setStochKSlowPeriods(int stochKSlowPeriods) {
		this.stochKSlowPeriods = stochKSlowPeriods;
	}

	public int getStochKFastPeriods() {
		return stochKFastPeriods;
	}

	public void setStochKFastPeriods(int stockKFastPeriods) {
		this.stochKFastPeriods = stockKFastPeriods;
	}

	public int getStochDSlowPeriods() {
		return stochDSlowPeriods;
	}

	public void setStochDSlowPeriods(int stochDSlowPeriods) {
		this.stochDSlowPeriods = stochDSlowPeriods;
	}

	public int getStochDFastPeriods() {
		return stochDFastPeriods;
	}

	public void setStochDFastPeriods(int stockDFastPeriods) {
		this.stochDFastPeriods = stockDFastPeriods;
	}

	public int getWilliamsRPeriods() {
		return williamsRPeriods;
	}

	public void setWilliamsRPeriods(int williamsRPeriods) {
		this.williamsRPeriods = williamsRPeriods;
	}

	public int getFutureClassPeriods() {
		return futureClassPeriods;
	}

	public void setFutureClassPeriods(int futureClassPeriods) {
		this.futureClassPeriods = futureClassPeriods;
	}

	public int getWmaPeriods() {
		return wmaPeriods;
	}

	public void setWmaPeriods(int wmaPeriods) {
		this.wmaPeriods = wmaPeriods;
	}

	public int getMomentumPeriods() {
		return momentumPeriods;
	}

	public void setMomentumPeriods(int momentumPeriods) {
		this.momentumPeriods = momentumPeriods;
	}
	
}
