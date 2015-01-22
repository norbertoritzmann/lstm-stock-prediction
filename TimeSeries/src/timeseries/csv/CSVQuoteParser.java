package timeseries.csv;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import org.apache.commons.io.IOUtils;
import timeseries.model.Quote;

public class CSVQuoteParser {

	public static String DATE_FORMAT = "yyyy-MM-dd";
	
	private final CsvParser csvParser = new CsvParser();
	
	public List<Quote> transform(String file) {
		final List<Quote> quotes = new ArrayList<Quote>();
		
        InputStream inputStream = null;
        try {
        	String current = new File( "." ).getCanonicalPath();
            inputStream = new FileInputStream( new File(current + File.separator + file));
            final List<String> readLines = IOUtils.readLines(inputStream);

            /* Parsing received CSV data */
            final SimpleDateFormat tradeDateFormat = new SimpleDateFormat(DATE_FORMAT, Locale.ENGLISH);
            readLines.remove(0); // Remove the header line
            for (final String line : readLines) {
                final String[] quoteInfo = csvParser.parse(line);
                try {
                    final Quote quote = new Quote(tradeDateFormat.parse(quoteInfo[0]));
                    quote.setOpen(Double.parseDouble(quoteInfo[1]));
                    quote.setHigh(Double.parseDouble(quoteInfo[2]));
                    quote.setLow(Double.parseDouble(quoteInfo[3]));
                    //Preço de fechamento não ajustado
//                    quote.setClose(Double.parseDouble(quoteInfo[4]));
                    quote.setVolume(Long.parseLong(quoteInfo[5]));
                    //Preço de fechamento ajustado
                    quote.setClose(Double.parseDouble(quoteInfo[6]));
                    // Replace the existing quote with the present value
                    if (quotes.contains(quote)) {
                        quotes.remove(quote);
                    }
                    quotes.add(quote);
                } catch (final Exception e) {
                    e.printStackTrace();
                }
            }
        } catch (final IOException e) {
            e.printStackTrace();
        } finally {
            IOUtils.closeQuietly(inputStream);
        }
        
		return quotes;
	}

}
