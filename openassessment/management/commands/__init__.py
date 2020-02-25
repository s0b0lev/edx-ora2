"""
Utilities shared by management commands.
"""
import csv
import six


def write_csv(file_handle, header, rows):
    """
    Writes the given header, rows to the file_handle as UTF-8 encoded CSV.
    """
    def _encode_row(data_list):
        """
        Properly encode ora2 responses for transcription into a .csv
        """
        processed_row = []

        for item in data_list:
            new_item = six.text_type(item).encode('utf-8') if six.PY2 else six.text_type(item)
            processed_row.append(new_item)

        return processed_row

    writer = csv.writer(file_handle, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)

    writer.writerow(_encode_row(header))
    for row in rows:
        writer.writerow(_encode_row(row))
