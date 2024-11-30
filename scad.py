import copy
import opsc
import oobb
import oobb_base
import yaml
import os

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True:
        filter = ""
        #filter = "test"

        #kwargs["save_type"] = "none"
        kwargs["save_type"] = "all"
        
        navigation = False
        navigation = True    

        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        part_default = {} 
        part_default["project_name"] = "oomlout_oobb_holder_electronic_breakout_board_mcu_pico_raspberry_pi" ####### neeeds setting
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["width"] = 4
        p3["height"] = 5
        p3["thickness"] = 3
        part["kwargs"] = p3
        part["name"] = "base"
        parts.append(part)

        
    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")
            if filter in name:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")


    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        generate_navigation(sort = sort)

def get_base(thing, **kwargs):

    #prepare_print = kwargs.get("prepare_print", False)
    prepare_print = kwargs.get("prepare_print", True)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add clamp piece
    if True:
        depth_clamp = 6
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_plate"
        p3["width"] = 1
        h = 3.5
        p3["height"] = h
        p3["depth"] = depth_clamp
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += -((height - h) / 2) * 15
        pos1[2] += depth
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #extra bottom piece
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_plate"
        p3["width"] = 2
        p3["height"] = 1
        p3["depth"] = depth_clamp
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0
        pos1[1] += -height /2 * 15 + 7.5
        pos1[2] += depth
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

        #add screw_countersunk
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["radius_name"] = "m3"
        p3["depth"] = depth_clamp + depth
        p3["holes"] = ["top","bottom","left"]
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        poss = []
        pos11 = copy.deepcopy(pos1)
        pos11[0] += 0
        pos11[1] += -height/2 * 15 + 7.5
        
        pos12 = copy.deepcopy(pos11)
        pos12[1] += 7.5

        poss.append(pos11)
        poss.append(pos12)
        p3["pos"] = poss
        rot1 = copy.deepcopy(rot)
        rot1[1] += 180
        p3["rot"] = rot1
        p3["nut"] = True
        p3["overhang"] = True
        p3["zz"] = "top"
        oobb_base.append_full(thing,**p3)


    #

    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = ["top","bottom","left"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    style = "simple_hole"
    style = "cutout_with_clamp"

    if style == "simple_hole":
        thing = add_simple_hole(thing, **kwargs)
    elif style == "cutout_with_clamp":
        p3 = copy.deepcopy(kwargs)
        shift = [0,5.5,depth]
        p3["shift"] = shift
        thing = add_cutout_with_clamp(thing, **p3)





    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 60
        pos1[2] += depth*2
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[2] += depth
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
###### utilities

def add_cutout_with_clamp(thing, **kwargs):
    depth = kwargs.get("thickness", 3)
    shift = kwargs.get("shift", [0,0,0])
    pos = kwargs.get("pos", [0, 0, 0])
    pos = [pos[i] + shift[i] for i in range(3)]

    #add main cutout square
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    ex = 0.5
    w = 21 + ex
    h = 51 + ex
    d = 1
    p3["size"] = [w,h,d]
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += 0
    pos1[2] += -d
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #wifi cutout cube with clearance
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    ex = 1
    w = 12 + ex
    h = 10 + ex
    d = 2
    p3["size"] = [w,h,d]
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += -11.75
    pos1[2] += 0
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add chip squisher cutout
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    ex = 1
    w = 15 #7 + ex
    h = 36 # + ex
    d = 1
    p3["size"] = [w,h,d]
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += -7.75
    pos1[2] += 0
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add cutouts for headers
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    ex = 0.5
    w = 3 + ex
    h = 51 + ex
    d = depth
    p3["size"] = [w,h,d]    
    #p3["m"] = "#"    
    shift_x = 2.54 * 3.5
    poss = []
    pos1 = copy.deepcopy(pos)
    pos1[2] += -depth
    for i in range(2):
        pos11 = copy.deepcopy(pos1)
        pos11[0] += shift_x
        pos11[1] += 0
        poss.append(pos11)
        shift_x = -shift_x
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    #add usb cutout
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    ex = 0
    w = 11 + ex
    h = 9 + ex
    d = depth
    p3["size"] = [w,h,d]
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += 30
    pos1[2] += -depth
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    return thing


def add_simple_hole(thing, **kwargs):
    depth = kwargs.get("thickness", 3)
    shift = kwargs.get("shift", [0,0,0])
    pos = kwargs.get("pos", [0, 0, 0])    
    pos = [pos[i] + shift[i] for i in range(3)]
        
    #add screw_countersunk m2 
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m2"
    p3["depth"] = depth
    p3["holes"] = ["top","bottom","left"]
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 0
    pos1[1] += 10.2
    shift_x = 5.7
    shift_y = 23.5
    shifts = []
    shifts.append([shift_x,shift_y])
    shifts.append([-shift_x,shift_y])
    shifts.append([shift_x,-shift_y])
    shifts.append([-shift_x,-shift_y])
    poss = []
    for shift in shifts:
        pos11 = copy.deepcopy(pos1)
        pos11[0] += shift[0]
        pos11[1] += shift[1]
        poss.append(pos11)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    rot1[1] += 180
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)


def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]    
    # test if func exists
    if callable(func):            
        func(thing, **kwargs)        
    else:            
        get_base(thing, **kwargs)   
    
    folder = f"scad_output/{thing['id']}"

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        

        opsc.opsc_make_object(f'{folder}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)  

    yaml_file = f"{folder}/working.yaml"
    with open(yaml_file, 'w') as file:
        yaml.dump(part, file)

def generate_navigation(folder="scad_output", sort=["width", "height", "thickness"]):
    #crawl though all directories in scad_output and load all the working.yaml files
    parts = {}
    for root, dirs, files in os.walk(folder):
        if 'working.yaml' in files:
            yaml_file = os.path.join(root, 'working.yaml')
            with open(yaml_file, 'r') as file:
                part = yaml.safe_load(file)
                # Process the loaded YAML content as needed
                part["folder"] = root
                part_name = root.replace(f"{folder}","")
                
                #remove all slashes
                part_name = part_name.replace("/","").replace("\\","")
                parts[part_name] = part

                print(f"Loaded {yaml_file}: {part}")

    pass
    for part_id in parts:
        part = parts[part_id]
        kwarg_copy = copy.deepcopy(part["kwargs"])
        folder_navigation = "navigation"
        folder_source = part["folder"]
        folder_extra = ""
        for s in sort:
            if s == "name":
                ex = part.get("name", "default")
            else:
                ex = kwarg_copy.get(s, "default")
            folder_extra += f"{s}_{ex}/"

        #replace "." with d
        folder_extra = folder_extra.replace(".","d")            
        folder_destination = f"{folder_navigation}/{folder_extra}"
        if not os.path.exists(folder_destination):
            os.makedirs(folder_destination)
        if os.name == 'nt':
            #copy a full directory auto overwrite
            command = f'xcopy "{folder_source}" "{folder_destination}" /E /I /Y'
            print(command)
            os.system(command)
        else:
            os.system(f"cp {folder_source} {folder_destination}")

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)