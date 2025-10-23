import bpy
import mathutils

FACIAL_BONES_TO_KEY = [
    "mixamorig:Head", "mixamorig:HeadTop_End", "mixamorig:L_Ear", "mixamorig:Jaw",
    "mixamorig:TongueBack", "mixamorig:TongueMid", "mixamorig:TongueTip",
    "mixamorig:Chin", "mixamorig:LowerChin", "mixamorig:L_Temple",
    "mixamorig:L_IOuterBrow", "mixamorig:L_MidBrow", "mixamorig:L_InnerBrow",
    "mixamorig:L_Eye", "mixamorig:L_EyelidLower", "mixamorig:L_EyelidUpper",
    "mixamorig:L_InnerCheek", "mixamorig:L_LowerCheek", "mixamorig:L_LipCorner",
    "mixamorig:L_LipCornerLowTweak", "mixamorig:L_LipCornerUpTweak",
    "mixamorig:L_LipLower", "mixamorig:L_LipUpper", "mixamorig:LipMidLower",
    "mixamorig:L_CheekFold", "mixamorig:L_Nostril", "mixamorig:Scalp",
    "mixamorig:L_OuterCheek", "mixamorig:R_LipLower", "mixamorig:RightNostril",
    "mixamorig:R_CheekFold", "mixamorig:R_LowerCheek", "mixamorig:R_gLipCorner",
    "mixamorig:R_gLipCornerLowTweak", "mixamorig:R_gLipCornerUpTweak",
    "mixamorig:R_LipUpper", "mixamorig:R_OuterCheek", "mixamorig:MidBrows",
    "mixamorig:R_InnerBrow", "mixamorig:R_MidBrow", "mixamorig:R_IOuterBrow",
    "mixamorig:R_Eye", "mixamorig:R_EyelidLower", "mixamorig:R_EyelidUpper",
    "mixamorig:R_Temple", "mixamorig:R_Ear", "mixamorig:R_InnerCheek", "mixamorig:Throat"
]

def apply_pose_keyframes(armature_name: str, frame: int):
    bpy.ops.object.mode_set(mode='POSE')
    armature = bpy.data.objects.get(armature_name)
    if not armature:
        print(f"Armature '{armature_name}' not found.")
        return

    pose_bones = armature.pose.bones
    bpy.context.view_layer.update()
    armature.update_tag(refresh={'DATA'})

    for bone_name in FACIAL_BONES_TO_KEY:
        if bone_name in pose_bones:
            bone = pose_bones[bone_name]
            bone.keyframe_insert(data_path="location", frame=frame, group=bone_name)
            bone.keyframe_insert(data_path="rotation_quaternion", frame=frame, group=bone_name)
            bone.keyframe_insert(data_path="scale", frame=frame, group=bone_name)

    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"Inserted keyframes for {armature_name} at frame {frame}")

# ------------------------------------------------------------------------
# REST POSE (For Initialization and Transitions)
# ------------------------------------------------------------------------
# In pose_functions.py

# ... (other functions)

def apply_rest_pose(armature_name: str, frame: int):
    """
    Sets the default pose by inserting keyframes for the default values 
    WITHOUT clearing transforms, allowing the keyframes to define the neutral state.
    """
    armature = bpy.data.objects.get(armature_name)
    if not armature or armature.type != 'ARMATURE':
        return

    # --- CRITICAL CHANGE: DO NOT USE pose.loc_clear()! ---
    # The keyframes inserted by apply_pose_keyframes must define the neutral pose.
    # To use this simplified Rest Pose, the neutral pose must be the default for the bone properties.
    
    # We rely on the fact that L/R/S transforms are 0/0/1 at the true rest pose.
    # Simply keyframe the default values.

    apply_pose_keyframes(armature_name, pose_functions.FACIAL_BONES_TO_KEY, frame)
    print(f"Rest/Neutral keyframe inserted at frame {frame}")

# ... (rest of the functions)
# ------------------------------------------------------------------------
# VISEME POSES
# ------------------------------------------------------------------------

