# Grab all archives into one place

def Archives():
    import _file
    import git
    return [
        _file.File,
        git.Git
    ]
Archives = Archives()
