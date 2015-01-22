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

import java.util.ArrayList;
import java.util.List;

/**
 * Implements a parser for comma separated values (CSV).
 * 
 * @author Hansgeorg Schwibbe
 */
public final class CsvParser {

    private final List<CsvExpression> expressions = new ArrayList<CsvExpression>();

    public CsvParser() {
        expressions.add(new WhitespaceExpression());
        expressions.add(new CommaExpression());
        expressions.add(new InvertedCommaExpression());
        expressions.add(new TextExpression());
    }

    /**
     * Parse the line containing comma separated values.
     * 
     * @param line a line with comma separated values
     * @return the values as an array
     */
    public String[] parse(final String line) {
        final List<String> values = new ArrayList<String>();
        final StringBuilder context = new StringBuilder(line);
        while (context.length() > 0) {
            final int lastLength = context.length();
            /*
             * Interprets the context, removes interpreted content from the context, and saves the
             * interpreted values in the value list.
             */
            for (final CsvExpression expression : expressions) {
                final String value = expression.interpret(context);
                if (value != null) {
                    values.add(value);
                }
                if (context.length() == 0) {
                    break;
                }
            }
            // Protection against infinite loops
            if (context.length() == lastLength) {
                break;
            }
        }
        return values.toArray(new String[values.size()]);
    }
}
