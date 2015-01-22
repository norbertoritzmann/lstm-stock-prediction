/*
 * jCandle, an application for technical chart analysis.
 * Copyright (C) 2012 Hansgeorg Schwibbe. All rights reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see [http://www.gnu.org/licenses/]. 
 */
package timeseries;

import java.text.DecimalFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * This class provides static method to format prices volumes and dates. To ensure thread-safety
 * this class uses <code>ThreadLocal</code> to provide a <code>SimpleDateFormat</code> for each
 * thread.
 * 
 * @author Hansgeorg Schwibbe
 */
public final class Formatter {

    /** SimpleDateFormat is not thread-safe, so give one to each thread */
    private static final ThreadLocal<SimpleDateFormat> DATE_FORMATTER = new ThreadLocal<SimpleDateFormat>() {
        @Override
        protected SimpleDateFormat initialValue() {
            return new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH);
        }
    };

    /** SimpleDateFormat is not thread-safe, so give one to each thread */
    private static final ThreadLocal<SimpleDateFormat> MONTH_FORMATTER = new ThreadLocal<SimpleDateFormat>() {
        @Override
        protected SimpleDateFormat initialValue() {
            return new SimpleDateFormat("yyyy-MM", Locale.ENGLISH);
        }
    };

    private static final ThreadLocal<DecimalFormat> PRICE_FORMATTER = new ThreadLocal<DecimalFormat>() {
        @Override
        protected DecimalFormat initialValue() {
            return new DecimalFormat("0.00");
        }
    };

    private static final ThreadLocal<DecimalFormat> VOLUME_FORMATTER = new ThreadLocal<DecimalFormat>() {
        @Override
        protected DecimalFormat initialValue() {
            return new DecimalFormat("0.00 Mio");
        }
    };

    private Formatter() {
        super();
    }

    /**
     * Formats the specified date.
     * 
     * @param date the date to format
     * @return the formatted date
     */
    public static String formatDate(final Date date) {
        return DATE_FORMATTER.get().format(date);
    }

    /**
     * Formats the specified price.
     * 
     * @param price the date to price
     * @return the formatted price
     */
    public static String formatPrice(final double price) {
        return PRICE_FORMATTER.get().format(price);
    }

    /**
     * Formats the specified price.
     * 
     * @param price the date to price
     * @return the formatted price
     */

    public static String formatPrice(final float price) {
        return PRICE_FORMATTER.get().format(price);
    }

    /**
     * Formats the specified price.
     * 
     * @param price the date to price
     * @return the formatted price
     */
    public static String formatPrice(final Number price) {
        return PRICE_FORMATTER.get().format(price);
    }

    /**
     * Formats the specified volume.
     * 
     * @param vol the date to volume
     * @return the formatted volume
     */
    public static String formatVolume(final double vol) {
        return VOLUME_FORMATTER.get().format(vol);
    }

    /**
     * Formats the specified volume.
     * 
     * @param vol the date to volume
     * @return the formatted volume
     */
    public static String formatVolume(final float vol) {
        return VOLUME_FORMATTER.get().format(vol);
    }

    /**
     * Formats the specified volume.
     * 
     * @param vol the date to volume
     * @return the formatted volume
     */
    public static String formatVolume(final Number vol) {
        return VOLUME_FORMATTER.get().format(vol);
    }

    public static SimpleDateFormat getMonthFormat() {
        return MONTH_FORMATTER.get();
    }

    /**
     * Returns the price formatter for the current thread.
     * 
     * @return the price formatter for the current thread.
     */
    public static DecimalFormat getPriceFormat() {
        return PRICE_FORMATTER.get();
    }

    /**
     * Returns the volume formatter for the current thread.
     * 
     * @return the volume formatter for the current thread.
     */
    public static DecimalFormat getVolumeFormat() {
        return VOLUME_FORMATTER.get();
    }

    /**
     * Parses a date string and returns a matching <code>Date</code> object.
     * 
     * @param dateString the date string to parse
     * @return the date object
     * @throws ParseException
     */
    public static Date parseDate(final String dateString) throws ParseException {
        return DATE_FORMATTER.get().parse(dateString);
    }
}
