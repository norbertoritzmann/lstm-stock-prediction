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
 * Implementations of the <code>Expression</code> interface are responsible for interpreting
 * specific parts of the CSV context.
 * 
 * @author Hansgeorg Schwibbe
 */
public interface CsvExpression {

    /**
     * Interprets a specific part of the underlying CSV context and returns the interpreted value.
     * 
     * @param context the context to interpret
     * @return the interpreted value
     */
    String interpret(StringBuilder context);
}