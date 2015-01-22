package timeseries;

import java.util.Calendar;

public class TSTransformedData {

	private Calendar date;
	private double smaDiff;
	private double emaDiff;
	
	public Calendar getDate() {
		return date;
	}
	public void setDate(Calendar date) {
		this.date = date;
	}
	public double getSmaDiff() {
		return smaDiff;
	}
	public void setSmaDiff(double smaDiff) {
		this.smaDiff = smaDiff;
	}
	public double getEmaDiff() {
		return emaDiff;
	}
	public void setEmaDiff(double emaDiff) {
		this.emaDiff = emaDiff;
	}
	
	
}