def apply_closed_lips_pose(armature_name: str, frame: int):
    """
    Sets the pose for ClosedLips (P, B, M) by applying the character's 
    default Rest Pose, as they are functionally the same.
    """
    apply_rest_pose(armature_name, frame)
    # print(f"ClosedLips pose applied (as Rest Pose) and keyframed at frame {frame}")


def applylipopensmallpose(armaturename: str, frame: int):
    armature = bpy.data.objects.get(armaturename)
    if not armature: return
    # CRITICAL FIX: Use the variable name 'pose_bones' consistently
    pose_bones = armature.pose.bones 
    
    # --- BONE NAMES CORRECTED TO COLON CONVENTION ---
    pose_bones["mixamorig:Jaw"].location = mathutils.Vector((0.0, -0.31852, 0.00197))
    pose_bones["mixamorig:Jaw"].rotation_quaternion = mathutils.Quaternion((0.99741, 0.07186, 0.0, 0.0))
    
    pose_bones["mixamorig:L_LipCorner"].location = mathutils.Vector((-0.42067, 0.0, 0.0))
    pose_bones["mixamorig:L_LipCorner"].scale = mathutils.Vector((0.85532, 1.0, 1.0))
    pose_bones["mixamorig:L_LipCornerLowTweak"].location = mathutils.Vector((0.0, -1.42089, 0.00882))
    pose_bones["mixamorig:L_LipCornerUpTweak"].location = mathutils.Vector((0.0, 0.25379, -0.00157))
    pose_bones["mixamorig:L_LipLower"].location = mathutils.Vector((0.0, -0.86978, 0.00540))
    pose_bones["mixamorig:L_LipLower"].scale = mathutils.Vector((1.14264, 0.67124, 1.14263))
    pose_bones["mixamorig:L_LipUpper"].location = mathutils.Vector((0.0, 0.56191, -0.00350))
    
    pose_bones["mixamorig:LipMidLower"].location = mathutils.Vector((0.0, -1.62752, -0.01725))
    pose_bones["mixamorig:LipMidLower"].scale = mathutils.Vector((1.14264, 0.67124, 1.14263))
    
    pose_bones["mixamorig:R_LipLower"].location = mathutils.Vector((0.0, -0.86978, 0.00540))
    pose_bones["mixamorig:R_LipLower"].scale = mathutils.Vector((1.14264, 0.67124, 1.14263))
    pose_bones["mixamorig:R_gLipCorner"].location = mathutils.Vector((0.42067, 0.0, 0.0))
    pose_bones["mixamorig:R_gLipCorner"].scale = mathutils.Vector((0.85532, 1.0, 1.0))
    pose_bones["mixamorig:R_gLipCornerLowTweak"].location = mathutils.Vector((0.0, -1.42089, 0.00882))
    pose_bones["mixamorig:R_gLipCornerUpTweak"].location = mathutils.Vector((0.0, 0.25379, -0.00157))
    pose_bones["mixamorig:R_LipUpper"].location = mathutils.Vector((0.0, 0.56191, -0.00350))

    bones_to_key = [
        "mixamorig:Jaw", "mixamorig:L_LipCorner", "mixamorig:L_LipCornerLowTweak", "mixamorig:L_LipCornerUpTweak",  
        "mixamorig:L_LipLower", "mixamorig:L_LipUpper", "mixamorig:LipMidLower", "mixamorig:R_LipLower",  
        "mixamorig:R_gLipCorner", "mixamorig:R_gLipCornerLowTweak", "mixamorig:R_gLipCornerUpTweak", "mixamorig:R_LipUpper"
    ]
    apply_pose_keyframes(armaturename, bones_to_key, frame)
    # print(f"LipOpenSmall pose applied and keyframed at frame {frame}")


