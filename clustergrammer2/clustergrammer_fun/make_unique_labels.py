import pandas as pd

# make_unique_labels

def main(net, df=None):
  '''
  Run in load_data module (which runs when file is loaded or dataframe is loaded),
  check for duplicate row/col names, and add index to names if necesary
  '''
  if df is None:
    df = net.export_df()

  # rows
  #############
  rows = df.index.tolist()
  if type(rows[0]) is str:

    if len(rows) != len(list(set(rows))):
      print('warning: making row names unique')
      new_rows = add_index_list(rows)
      df.index = new_rows

  elif type(rows[0]) is tuple:

    row_names = []
    for inst_row in rows:
      row_names.append(inst_row[0])

    if len(row_names) != len(list(set(row_names))):
      print('warning: making row names unique')
      row_names = add_index_list(row_names)

      # add back to tuple
      new_rows = []
      for inst_index in range(len(rows)):
        inst_row = rows[inst_index]
        new_row = list(inst_row)
        new_row[0] = row_names[inst_index]
        new_row = tuple(new_row)
        new_rows.append(new_row)

      df.index = new_rows

  # cols
  #############
  cols = df.columns.tolist()
  if type(cols[0]) is str:

    # list column names
    if len(cols) != len(list(set(cols))):
      print('warning: making col names unique')
      new_cols = add_index_list(cols)
      df.columns = new_cols

  elif type(cols[0]) is tuple:

    col_names = []
    for inst_col in cols:
      col_names.append(inst_col[0])

    if len(col_names) != len(list(set(col_names))):
      print('warning: making col names unique')
      col_names = add_index_list(col_names)

      # add back to tuple
      new_cols = []
      for inst_index in range(len(cols)):
        inst_col = cols[inst_index]
        new_col = list(inst_col)
        new_col[0] = col_names[inst_index]
        new_col = tuple(new_col)
        new_cols.append(new_col)

      df.columns = new_cols

  # return dataframe with unique names
  return df

def add_index_list(nodes):

  new_nodes = []
  for i in range(len(nodes)):
    index = i + 1
    inst_node = nodes[i]
    new_node = inst_node + '-' + str(index)
    new_nodes.append(new_node)

  return new_nodes
