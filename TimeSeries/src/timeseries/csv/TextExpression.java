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
package timeseries.csv;

/**
 * This expression interprets the text values separated by commas.
 * 
 * @author Hansgeorg Schwibbe
 */
public final class TextExpression implements CsvExpression {

    @Override
    public String interpret(final StringBuilder context) {
        final char charAt = context.charAt(0);
        if (charAt != ',' && charAt != ' ' && charAt != '\t' && charAt != '\"') {
            final int indexOfComma = context.indexOf(",");
            String value;
            if (indexOfComma > 0) {
                value = context.substring(0, indexOfComma);
                context.delete(0, indexOfComma);
            } else {
                value = context.substring(0, context.length());
                context.delete(0, context.length());
            }
            return value;
        }
        return null;
    }
}