from __future__ import annotations
import bpy
from bpy.types import (
    Operator,
)
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    StringProperty,
)


class Options(bpy.types.PropertyGroup):
       
    base_str: StringProperty(name="Base Name")# type: ignore
    
    number_options: EnumProperty(
        name="NumberOPT",
        options={'ENUM_FLAG'},
        default={'ONE'},
        items=(
            ('ZERO', "Start at Zero", ""),
            ('ONE', "Start at 1", ""),
            ('BLANK', "Start with no numbers", ""),
            ),
        ) # type: ignore
     
    include_prior_number: BoolProperty(
        name="Include Prior Character",
        description="Do you want to include tthe character before the Match",
    )# type: ignore
    
    letter_options: EnumProperty(
        name="LetterOPT",
        options={'ENUM_FLAG'},
        default={'START'},
        items=(
            ('START', "Start at A", ""),
            ('BLANK', "Start with no letters", ""),
        ),
    )# type: ignore
    include_prior_letter: BoolProperty(
        name="Include Prior Character",
        description="Do you want to include tthe character before the Match",
    )# type: ignore
    
    lttr_pad: StringProperty(name="Letter Padding Char",maxlen=1,default='0')# type: ignore
    
    let_or_num: EnumProperty(
        name="LetterOPT",
        options={'ENUM_FLAG'},
        default={'LETTER'},
        items=(
            ('LETTER', "Use Letters for new chains", ""),
            ('NUMBER', "Use Numbers for new chains", ""),
        ),   
    )# type: ignore

