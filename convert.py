import unreal
import pandas as pd

def activate_AU_array(AU : int, values: list[float], start_frame : int):
    CTRL_param = right_side_AU_c_dict.get(AU)
    
    if AU == 9 or AU == 26:
        activate_AU_array_vector2d(AU, values, start_frame)
        return
    
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, unreal.FrameNumber(0), 0.0, set_key = True)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, unreal.FrameNumber(start_frame-1), 0.0, set_key = True)
    frame = start_frame
    for value in values:
        value = value[0]/5.0       #normalizing between 0 and 1
        frame_num = unreal.FrameNumber(frame)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, frame_num, value, set_key = True)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param.replace("_R", "_L"), frame_num, value, set_key = True)
        frame += 1
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, frame_num+1, 0.0, set_key = True)

def activate_AU_array_vector2d(AU : int, values: list[float], start_frame : int):
    CTRL_param = right_side_AU_c_dict.get(AU)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, unreal.FrameNumber(0), unreal.Vector2D.ZERO, set_key = True)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, unreal.FrameNumber(start_frame-1), unreal.Vector2D.ZERO, set_key = True)
    frame = start_frame
    for value in values:
        value = value[0]/5.0       #normalizing between 0 and 1
        frame_num = unreal.FrameNumber(frame)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, frame_num, (0, value), set_key = True)
        if AU == 9:
            unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, "CTRL_L_nose", frame_num, (0, value), set_key = True)
        frame += 1
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, frame_num+1, unreal.Vector2D.ZERO, set_key = True)

def activate_right_side_AU_c(AU : int, start_frame : int, end_frame : int):
    
    CTRL_param = right_side_AU_c_dict.get(AU)
    
    if start_frame > end_frame:
        print("end time before start time")
        return
    
    if AU == 9 or AU == 26:
        activate_symetric_vector2d_AU_c(AU, start_frame, end_frame)
        return
    
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, unreal.FrameNumber(0), 0.0, set_key = True)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, unreal.FrameNumber(start_frame-1), 0.0, set_key = True)
    for i in range(start_frame, end_frame+1):
        frame_num = unreal.FrameNumber(i)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, frame_num, 1.0, set_key = True)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, rig, CTRL_param, frame_num+1, 0.0, set_key = True)
    
def activate_symetric_vector2d_AU_c(AU : int, start_frame : int, end_frame : int):
    
    CTRL_param = right_side_AU_c_dict.get(AU)
    
    vector2d = (0, 1)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, unreal.FrameNumber(0), unreal.Vector2D.ZERO, set_key = True)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, unreal.FrameNumber(start_frame-1), unreal.Vector2D.ZERO, set_key = True)
    for i in range(start_frame, end_frame+1):
        frame_num = unreal.FrameNumber(i)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, frame_num, vector2d, set_key = True)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, rig, CTRL_param, frame_num+1, unreal.Vector2D.ZERO, set_key = True)
    return
    
# Get the Editor world
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
 
# Get the control rig asset
rig = unreal.EditorAssetLibrary.load_asset("/Game/MetaHumans/Common/Face/Face_ControlBoard_CtrlRig")
 
# Get the rig class
rig_class = rig.get_control_rig_class()

# Get level sequence 
level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

# Get actor bindings
ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()

# Get the Control Rigs in Sequencer, returns a list of ControlRigSequencerBindingProxy
rig_proxies = unreal.ControlRigSequencerLibrary.get_control_rigs(level_sequence)
 
# Get the face control rig proxy
rig_proxy = rig_proxies[1]
 
# From the ControlRigSequencerBindingProxy, we can get the ControlRig object
rig = rig_proxy.control_rig

left_side_AU_r_dict = {   
    1 : "CTRL_L_brow_raiseIn",                 # AU01_r,
    2 : "CTRL_L_brow_raiseOut",                # AU02_r,
    4 : "CTRL_L_brow_down",                    # AU04_r,
    5 : "CTRL_L_eye_eyelidU",                  # AU05_r,
    6 : "CTRL_L_eye_cheekRaise",               # AU06_r,
    7 : "CTRL_L_eye_squintInner",              # AU07_r,    #Talvez eye_blink negativo
    9 : "CTRL_L_nose",                         # AU09_r,    # eixo Y
    10: "CTRL_L_mouth_upperLipRaise",          # AU10_r,
    12: "CTRL_L_mouth_cornerPull",             # AU12_r,    #Também tem o sharpCornerPull
    14: "CTRL_L_mouth_dimple",                 # AU14_r,
    15: "CTRL_L_mouth_cornerDepress",          # AU15_r,
    17: "CTRL_L_jaw_ChinRaiseD",               # AU17_r,    #Talvez junto com o ChinRaiseU
    20: "CTRL_L_mouth_stretch",                # AU20_r,
    23: "CTRL_L_mouth_tightenU",               # AU23_r,    #Certamente junto com o tightenD
    25: "CTRL_L_mouth_lowerLipDepress",        # AU25_r,    #Mais relaxar o 17
    26: "CTRL_C_jaw",                          # AU26_r,    # Y+
    45: "CTRL_L_eye_blink"                     # AU45_r     
}

