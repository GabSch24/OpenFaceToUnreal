# OpenFaceToUnreal
## Introduction
  A python script for use in Unreal Engine 5 that converts an [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace) .csv output into a Unreal Metahuman animation using tha AUs (Action Units) output paramether.
## Prerequisites
  * Unreal Engine
    
      You must have Unreal Engine 5.3.2 (most likely works in any 5.3 release but it is untested) installed and have the Python Editor Script Plugin enabled.
  * Python and Libraries
    
      The pandas library must be installed in the python enviroment used by Unreal, you can find it in your installation folder in \UE_5.3\Engine\Binaries\ThirdParty\Python3\Win64\python.exe (for Windows)
## Usage
  After downloading and adding the script to your Unreal project, you must **add the path to your .csv in the script inside *file_location***, after that, create a new Level Sequence and add your MetaHuman to it, click to select it and run the script using the Terminal found in Output Log with it set to Python.