class WM_OT_chain_name_your_way(Operator):
    bl_idname="wm.chain_name_your_way"
    bl_label="Chain Name Your Way"
    
    this: CollectionProperty(type = Options)#type: ignore
            
    def _get_sel(self,context):
        sel = []
        if context.mode == "POSE":
            sel = context.selected_pose_bones
        elif context.mode == "EDIT_ARMATURE":
            sel = context.selected_editable_bones
        elif context.mode == "OBJECT":
            sel = context.selected_objects
        return sel
    
    def _is_multi_chain(self,sel):
        count = 0
        for s in sel:
            if s.parent not in sel:
                count += 1
        return True if count > 1 else False
    
    def draw(self, context):
        #Create an actual instance of options propertgroup    
        this = self.this
        
        opt = this[0]
        #Build Basic ui structures
        l = self.layout
        box = l.box()
        split = box.split(factor=0.87)
        col = split.column()
        #Create tip on ussage
        box.label(text="#-Numbers | @-Letters")
        if self._is_multi_chain(self._get_sel(context)):
            row = box.row()
            row.prop(opt, "let_or_num")
        #create all the options
        opt_keys = list(opt.__annotations__.keys())
        for o in opt_keys[:-1]:
            row = box.row()
            if o == "lttr_pad":
                col.split(factor =.3)
                row.alignment = 'RIGHT'
            row.prop(opt,o)
         
    def execute(self,context):
        import re
        opt = self.this[0]
        base_str = opt.base_str
        num_re = re.compile(f'(?P<pre>.*[^#])?(?P<mid>#+)(?P<post>.*)?')
        match_num = num_re.match(base_str)
        let_re = re.compile(f'(?P<pre>.*[^@])?(?P<mid>@+)(?P<post>.*)?')
        match_let = let_re.match(base_str)        
         
        if not (match_num or match_let): #or not match_let
            print("add # or @ plz")#make info box later
                    
        sel = self._get_sel(context)
        
        if not sel:
            print("nothing selected") # change to info box
 
        def _starter(type, match, rematch, sel):
            if type is "num":
                pre = match['pre'] if match['pre'] else "" #these are optional matches that can return none so need to be sanatized
                pst = match['post'] if match['post'] else ""
                num=0
                mid = ''
                tpre = pre
                match opt.number_options.pop():
                    case "ZERO":
                        num = 0
                        mid = str(num).rjust(len(match['mid']),'0')
                    case 'ONE':
                        num = 1
                        mid = str(num).rjust(len(match['mid']),'0')                      
                    case "BLANK":
                        if opt.include_prior_number:
                            tpre = pre[:-1]
                        pass
                sel[0].name =  tpre + mid + pst
                return num, pre, pst, mid, tpre
            elif type == "let":
                mlet = let_re.match(sel[0].name) if rematch else match
                pre = mlet['pre'] if mlet['pre'] else "" #these are optional matches that can return none so need to be sanatized
                pst = mlet['post'] if mlet['post'] else ""
                let=''
                mid = ''
                tpre = pre
                match opt.letter_options.pop():
                    case "START":
                        let = 'A'
                        mid = let.rjust(len(mlet['mid']), opt.lttr_pad)                         
                    case "BLANK":
                        if opt.include_prior_letter:
                           tpre = pre[:-1]        
                sel[0].name =  tpre + mid + pst  
                return let, pre, pst, mid, tpre
            
        def _incrament(length, type, value, pad):
            new = ""
            mid = ""
            match type:
                case "let":

                    if not value:
                        new = "A"
                        pass
                    if re.match("^Z+$", value):
                        new = "".join(["A" for i in range(len(value)+1)])
                        pass
                    temp = [c for c in value]
                    for i in range(len(temp)-1, -1,-1):
                        if ord(temp[i]) >= 90:
                            temp[i] = "A"
                            continue
                        else:
                            temp[i] = chr(ord(temp[i])+1)
                            new = "".join(temp)
                            break
                    mid = new.rjust(length, pad)
                case "num":
                    new = int(value) + 1
                    mid = str(new).rjust(length, pad)      
            return mid, new
        
        def _numchange(match, rematch, sel):            
            num, pre, pst, snum, tpre = _starter("num",match, rematch, sel)       
            for s in sel[1:]:             
                snum = ''
                snum, num = _incrament(len(match['mid']),"num", num, "0")
                s.name = pre + snum + pst
         
        def _letchange(match, rematch, sel):                   
            let, pre, pst, slet, tpre = _starter("let",match, rematch, sel)
            mlet = match
            for s in sel[1:]:
                if rematch:
                    mlet = let_re.match(s.name)  
                    pre, pst = mlet["pre"], mlet["post"]                  
                slet = ''
                slet, let = _incrament(len(match['mid']),"let", let, opt.lttr_pad)
                s.name = pre + slet + pst
       
        def _multichain():
            type = {"LETTER":"let","NUMBER":"num"}  
            match = {"LETTER":match_let,"NUMBER":match_num} 
            incrament = {"LETTER": lambda s: chr(ord(s) + 1) ,"NUMBER":lambda i: str(int(i) + 1)}
            re_match = {"LETTER":num_re.match,"NUMBER":let_re.match}
            is_rematch = {"LETTER":True,"NUMBER":False}
            change = {"LETTER":_numchange, "NUMBER":_letchange}
            pad = {"LETTER":opt.lttr_pad, "NUMBER":"0"}
            starters = {"LETTER":"A", "NUMBER":"1"}
            
            let_or_num = opt.let_or_num.pop()
            chain, pre, pst, mid, tpre = _starter(type[let_or_num], match[let_or_num], False, sel)

            tmatch = re_match[let_or_num](tpre+mid+pst)
            fsel = sel
            for s,i in zip(sel[1:],range(1,len(sel))):
                if s.parent not in sel:
                    mid, chain = _incrament(len(match[let_or_num]['mid']), type[let_or_num], chain, pad[let_or_num])
                    tmatch = re_match[let_or_num](pre+mid+pst)
                    fsel = sel[i:]                    
                change[let_or_num](tmatch, is_rematch[let_or_num], fsel)
                     
        if self._is_multi_chain(sel):
            if match_num and match_let:
                _multichain()
            else:
                if match_num:
        


        

        
                    _numchange(match_num, bool(match_let), sel)
                if match_let:       
                    _letchange(match_let, bool(match_num), sel)     
        else:
            if match_num:
                _numchange(match_num, bool(match_let),sel)
            if match_let:       
                _letchange(match_let, bool(match_num),sel)
            
        return{'FINISHED'}
    
    @classmethod
    def poll(cls, context):
        if (context.mode in ("EDIT_ARMATURE","POSE") and (context.selected_bones or context.selected_pose_bones) ) or (context.mode == "OBJECT" and context.selected_objects)  :
            return True
        else: 
            return False
    
    def invoke(self,context,event):   
        self.this.add()   
        base = ""
        if context.active_object:
            match context.mode:
                case "EDIT_ARMATURE":
                    base = ((context.active_bone.name if context.active_bone else "") if  len(context.selected_bones) > 0 else "") if context.selected_bones else ""
                case "POSE":
                    base = ((context.active_bone.name if context.active_bone else "") if  len(context.selected_pose_bones) > 0 else "") if context.selected_pose_bones else ""                    
                case  "OBJECT":
                    base = ((context.active_object.name if context.active_object else "") if  len(context.selected_objects) > 0 else "") if context.selected_objects else ""
        self.this[0].base_str = base
        return context.window_manager.invoke_props_dialog(self, width=400)
