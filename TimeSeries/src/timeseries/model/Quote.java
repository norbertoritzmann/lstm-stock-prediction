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
package timeseries.model;

import java.util.Date;

import timeseries.Formatter;


public final class Quote {

    private String dateAsString;

    private Integer id;

    private Date date;

    private double open;

    private double close;

    private double low;

    private double high;

    private long volume;

    public Quote() {
    	
    }
    
    public Quote(final Date date) {
        if (date == null) {
            throw new IllegalArgumentException("date must not be null");
        }
        this.date = date;
    }

    public Quote(final Date date, final double close) {
        if (date == null) {
            throw new IllegalArgumentException("date must not be null");
        }
        this.date = date;
        this.close = close;
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public boolean equals(final Object obj) {
        if (obj == this) {
            return true;
        }
        if (!(obj instanceof Quote)) {
            return false;
        }
        final Quote quote = (Quote) obj;
        boolean stockEquals = true;
//        if (stock != null) {
//            stockEquals = stock.equals(quote.stock);
//        } else if (quote.stock != null) {
//            stockEquals = quote.stock.equals(stock);
//        }
        return date.getTime() == quote.date.getTime() && stockEquals;
    }

    public double getClose() {
        return close;
    }

    public Date getDate() {
        return date;
    }

    public String getDateAsString() {
        if (dateAsString == null) {
            dateAsString = Formatter.formatDate(date);
        }
        return dateAsString;
    }

    public double getHigh() {
        return high;
    }

    public Integer getId() {
        return id;
    }

    public double getLow() {
        return low;
    }

    public double getOpen() {
        return open;
    }

//    public Stock getStock() {
//        return stock;
//    }

    public double getValue() {
        return close;
    }

    public long getVolume() {
        return volume;
    }

    public boolean isBearish() {
        return close < open;
    }

    public boolean isBullish() {
        return close > open;
    }

    public void setClose(final double close) {
        this.close = close;
    }

    public void setHigh(final double high) {
        this.high = high;
    }

    public void setLow(final double low) {
        this.low = low;
    }

    public void setOpen(final double open) {
        this.open = open;
    }

//    public void setStock(final Stock stock) {
//        this.stock = stock;
//    }

    public void setVolume(final long volume) {
        this.volume = volume;
    }

    /**
     * Returns the code representation of this quote. This is a helper method to create JUnit setup
     * code from real data.
     * 
     * @return the code representation of this quote
     */
    public String toJava() {
        final StringBuilder builder = new StringBuilder();
        final String simpleName = this.getClass().getSimpleName();
        builder.append("new " + simpleName + "(\"");
        builder.append(getDateAsString() + "\", ");
        builder.append(open + "f, ");
        builder.append(high + "f, ");
        builder.append(low + "f, ");
        builder.append(close + "f, ");
        builder.append(volume + ");");
        return builder.toString();
    }

    @Override
    public String toString() {
        return (new StringBuilder())
        		.append("date:" + getDateAsString())
                .append(", open: " + open)
                .append(", high: " + high)
                .append(", low: " + low)
                .append(",close: " + close)
                .append(", volume: "+ volume)
                .toString();
    }
}
