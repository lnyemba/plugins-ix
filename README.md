# About Plugins-ix

The goal of this project is to facilitate a plug-n-play architectural style with python i.e have a function in a **file**, **load** it and **execute** it. **Plugins-ix** is fully open-source and feel free to change distribute at will ... giving credit wont hurt ;-)


The **Plugins-ix** is using python libraries (no dependencies) and is made of **three components** :


0. **Loader**

This class loads files from disk, loads the functions and applies provides a means to access the functions


1. **Registry**

This class provides functions to manage a location on disk that serves as registry. Calling code can use this to manage plug-n-play functions on disk.

The registry aggregates a load and allow quick access to a given function

functions are referenced here in the following format **function**@**file** e.g: in the file **demo.py**, the function **foo** will be referenced as ***foo***@***demo***

    #
    # This function will be referenced as copyright@demo

    def copyright():
        return {"copyright":"2024 - 2025, Steve Nyemba", "license":"MIT"}



2. **CLI: plugin-ix**

The command-line interpreter **plugin-ix** helps manage plugins in a given location (considered the registry). It is a great example for how we use registry
