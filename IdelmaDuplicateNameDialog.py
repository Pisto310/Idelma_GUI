from IdelmaWarningDialog import IdelmaWarningDialog


class IdelmaDuplicateNameDialog(IdelmaWarningDialog):
    """
    Warning dialog that pop-up when user tries to create
    a section with an already existing name
    """
    def __init__(self):
        super().__init__()

