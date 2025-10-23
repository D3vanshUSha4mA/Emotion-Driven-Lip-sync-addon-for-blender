bl_info = {
    "name": "Automatic Lip Sync Addon",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "category": "Animation",
    "description": "Generates lip sync animation using Whisper and G2P."
}

import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Panel, PropertyGroup
import subprocess
import os
import json
import mathutils
import sys

# Import the local module containing pose functions
from . import pose_functions 


# ------------------------------------------------------------------------
# 0. CONFIGURATION AND MAPPING
# ------------------------------------------------------------------------

VISEME_TO_FUNCTION = {
    "Rest/Neutral": 'apply_rest_pose', 
    "ClosedLips": 'apply_closed_lips_pose',
    "LipOpenSmall": 'applylipopensmallpose',
    "LipWide": 'apply_lip_wide_pose',
    "LipOpenBig": 'apply_lip_open_big_pose',
    "OO": 'apply_oo_pose',
    "EE": 'apply_ee_pose',
    "FV": 'apply_fv_pose',
    "TH": 'apply_th_pose',
    "ChSh": 'apply_chsh_pose',
    "KG": 'apply_kg_pose',
    "LR": 'apply_lr_pose'
}


# ------------------------------------------------------------------------
# 1. DATA / PROPERTIES
# ------------------------------------------------------------------------

class PhonemeSettings(PropertyGroup):
    audio_file: StringProperty(
        name="Audio File",
        description="Select audio file for phoneme extraction",
        subtype='FILE_PATH'
    )
    armature_name: StringProperty(
        name="Target Armature",
        default="mixamorig",
        description="Name of the Armature object to animate (e.g., 'mixamorig')"
    )

# ------------------------------------------------------------------------
# 2. EXTERNAL EXECUTION LOGIC
# ------------------------------------------------------------------------