def apply_lip_wide_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones
    
    pose_bones['mixamorig:Neck'].location = mathutils.Vector((-0.00000, -0.00009, 0.00009))
    pose_bones['mixamorig:Head'].location = mathutils.Vector((-0.00000, 0.00013, -0.00001))
    pose_bones['mixamorig:Jaw'].location = mathutils.Vector((-0.00000, -0.25739, 0.00159))
    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((0.99983, 0.01837, 0.00000, -0.00000))
    pose_bones['mixamorig:TongueBack'].location = mathutils.Vector((0.00000, 0.00001, -0.00000))
    pose_bones['mixamorig:TongueMid'].location = mathutils.Vector((-0.00000, 0.00001, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].location = mathutils.Vector((0.27251, 0.00000, -0.00000))
    pose_bones['mixamorig:L_LipCorner'].scale = mathutils.Vector((1.09372, 1.00000, 1.00000))
    pose_bones['mixamorig:L_LipCornerLowTweak'].location = mathutils.Vector((-0.00000, -0.24079, 0.00149))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((-0.00000, -0.24079, 0.00149))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((0.00000, 0.51778, -0.00321))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((-0.00000, -0.94049, 0.00584))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((-0.00000, -0.24079, 0.00149))
    pose_bones['mixamorig:R_gLipCorner'].location = mathutils.Vector((-0.27251, -0.00000, 0.00000))
    pose_bones['mixamorig:R_gLipCorner'].scale = mathutils.Vector((1.09372, 1.00000, 1.00000))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].location = mathutils.Vector((-0.00000, -0.24079, 0.00149))
    pose_bones['mixamorig:R_LipUpper'].location = mathutils.Vector((0.00000, 0.51778, -0.00321))
    
    bones_to_key = [
        'mixamorig:Neck', 'mixamorig:Head', 'mixamorig:Jaw', 'mixamorig:TongueBack', 
        'mixamorig:TongueMid', 'mixamorig:L_LipCorner', 'mixamorig:L_LipCornerLowTweak', 
        'mixamorig:L_LipLower', 'mixamorig:L_LipUpper', 'mixamorig:LipMidLower', 
        'mixamorig:R_LipLower', 'mixamorig:R_gLipCorner', 'mixamorig:R_gLipCornerLowTweak', 
        'mixamorig:R_LipUpper'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"LipWide pose applied and keyframed at frame {frame}")


def apply_lip_open_big_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones

    pose_bones['mixamorig:Neck'].location = mathutils.Vector((-0.00000, -0.00009, 0.00009))
    pose_bones['mixamorig:Jaw'].location = mathutils.Vector((0.00000, -1.64445, 0.01021))
    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((0.99918, 0.04052, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].location = mathutils.Vector((0.03582, 0.16089, -0.00100))
    pose_bones['mixamorig:L_LipCorner'].scale = mathutils.Vector((1.01232, 0.92739, 0.92739))
    pose_bones['mixamorig:L_LipCornerLowTweak'].location = mathutils.Vector((0.00000, -2.18090, 0.17386))
    pose_bones['mixamorig:L_LipCornerLowTweak'].scale = mathutils.Vector((1.00000, 0.60808, 0.99999))
    pose_bones['mixamorig:L_LipCornerUpTweak'].location = mathutils.Vector((0.00000, 0.57010, 0.15225))
    pose_bones['mixamorig:L_LipCornerUpTweak'].scale = mathutils.Vector((1.00000, 0.63409, 0.99999))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((0.00000, -2.18221, -0.03846))
    pose_bones['mixamorig:L_LipLower'].scale = mathutils.Vector((1.00000, 0.60808, 0.99999))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((0.00000, 0.42902, -0.00266))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((0.00000, -2.18324, -0.20309))
    pose_bones['mixamorig:LipMidLower'].scale = mathutils.Vector((1.00000, 0.60808, 0.99999))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((-0.00000, -2.18221, -0.03846))
    pose_bones['mixamorig:R_LipLower'].scale = mathutils.Vector((1.00000, 0.60808, 0.99999))
    pose_bones['mixamorig:R_gLipCorner'].location = mathutils.Vector((-0.03582, 0.16089, -0.00100))
    pose_bones['mixamorig:R_gLipCorner'].scale = mathutils.Vector((1.01232, 0.92739, 0.92739))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].location = mathutils.Vector((-0.00000, -2.18090, 0.17386))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].scale = mathutils.Vector((1.00000, 0.60808, 0.99999))
    pose_bones['mixamorig:R_gLipCornerUpTweak'].location = mathutils.Vector((0.00000, 0.57010, 0.15225))
    pose_bones['mixamorig:R_gLipCornerUpTweak'].scale = mathutils.Vector((1.00000, 0.63409, 0.99999))
    pose_bones['mixamorig:R_LipUpper'].location = mathutils.Vector((0.00000, 0.42902, -0.00266))

    bones_to_key = [
        'mixamorig:Neck', 'mixamorig:Jaw', 'mixamorig:L_LipCorner', 'mixamorig:L_LipCornerLowTweak', 
        'mixamorig:L_LipCornerUpTweak', 'mixamorig:L_LipLower', 'mixamorig:L_LipUpper', 
        'mixamorig:LipMidLower', 'mixamorig:R_LipLower', 'mixamorig:R_gLipCorner', 
        'mixamorig:R_gLipCornerLowTweak', 'mixamorig:R_gLipCornerUpTweak', 'mixamorig:R_LipUpper'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"LipOpenBig pose applied and keyframed at frame {frame}")


