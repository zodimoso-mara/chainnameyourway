# chainnameyourway
Blender addon to help with nameing chains of bones all at once. Works in 5.1! (ostenibly)

<img width="428" height="306" alt="image" src="https://github.com/user-attachments/assets/0d232cc4-158d-44f2-ba67-44c304ce358f" />

Allows user to set where and how bnones should be delinaated, with either numbers or letters, or both.
Works in edit and pose mode!

<img width="500" height="550" alt="image" src="https://github.com/user-attachments/assets/910bdcef-37fb-4850-a8dc-4b55bd55b3b5" />
<img width="500" height="550" alt="image" src="https://github.com/user-attachments/assets/91c284a7-fe52-482e-873a-9f78d2ce1fa4" />

They should name in the order you select them
(blender stores selected bones in an unordered set and may not name in the right order working on a fix for that)

## How to use

The default keybind is alt+f2

<img width="752" height="114" alt="image" src="https://github.com/user-attachments/assets/9b604f0e-b078-46de-8b2e-302f26833145" />

### Nameing
When typing the name for the bones set either a "#" or "@" symbol to set where you want the numbers or letters to go in the name. The number of symbols determins the padding so:
@@@ = 00A
###### = 000001

### Root Options
For Numbers and letters there are difrent options for how to name the root which can be selected by the radio buttons. 
<img width="376" height="34" alt="image" src="https://github.com/user-attachments/assets/38654bd0-ced5-4efa-b089-da7962d715de" />
<img width="376" height="34" alt="image" src="https://github.com/user-attachments/assets/3fcdefd8-9669-4057-bf0a-c024e697cb06" />

Each allows either starting blank or starting with numbers or letters.
Numbers gives the option to start at 0 or 1 

When starting blank you can check 

<img width="376" height="34" alt="image" src="https://github.com/user-attachments/assets/fbfb7768-03c9-45a4-87be-8df4be6b71e4" />

to remove the character before the symbols. This is if you have a seperator like "_" or "." but don't want your chain to start with numbers or letters with out this you may end up with hanging seperator or dopuble seperator.

Jim.##.L -> Jim..L
or if on
Jim.##.L -> Jim.L

This only applies to the root bone of the chain.

Finally you can set the padding character for the letter naming scheme

## Multi chain!

<img width="396" height="314" alt="image" src="https://github.com/user-attachments/assets/62f50681-8ae3-4e72-9e35-9380cd2e151a" />

This addon allows for naming multiple chains together, useful for fingers or hair chains. All you have to do is select multiple chains and the addon will change to multichain mode.
The only difrent option is setting what marks a sperate chain, the other will be used to mark seperate bones per chain.

<img width="378" height="26" alt="image" src="https://github.com/user-attachments/assets/dd740d5a-b37f-4d81-bb10-6e68b2ad706a" />

