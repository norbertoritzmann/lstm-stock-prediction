package timeseries;

import weka.core.Instances;
import weka.core.converters.ArffSaver;

import java.io.File;

/**
 * Helper class for writing ARFF files.
 * 
 * @author  fracpete (fracpete at waikato dot ac dot nz)
 * @version $Revision$
 */
public class DataSink {

  /**
   * Writes a dataset to an ARFF file.
   * 
   * @param filename	the file to write to
   * @param data	the data to write as ARFF
   * @throws Exception	if writing fails
   */
  public static void write(String filename, Instances data) throws Exception {
    ArffSaver saver = new ArffSaver();
    saver.setInstances(data);
    saver.setFile(new File(filename));
    saver.writeBatch();
  }
}