left_side_AU_c_dict = {   
    1 : "CTRL_L_brow_raiseIn",                 # AU01_c,
    2 : "CTRL_L_brow_raiseOut",                # AU02_c,
    4 : "CTRL_L_brow_down",                    # AU04_c,
    5 : "CTRL_L_eye_eyelidU",                  # AU05_c,
    6 : "CTRL_L_eye_cheekRaise",               # AU06_c,
    7 : "CTRL_L_eye_squintInner",              # AU07_c,    #Talvez eye_blink negativo
    9 : "CTRL_L_nose",                         # AU09_c,    # eixo Y
    10: "CTRL_L_mouth_upperLipRaise",          # AU10_c,
    12: "CTRL_L_mouth_cornerPull",             # AU12_c,    #Também tem o sharpCornerPull
    14: "CTRL_L_mouth_dimple",                 # AU14_c,
    15: "CTRL_L_mouth_cornerDepress",          # AU15_c,
    17: "CTRL_L_jaw_ChinRaiseD",               # AU17_c,    #Talvez junto com o ChinRaiseU
    20: "CTRL_L_mouth_stretch",                # AU20_c,
    23: "CTRL_L_mouth_tightenU",               # AU23_c,    #Certamente junto com o tightenD
    25: "CTRL_L_mouth_lowerLipDepress",        # AU25_c,    #Mais relaxar o 17
    26: "CTRL_C_jaw",                          # AU26_c,    # Y+
    28: "CTRL_L_mouth_pressD",                 # AU28_c     # Talvez mais pressU
    45: "CTRL_L_eye_blink"                     # AU45_c     
}

right_side_AU_r_dict = {   
    1 : "CTRL_R_brow_raiseIn",                 # AU01_r,
    2 : "CTRL_R_brow_raiseOut",                # AU02_r,
    4 : "CTRL_R_brow_down",                    # AU04_r,
    5 : "CTRL_R_eye_eyelidU",                  # AU05_r,
    6 : "CTRL_R_eye_cheekRaise",               # AU06_r,
    7 : "CTRL_R_eye_squintInner",              # AU07_r,    #Talvez eye_blink negativo
    9 : "CTRL_R_nose",                         # AU09_r,    # eixo Y
    10: "CTRL_R_mouth_upperLipRaise",          # AU10_r,
    12: "CTRL_R_mouth_cornerPull",             # AU12_r,    #Também tem o sharpCornerPull
    14: "CTRL_R_mouth_dimple",                 # AU14_r,
    15: "CTRL_R_mouth_cornerDepress",          # AU15_r,
    17: "CTRL_R_jaw_ChinRaiseD",               # AU17_r,    #Talvez junto com o ChinRaiseU
    20: "CTRL_R_mouth_stretch",                # AU20_r,
    23: "CTRL_R_mouth_tightenU",               # AU23_r,    #Certamente junto com o tightenD
    25: "CTRL_R_mouth_lowerLipDepress",        # AU25_r,    #Mais relaxar o 17
    26: "CTRL_C_jaw",                          # AU26_r,    # Y+
    45: "CTRL_R_eye_blink"                     # AU45_r     
}

right_side_AU_c_dict = {   
    1 : "CTRL_R_brow_raiseIn",                 # AU01_c,
    2 : "CTRL_R_brow_raiseOut",                # AU02_c,
    4 : "CTRL_R_brow_down",                    # AU04_c,
    5 : "CTRL_R_eye_eyelidU",                  # AU05_c,
    6 : "CTRL_R_eye_cheekRaise",               # AU06_c,
    7 : "CTRL_R_eye_squintInner",              # AU07_c,    #Talvez eye_blink negativo
    9 : "CTRL_R_nose",                         # AU09_c,    # eixo Y
    10: "CTRL_R_mouth_upperLipRaise",          # AU10_c,
    12: "CTRL_R_mouth_cornerPull",             # AU12_c,    #Também tem o sharpCornerPull
    14: "CTRL_R_mouth_dimple",                 # AU14_c,
    15: "CTRL_R_mouth_cornerDepress",          # AU15_c,
    17: "CTRL_R_jaw_ChinRaiseD",               # AU17_c,    #Talvez junto com o ChinRaiseU
    20: "CTRL_R_mouth_stretch",                # AU20_c,
    23: "CTRL_R_mouth_tightenU",               # AU23_c,    #Certamente junto com o tightenD
    25: "CTRL_R_mouth_lowerLipDepress",        # AU25_c,    #Mais relaxar o 17
    26: "CTRL_C_jaw",                          # AU26_c,    # Y+
    28: "CTRL_R_mouth_pressD",                 # AU28_c     # Talvez mais pressU
    45: "CTRL_R_eye_blink"                     # AU45_c     
}

# Test all binary activations
'''
i = 0
for au in right_side_AU_c_dict:

    activate_right_side_AU_c(au, i, i + 30)
    i += 60
'''

# Test all array activations
'''
values = []
for i in range(0, 500, 15):
    i = i/100
    values.append(i)
i = 0
for au in right_side_AU_r_dict:

    activate_AU_array(au,values,i)
    i += values.__len__()*2
'''
file_location = ""
if file_location == "":
    print("You must update your file location in convert.py")
arquivo = pd.read_csv(file_location)
values = []
#valores = arquivo.iloc[:, 679:696]  

offset = 0
for i in right_side_AU_r_dict.keys():
    valor = arquivo.iloc[:, 679+offset:680+offset]
    activate_AU_array(i, valor.values, 0)
    offset += 1
