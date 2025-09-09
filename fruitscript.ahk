#Requires AutoHotkey v2.0+

SetKeyDelay 30
SendMode "Event"
SetTitleMatchMode 2
CoordMode "Mouse", "Screen"

names := [
    "Mango",         ; Numpad1
    "Lightshoot",    ; Numpad2
    "Ember%SLily",   ; Numpad3
    "Sugar%SApple",  ; Numpad4
    "Strawberry",    ; Numpad5
    "Blueberry",     ; Numpad6
    "Orange%STulip", ; Numpad7
    "Tomato",        ; Numpad8
    "Corn",          ; Numpad9
    "Daffodil",      ; Numpad0
    "Watermelon",    ; NumpadDiv (/)
    "Pumpkin",       ; NumpadMult (*)
    "Apple",         ; NumpadSub  (-)
    "Bamboo",        ; NumpadAdd  (+)
    "Coconut",       ; NumpadEnter
    "Cactus",        ; NumpadDot (.)
    "Dragon%sFruit", ; Insert
    "Pepper",        ; Home
    "Grape",         ; PgUp
    "Sunbulb",       ; Delete
    "Cacao",         ; End
    "Burning%SBud"   ; PgDn
]

; Map keys to indexes in names[]
keyMap := Map(
    "Numpad1", 1,
    "Numpad2", 2,
    "Numpad3", 3,
    "Numpad4", 4,
    "Numpad5", 5,
    "Numpad6", 6,
    "Numpad7", 7,
    "Numpad8", 8,
    "Numpad9", 9,
    "Numpad0", 10,
    "NumpadDiv", 11,
    "NumpadMult", 12,
    "NumpadSub", 13,
    "NumpadAdd", 14,
    "NumpadEnter", 15,
    "NumpadDot", 16,
    "Insert", 17,
    "Home", 18,
    "PgUp", 19,
    "Delete", 20,
    "End", 21,
    "PgDn", 22
)

; Register hotkeys — use a closure factory so idx is captured correctly
for key, idx in keyMap {
    Hotkey key, MakeHandler(idx)
}

MakeHandler(idx) {
    return (*) => (
        names[idx] != "" ? SendName(names[idx]) : ""
    )
}

SendName(name) {
    MouseClick "L", 2227, 1183
    Sleep 100
    MouseClick "L", 2163, 1192
    Sleep 100
    Send "{Blind}" name
    Sleep 100
    MouseClick "L", 1569, 1288
}
