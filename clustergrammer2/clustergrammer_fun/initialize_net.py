def main(self, widget=None):

  if hasattr(self, 'meta_cat') == False:
    self.meta_cat = False
    # print('meta_cet False')

  self.dat = {}
  self.dat['nodes'] = {}
  self.dat['nodes']['row'] = []
  self.dat['nodes']['col'] = []
  self.dat['mat'] = []

  self.dat['node_info'] = {}
  for inst_rc in self.dat['nodes']:
    self.dat['node_info'][inst_rc] = {}
    self.dat['node_info'][inst_rc]['ini'] = []
    self.dat['node_info'][inst_rc]['clust'] = []
    self.dat['node_info'][inst_rc]['rank'] = []
    self.dat['node_info'][inst_rc]['info'] = []
    self.dat['node_info'][inst_rc]['cat'] = []
    self.dat['node_info'][inst_rc]['value'] = []

  # check if net has categories predefined
  if hasattr(self, 'persistent_cat_colors') == False:
    self.persistent_cat_colors = False
    found_cats = False
  else:
    found_cats = True
    inst_cat_colors = self.viz['cat_colors']

  # initialize matrix colors
  ###########################
  has_matrix_colors = False
  if hasattr(self, 'viz'):
    if 'matrix_colors' in self.viz:
      has_matrix_colors = True

  if has_matrix_colors:
    matrix_colors = self.viz['matrix_colors']
  else:
    matrix_colors = {}
    matrix_colors['pos'] = 'red'
    matrix_colors['neg'] = 'blue'

  # add widget if necessary
  if widget != None:
    self.widget_class = widget

  self.viz = {}
  self.viz['row_nodes'] = []
  self.viz['col_nodes'] = []
  self.viz['links'] = []
  self.viz['mat'] = []

  if found_cats == False:
    self.viz['cat_colors'] = {}
    self.viz['cat_colors']['row'] = {}
    self.viz['cat_colors']['col'] = {}
  else:
    self.viz['cat_colors'] = inst_cat_colors

  self.viz['matrix_colors'] = matrix_colors

  self.sim = {}


def viz(self, reset_cat_colors=False):

  # keep track of old cat_colors
  old_cat_colors = self.viz['cat_colors']

  if 'matrix_colors' in self.viz:
    matrix_colors = self.viz['matrix_colors']

  self.viz = {}
  self.viz['row_nodes'] = []
  self.viz['col_nodes'] = []
  self.viz['links'] = []
  self.viz['mat'] = []

  if reset_cat_colors == True:
    self.viz['cat_colors'] = {}
    self.viz['cat_colors']['row'] = {}
    self.viz['cat_colors']['col'] = {}
  else:
    self.viz['cat_colors'] = old_cat_colors

  self.viz['matrix_colors'] = matrix_colors
