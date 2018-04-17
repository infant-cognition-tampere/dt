# Data transformation library for python

import csv

def read_file(filepath):
    """ Read file and return datarows """
    with open(filepath, "rb") as inputfile:

        print "Reading file " + filepath + "..."

        reader = csv.reader(inputfile, delimiter='\t')

        # loop all datarows
        rows = []
        for row in reader:
            # store the row
            rows.append(row)

        return rows

def save_file(filepath, rows):
    """ Save a file to disk. """

    print "Writing " + filepath

    with open(filepath, "wb") as outputfile:
        writer = csv.writer(outputfile, delimiter='\t')

        # write datarows
        for row in rows:
            writer.writerow(row)

        print "Done."

def pick_columns(rows, list_of_column_names):
	""" Pick columns from the original file and return rows with new columns. """

    column_indexes = []

    # find column indexes for each column
    for l in list_of_column_names:
        col_id = _get_column_index(rows, l)
        if col_id is not None:
            column_indexes.append(col_id)

    newrows = []
    for row in rows:
        newrow = []

        # loop all column indexes and collect    
        for cind in column_indexes:
            newrow.append(row[cind])

        newrows.append(newrow)
		
    return newrows

def _get_column_index(rows, column_id):
    """ Internal function that return column index for column_id. """

    headers = rows[0]

    if column_id in headers:
        return headers.index(column_id)
    else:
        return None
    # add an exeption if not found?

def fill_tag(rows, column_id, start_tag, end_tag, filler_tag, fill_end_tag):
    """ Fill values between start_tag and end_tag with filler_tag. """

    column = _get_column_index(rows, column_id)

    # make a new list and append headers which don't go to loop
    newrows = []
    newrows.append(rows[0])

    filling_active = False
    for row in rows[1:]:
        newrow = row[:]
        tag = newrow[column]

        # inspect conditions
        if tag == start_tag:
            filling_active = True

        if filling_active:
            if tag == end_tag:
                # check whether encountered end tag
                filling_active = False
                if fill_end_tag:
                    # fill end tag also anyways
                    newrow[column] = filler_tag
            else:
                # just fill as normal
                newrow[column] = filler_tag

        newrows.append(newrow)
    return newrows

def replace_string(rows, column_id, str_to_replace, replacement_str):
    """ Replace strings in a column with replacement string. """

    column = _get_column_index(rows, column_id)

    print "Replacing strings \"" + str_to_replace + "\" in column " + \
        column_id + "(" +str(column) + ") with \"" + replacement_str + "\""

    # grab header information
    headers = rows[0]

    # loop all datarows
    newrows = []
    replaced = 0
    for row in rows[0:]:
        current_value = row[column]

        # COPY list (not just list pointer)
        newrow = row[:]

        # check if the value is the one needed to replace
        if current_value == str_to_replace:
            # replace
            newrow[column] = replacement_str
            replaced = replaced + 1

        # store the row
        newrows.append(newrow)

    print "Total number of strings replaced: " + str(replaced) + "."
    return newrows