def apply_oo_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones

    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((0.99900, 0.04464, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].location = mathutils.Vector((-0.59168, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].scale = mathutils.Vector((0.79650, 1.00000, 1.00000))
    pose_bones['mixamorig:L_LipCornerLowTweak'].location = mathutils.Vector((-0.22262, -0.76171, 0.13393))
    pose_bones['mixamorig:L_LipCornerLowTweak'].scale = mathutils.Vector((0.89401, 0.88218, 1.28941))
    pose_bones['mixamorig:L_LipCornerUpTweak'].location = mathutils.Vector((-0.23362, 0.25666, 0.78128))
    pose_bones['mixamorig:L_LipCornerUpTweak'].scale = mathutils.Vector((0.89296, 1.01627, 1.05989))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((-0.52621, -0.76277, -0.03717))
    pose_bones['mixamorig:L_LipLower'].scale = mathutils.Vector((0.58191, 0.57421, 0.83927))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((-0.71145, 0.37826, -0.01110))
    pose_bones['mixamorig:L_LipUpper'].scale = mathutils.Vector((0.45193, 0.62289, 0.64962))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((0.00000, -1.10456, -0.16773))
    pose_bones['mixamorig:LipMidLower'].scale = mathutils.Vector((0.69334, 0.68417, 0.99999))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((0.52621, -0.76277, -0.03717))
    pose_bones['mixamorig:R_LipLower'].scale = mathutils.Vector((0.58191, 0.57421, 0.83927))
    pose_bones['mixamorig:R_gLipCorner'].location = mathutils.Vector((0.59168, 0.00000, 0.00000))
    pose_bones['mixamorig:R_gLipCorner'].scale = mathutils.Vector((0.79650, 1.00000, 1.00000))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].location = mathutils.Vector((0.22262, -0.76171, 0.13393))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].scale = mathutils.Vector((0.89401, 0.88218, 1.28941))
    pose_bones['mixamorig:R_gLipCornerUpTweak'].location = mathutils.Vector((0.23362, 0.25666, 0.78128))
    pose_bones['mixamorig:R_gLipCornerUpTweak'].scale = mathutils.Vector((0.89296, 1.01627, 1.05989))
    pose_bones['mixamorig:R_LipUpper'].location = mathutils.Vector((0.71145, 0.37826, -0.01110))
    pose_bones['mixamorig:R_LipUpper'].scale = mathutils.Vector((0.45193, 0.62289, 0.64962))

    bones_to_key = [
        'mixamorig:Jaw', 'mixamorig:L_LipCorner', 'mixamorig:L_LipCornerLowTweak', 
        'mixamorig:L_LipCornerUpTweak', 'mixamorig:L_LipLower', 'mixamorig:L_LipUpper', 
        'mixamorig:LipMidLower', 'mixamorig:R_LipLower', 'mixamorig:R_gLipCorner', 
        'mixamorig:R_gLipCornerLowTweak', 'mixamorig:R_gLipCornerUpTweak', 'mixamorig:R_LipUpper'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"OO pose applied and keyframed at frame {frame}")