def extract_phonemes_external(audio_path):
    script_path = os.path.join(os.path.dirname(__file__), "open_AI_whisper.py")
    output_path = os.path.splitext(audio_path)[0] + "_phonemes.json"
    
    # !!! CRITICAL: YOUR PYTHON INSTALLATION PATH !!!
    python_exe = r"C:\Program Files\Python310\python.exe" 

    try:
        audio_path = os.path.abspath(audio_path)
        if not os.path.exists(audio_path): return None

        cmd = [python_exe, script_path, "--audio", audio_path, "--out", output_path]
        
        print(f"Running external script: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy(), timeout=300)

        if result.returncode != 0:
            print("Error running Whisper script; return code:", result.returncode)
            print("[Subprocess stdout]:", result.stdout)
            print("[Subprocess stderr]:", result.stderr)
            return None

        return output_path if os.path.exists(output_path) else None

    except Exception as e:
        print(f"Error calling phoneme extraction: {e}")
        return None

# ------------------------------------------------------------------------
# 3. OPERATORS
# ------------------------------------------------------------------------

class PHONEME_OT_Extract(Operator):
    bl_idname = "wm.phoneme_extract"
    bl_label = "Extract Timings (Run Whisper)"

    def execute(self, context):
        settings = context.scene.phoneme_settings
        audio_path = settings.audio_file

        if not audio_path or not os.path.exists(audio_path):
            self.report({'ERROR'}, "Please select a valid audio file.")
            return {'CANCELLED'}

        output_json = extract_phonemes_external(audio_path)

        if output_json:
            self.report({'INFO'}, f"Timings saved to: {output_json}")
        else:
            self.report({'ERROR'}, "Failed to extract timings. Check console.")
            return {'CANCELLED'}

        return {'FINISHED'}


class PHONEME_OT_Animate(Operator):
    bl_idname = "wm.phoneme_animate"
    bl_label = "Generate Lip Sync Animation"

    def execute(self, context):
        settings = context.scene.phoneme_settings
        armature_name = settings.armature_name
        
        # 1. Check & Load
        armature = bpy.data.objects.get(armature_name)
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, f"Armature '{armature_name}' not found.")
            return {'CANCELLED'}

        json_path = os.path.splitext(settings.audio_file)[0] + "_phonemes.json"
        if not os.path.exists(json_path):
            self.report({'ERROR'}, f"Viseme JSON file not found. Run extraction first.")
            return {'CANCELLED'}

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                viseme_data = json.load(f).get("phoneme_timings", [])
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load viseme data: {e}")
            return {'CANCELLED'}

        if not viseme_data:
            self.report({'ERROR'}, "No viseme timings found.")
            return {'CANCELLED'}
            
        # 2. Setup Mode and Scene
        if context.active_object != armature:
             bpy.ops.object.select_all(action='DESELECT')
             armature.select_set(True)
             context.view_layer.objects.active = armature
        
        # Switch to Pose Mode (REQUIRED for keyframing pose bones)
        bpy.ops.object.mode_set(mode='POSE')
        
        # Clear existing animation data
        if armature.animation_data and armature.animation_data.action:
            bpy.data.actions.remove(armature.animation_data.action)
        armature.animation_data_clear()

        # --- CRITICAL FIX 1: Create a new Action for keyframes ---
        armature.animation_data_create()
        armature.animation_data.action = bpy.data.actions.new(name="LipSyncAction")


        fps = context.scene.render.fps
        start_time_sec = viseme_data[0]['start']
        end_time_sec = viseme_data[-1]['end']
        
        # Set frame range with a buffer
        initial_rest_frame = max(1, int(start_time_sec * fps) - int(fps * 0.1)) 
        final_end_frame = int(end_time_sec * fps) + int(fps * 0.5) 
        
        context.scene.frame_start = initial_rest_frame
        context.scene.frame_end = final_end_frame

        # 3. Apply Initial Rest Pose (Before dialogue starts)
        pose_functions.apply_rest_pose(armature_name, initial_rest_frame)
        
        # 4. Apply Viseme Poses and Keyframes (Look-Ahead Logic)
        for i, viseme_item in enumerate(viseme_data):
            current_viseme_code = viseme_item['viseme']
            start_sec = viseme_item['start']
            end_sec = viseme_item['end']
            
            start_frame = int(start_sec * fps)
            # Peak frame is slightly after the start (30ms for hold)
            peak_frame = start_frame + max(1, int(fps * 0.03)) 
            end_frame = int(end_sec * fps)

            # Get the function for the CURRENT viseme
            current_pose_func_name = VISEME_TO_FUNCTION.get(current_viseme_code)

            # --- A. Apply Viseme Pose (Peak Frame) ---
            if current_pose_func_name and hasattr(pose_functions, current_pose_func_name):
                current_pose_func = getattr(pose_functions, current_pose_func_name)
                
                # Apply the current pose to define the peak of the sound.
                current_pose_func(armature_name, peak_frame)

            # --- B. Set Transition (End Frame) ---
            
            # CRITICAL FIX 2: We must have a function call that forces the transition 
            # at the end_frame, even if it's the Rest Pose.
            
            if i + 1 < len(viseme_data):
                # Look ahead: Use the NEXT viseme's pose at the CURRENT viseme's END frame
                next_viseme_code = viseme_data[i+1]['viseme']
                next_pose_func_name = VISEME_TO_FUNCTION.get(next_viseme_code)

                if next_pose_func_name and hasattr(pose_functions, next_pose_func_name):
                     next_pose_func = getattr(pose_functions, next_pose_func_name)
                     
                     # Apply the NEXT pose at the CURRENT viseme's END frame.
                     next_pose_func(armature_name, end_frame)
                else:
                     # Fallback to Rest if the next viseme is unknown (Treating gaps as Rest)
                     pose_functions.apply_rest_pose(armature_name, end_frame) 

            else:
                # If this is the LAST viseme, transition back to the Rest Pose.
                pose_functions.apply_rest_pose(armature_name, final_end_frame)
        
        # CRITICAL FIX 3: Force Pose Refresh after keyframing is complete
        bpy.context.view_layer.update()

        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, f"Lip Sync Animation Generated on '{armature_name}'!")
        return {'FINISHED'}

# ------------------------------------------------------------------------
# 4. PANEL / UI & REGISTRATION
# ------------------------------------------------------------------------

class PHONEME_PT_MainPanel(Panel):
    bl_label = "Automatic Lip Sync"
    bl_idname = "PHONEME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Phoneme"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.phoneme_settings

        # 1. Extraction
        box = layout.box()
        box.label(text="1. Audio and Extraction", icon='SOUND')
        box.prop(settings, "audio_file")
        box.operator("wm.phoneme_extract", text="Run Whisper & Extract Timings")
        
        # 2. Animation Settings
        box = layout.box()
        box.label(text="2. Animation Settings", icon='OUTLINER_OB_ARMATURE')
        box.prop(settings, "armature_name")
        
        # 3. Generation
        box = layout.box()
        box.label(text="3. Generate Animation", icon='POSE_HLT')
        box.operator("wm.phoneme_animate", text="Generate Keyframes")


def register():
    bpy.utils.register_class(PhonemeSettings)
    bpy.utils.register_class(PHONEME_OT_Extract)
    bpy.utils.register_class(PHONEME_OT_Animate)
    bpy.utils.register_class(PHONEME_PT_MainPanel)
    bpy.types.Scene.phoneme_settings = bpy.props.PointerProperty(type=PhonemeSettings)


def unregister():
    bpy.utils.unregister_class(PhonemeSettings)
    bpy.utils.unregister_class(PHONEME_OT_Extract)
    bpy.utils.unregister_class(PHONEME_OT_Animate)
    bpy.utils.unregister_class(PHONEME_PT_MainPanel)
    del bpy.types.Scene.phoneme_settings