package timeseries.model;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.IOUtils;

public class FieldMapping {

	private Map<String, Integer> attributesIndexes = new HashMap<String, Integer>();
	
	public FieldMapping(String stockFile) {
		InputStream inputStream = null;
		
		try {
			String current;
			current = new File( "." ).getCanonicalPath();
	        inputStream = new FileInputStream( new File(current + File.separator + new File(stockFile)));
	        final List<String> readLines = IOUtils.readLines(inputStream);
	        String header = readLines.get(0);
	        this.setup(header);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * HeaderLine: primeira linha do CSV, contém a definição dos atributos em ordem
	 **/
	private void setup(String headerLine) {
		String[] attributesNames = headerLine.split(",");
		
		for (int i = 0; i < attributesNames.length; i++) {
			String name = attributesNames[i];
			
			if(CSVFields.OPEN.equals(name)) {
				attributesIndexes.put(CSVFields.OPEN, i);
			} else if(CSVFields.LOW.equals(name)) {
				attributesIndexes.put(CSVFields.LOW, i);
			} else if(CSVFields.HIGHT.equals(name)) {
				attributesIndexes.put(CSVFields.HIGHT, i);
			} else if(CSVFields.DATE.equals(name)) {
				attributesIndexes.put(CSVFields.DATE, i);
			} else if(CSVFields.CLOSE.equals(name)) {
				attributesIndexes.put(CSVFields.CLOSE, i);
			} else if(CSVFields.ADJ_CLOSE.equals(name)) {
				attributesIndexes.put(CSVFields.ADJ_CLOSE, i);
			} else if(CSVFields.VOLUME.equals(name)) {
				attributesIndexes.put(CSVFields.VOLUME, i);
			}
		}
	}
	
	public Integer getAttributeIndex(String attribute) {
		return attributesIndexes.get(attribute);
	}

}
