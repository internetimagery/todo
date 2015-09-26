# Generic Elements

class PlaceHolder(MayaElement):
    """
    An empty placeholder
    """
    def _buildGUI(s):
        s.root = cmds.columnLayout(adj=True)
        s.attach = s.root
