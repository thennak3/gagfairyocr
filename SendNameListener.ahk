#Requires AutoHotkey v2.0+
#SingleInstance Force

SetKeyDelay 30
SendMode "Event"
SetTitleMatchMode 2
CoordMode "Mouse", "Screen"

commandFile := A_ScriptDir "\next_fruit.txt"

SendName(name) {
    MouseClick "L", 2227, 1183
    Sleep 100
    MouseClick "L", 2163, 1192
    Sleep 100
    Send "{Blind}" name
    Sleep 100
    MouseClick "L", 1569, 1288
}

SetTimer checkFile, 100

checkFile(*) {
    global commandFile
    if !FileExist(commandFile)
        return

    try {
        content := FileRead(commandFile)
    } catch {
        return
    }

    fruit := Trim(content)
    if fruit {
        SendName(fruit)
        try {
            FileDelete(commandFile)
        } catch {
            ;
        }
    }
}