def apply_ee_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones
    
    pose_bones['mixamorig:Jaw'].location = mathutils.Vector((0.00000, -0.00002, -0.00001))
    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((0.99933, 0.03662, 0.00000, -0.00000))
    pose_bones['mixamorig:TongueBack'].location = mathutils.Vector((0.00000, 0.00001, -0.00000))
    pose_bones['mixamorig:TongueMid'].location = mathutils.Vector((-0.00000, 0.00001, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].location = mathutils.Vector((0.66420, 0.00000, -0.00000))
    pose_bones['mixamorig:L_LipCorner'].scale = mathutils.Vector((1.22844, 1.00000, 1.00000))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((-0.00000, -0.74618, 0.00463))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((0.00000, 0.33037, -0.00205))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((-0.00000, -0.74618, 0.00463))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((-0.00000, -0.74618, 0.00463))
    
    bones_to_key = [
        'mixamorig:Jaw', 'mixamorig:TongueBack', 'mixamorig:TongueMid', 'mixamorig:L_LipCorner', 
        'mixamorig:L_LipLower', 'mixamorig:L_LipUpper', 'mixamorig:LipMidLower', 'mixamorig:R_LipLower'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"EE pose applied and keyframed at frame {frame}")


def apply_fv_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones

    pose_bones['mixamorig:Neck'].location = mathutils.Vector((-0.00000, -0.00009, 0.00009))
    pose_bones['mixamorig:Neck'].rotation_quaternion = mathutils.Quaternion((1.00000, 0.00000, -0.00000, -0.00000))
    pose_bones['mixamorig:Head'].location = mathutils.Vector((-0.00000, 0.00013, -0.00001))
    pose_bones['mixamorig:Head'].rotation_quaternion = mathutils.Quaternion((1.00000, -0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:Jaw'].location = mathutils.Vector((-0.00000, -0.00002, -0.00001))
    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((1.00000, -0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:TongueBack'].location = mathutils.Vector((0.00000, 0.00001, -0.00000))
    pose_bones['mixamorig:TongueMid'].location = mathutils.Vector((-0.00000, 0.00001, 0.00000))
    pose_bones['mixamorig:L_LipCornerLowTweak'].location = mathutils.Vector((0.00000, -0.19026, -0.00972))
    pose_bones['mixamorig:L_LipCornerLowTweak'].rotation_quaternion = mathutils.Quaternion((0.97468, -0.22362, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipCornerUpTweak'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipLower'].rotation_quaternion = mathutils.Quaternion((0.97468, -0.22362, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((0.00000, 0.56058, -0.00348))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((0.00000, 0.19567, -0.03341))
    pose_bones['mixamorig:LipMidLower'].rotation_quaternion = mathutils.Quaternion((0.97468, -0.22362, 0.00000, 0.00000))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:R_LipLower'].rotation_quaternion = mathutils.Quaternion((0.97468, -0.22362, 0.00000, 0.00000))
    pose_bones['mixamorig:R_gLipCorner'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].location = mathutils.Vector((0.00000, -0.19026, -0.00972))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].rotation_quaternion = mathutils.Quaternion((0.97468, -0.22362, 0.00000, 0.00000))
    pose_bones['mixamorig:R_gLipCornerUpTweak'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:R_LipUpper'].location = mathutils.Vector((0.00000, 0.56058, -0.00348))

    bones_to_key = [
        'mixamorig:Neck', 'mixamorig:Head', 'mixamorig:Jaw', 'mixamorig:TongueBack', 'mixamorig:TongueMid', 
        'mixamorig:L_LipCornerLowTweak', 'mixamorig:L_LipCornerUpTweak', 'mixamorig:L_LipLower', 
        'mixamorig:L_LipUpper', 'mixamorig:LipMidLower', 'mixamorig:R_LipLower', 
        'mixamorig:R_gLipCorner', 'mixamorig:R_gLipCornerLowTweak', 'mixamorig:R_gLipCornerUpTweak', 
        'mixamorig:R_LipUpper'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"FV pose applied and keyframed at frame {frame}")


def apply_th_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones

    pose_bones['mixamorig:Jaw'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((0.99919, 0.04023, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].location = mathutils.Vector((0.23440, 0.37677, -0.00234))
    pose_bones['mixamorig:L_LipCorner'].scale = mathutils.Vector((1.08062, 1.00000, 1.00000))
    pose_bones['mixamorig:L_LipCornerLowTweak'].location = mathutils.Vector((0.00000, -0.55701, 0.14101))
    pose_bones['mixamorig:L_LipCornerLowTweak'].scale = mathutils.Vector((1.00000, 0.66374, 0.99999))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((0.00000, -0.55814, -0.04116))
    pose_bones['mixamorig:L_LipLower'].scale = mathutils.Vector((1.00000, 0.66374, 0.99999))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((0.10465, 0.37677, -0.00234))
    pose_bones['mixamorig:L_LipUpper'].scale = mathutils.Vector((1.08062, 1.00000, 1.00000))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((0.00000, -0.55902, -0.18241))
    pose_bones['mixamorig:LipMidLower'].scale = mathutils.Vector((1.00000, 0.66374, 0.99999))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:R_LipLower'].rotation_quaternion = mathutils.Quaternion((0.97468, -0.22362, 0.00000, 0.00000))
    
    bones_to_key = [
        'mixamorig:Jaw', 'mixamorig:L_LipCorner', 'mixamorig:L_LipCornerLowTweak', 'mixamorig:L_LipLower', 
        'mixamorig:L_LipUpper', 'mixamorig:LipMidLower', 'mixamorig:R_LipLower'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"TH pose applied and keyframed at frame {frame}")


def apply_chsh_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones

    pose_bones['mixamorig:Jaw'].location = mathutils.Vector((0.00000, 0.00000, 0.00000))
    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((0.99919, 0.04023, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].location = mathutils.Vector((-0.54898, 0.00000, 0.00000))
    pose_bones['mixamorig:L_LipCorner'].scale = mathutils.Vector((0.81119, 1.00000, 1.00000))
    pose_bones['mixamorig:L_LipCornerLowTweak'].location = mathutils.Vector((-0.10380, -0.12442, 0.17496))
    pose_bones['mixamorig:L_LipCornerLowTweak'].scale = mathutils.Vector((0.95058, 0.57420, 0.99999))
    pose_bones['mixamorig:L_LipCornerUpTweak'].location = mathutils.Vector((-0.13563, 0.12508, -0.01701))
    pose_bones['mixamorig:L_LipCornerUpTweak'].scale = mathutils.Vector((0.93786, 1.03124, 1.00000))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((-0.30039, -0.61242, -0.05270))
    pose_bones['mixamorig:L_LipLower'].scale = mathutils.Vector((0.76133, 0.57420, 0.99999))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((-0.28549, 0.63721, 0.00255))
    pose_bones['mixamorig:L_LipUpper'].scale = mathutils.Vector((0.78007, 1.03124, 1.00000))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((0.00000, -0.61353, -0.23156))
    pose_bones['mixamorig:LipMidLower'].scale = mathutils.Vector((0.76133, 0.57420, 0.99999))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((0.30039, -0.61242, -0.05270))
    pose_bones['mixamorig:R_LipLower'].scale = mathutils.Vector((0.76133, 0.57420, 0.99999))
    
    bones_to_key = [
        'mixamorig:Jaw', 'mixamorig:L_LipCorner', 'mixamorig:L_LipCornerLowTweak', 'mixamorig:L_LipCornerUpTweak', 
        'mixamorig:L_LipLower', 'mixamorig:L_LipUpper', 'mixamorig:LipMidLower', 'mixamorig:R_LipLower'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"ChSh pose applied and keyframed at frame {frame}")


def apply_kg_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones
    
    # We rely on apply_rest_pose to clear all non-jaw facial transforms
    pose_bones['mixamorig:Jaw'].rotation_quaternion = mathutils.Quaternion((0.99942, 0.03416, 0.00000, 0.00000))
    
    bones_to_key = ['mixamorig:Jaw']
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"KG pose applied and keyframed at frame {frame}")


def apply_lr_pose(armature_name: str, frame: int):
    armature = bpy.data.objects.get(armature_name)
    if not armature: return
    pose_bones = armature.pose.bones

    pose_bones['mixamorig:Jaw'].location = mathutils.Vector((0.00000, -0.75689, 0.00470))
    pose_bones['mixamorig:TongueMid'].location = mathutils.Vector((0.00000, 0.58324, -0.00362))
    
    pose_bones['mixamorig:L_LipCorner'].location = mathutils.Vector((-0.28069, 0.30408, -0.00189))
    pose_bones['mixamorig:L_LipCorner'].scale = mathutils.Vector((0.90346, 1.00000, 1.00000))
    pose_bones['mixamorig:L_LipCornerLowTweak'].location = mathutils.Vector((0.00000, -0.96960, 0.08958))
    pose_bones['mixamorig:L_LipCornerLowTweak'].scale = mathutils.Vector((1.00000, 0.79574, 0.99999))
    pose_bones['mixamorig:L_LipCornerUpTweak'].location = mathutils.Vector((-0.08871, 0.15287, -0.00095))
    pose_bones['mixamorig:L_LipCornerUpTweak'].scale = mathutils.Vector((0.95935, 1.00000, 1.00000))
    pose_bones['mixamorig:L_LipLower'].location = mathutils.Vector((0.00000, -0.97028, -0.02108))
    pose_bones['mixamorig:L_LipLower'].scale = mathutils.Vector((1.00000, 0.79574, 0.99999))
    pose_bones['mixamorig:L_LipUpper'].location = mathutils.Vector((-0.14777, 0.56161, -0.00349))
    pose_bones['mixamorig:L_LipUpper'].scale = mathutils.Vector((0.88617, 1.00000, 1.00000))
    pose_bones['mixamorig:LipMidLower'].location = mathutils.Vector((0.00000, -0.97082, -0.10688))
    pose_bones['mixamorig:LipMidLower'].scale = mathutils.Vector((1.00000, 0.79574, 0.99999))
    pose_bones['mixamorig:R_LipLower'].location = mathutils.Vector((0.00000, -0.97028, -0.02108))
    pose_bones['mixamorig:R_LipLower'].scale = mathutils.Vector((1.00000, 0.79574, 0.99999))
    pose_bones['mixamorig:R_gLipCorner'].location = mathutils.Vector((0.28069, 0.30408, -0.00189))
    pose_bones['mixamorig:R_gLipCorner'].scale = mathutils.Vector((0.90346, 1.00000, 1.00000))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].location = mathutils.Vector((0.00000, -0.96960, 0.08958))
    pose_bones['mixamorig:R_gLipCornerLowTweak'].scale = mathutils.Vector((1.00000, 0.79574, 0.99999))
    pose_bones['mixamorig:R_gLipCornerUpTweak'].location = mathutils.Vector((0.08871, 0.15287, -0.00095))
    pose_bones['mixamorig:R_gLipCornerUpTweak'].scale = mathutils.Vector((0.95935, 1.00000, 1.00000))
    pose_bones['mixamorig:R_LipUpper'].location = mathutils.Vector((0.14777, 0.56161, -0.00349))
    pose_bones['mixamorig:R_LipUpper'].scale = mathutils.Vector((0.88617, 1.00000, 1.00000))
    
    bones_to_key = [
        'mixamorig:Jaw', 'mixamorig:TongueMid', 'mixamorig:L_LipCorner', 'mixamorig:L_LipCornerLowTweak', 
        'mixamorig:L_LipCornerUpTweak', 'mixamorig:L_LipLower', 'mixamorig:L_LipUpper', 
        'mixamorig:LipMidLower', 'mixamorig:R_LipLower', 'mixamorig:R_gLipCorner', 
        'mixamorig:R_gLipCornerLowTweak', 'mixamorig:R_gLipCornerUpTweak', 'mixamorig:R_LipUpper'
    ]
    apply_pose_keyframes(armature_name, bones_to_key, frame)
    # print(f"LR viseme pose applied and keyframed at frame {frame}")