import json
import sys
import os

if hasattr(sys, '_MEIPASS'):
    etc_dir = os.path.join(sys._MEIPASS, 'etc')
    os.environ.setdefault('PANDA_PRC_DIR', etc_dir)
    os.environ.setdefault('PANDA_PRC_PATH', etc_dir)
    from ursina import application
    from pathlib import Path
    application.fonts_folder = Path(sys._MEIPASS)
    application.internal_fonts_folder = Path(sys._MEIPASS)
    application.asset_folder = Path(sys._MEIPASS)
    os.chdir(sys._MEIPASS)
from ursina import *
from ursina.models.procedural.cone import Cone
window.vsync = False
window.editor_ui_enabled = False
app = Ursina(title="125Dash", show_ursina_splash=True, development_mode=False, borderless=True, fullscreen=True)
#player
cube = Entity(model="cube", position=(0, 1, 10), collider="box", texture="icon.png")
ground = Entity(model="cube", scale=(1, 1, 100), color=color.black, collider='box', y=0)
selection = Entity(model="cube", scale=(1.1, 1.1, 1.1), position=(0, 1, 10), color=color.green, visible=False)
blocks = []
camera.position = (-30, 5, 30)
camera.rotation = (0, 135, 0)
last_mouse_rig = False
last_mouse_left = False
last_held_keys = held_keys
unlockedMenu = False
menu = "intro"
velY = 0.11
photos = os.listdir("textures/gallery")
currPhoto = 0
def endIntro():
    global intro
    destroy(intro)
    goMenu()
def goIntro():
    global menu, intro
    menu = "intro"
    intro = Entity(model="quad", parent=camera.ui, texture="launch.png", scale=(1.7, 1))
    invoke(endIntro, delay=5)
def goGallery():
    global menu, name, gallery, image, nextImg, prevImg, currPhoto, play
    if menu == "main":
        destroy(name)
        destroy(gallery)
        del name, gallery
        if unlockedMenu:
            destroy(play)
    menu = "gallery"
    currPhoto = 0
    image = Entity(model="quad", parent=camera.ui, texture="gallery/" + photos[currPhoto])
    nextImg = Entity(model="quad", parent=camera.ui, texture="next.png", scale=0.2, position=(0.75, 0), collider="box")
    prevImg = Entity(model="quad", parent=camera.ui, texture="prev.png", scale=0.2, position=(-0.75, 0), collider="box")
def levelComplete():
    global congrats, menu
    menu = "complete"
    levelAudio.stop()
    Audio("end.ogg", auto_destroy=True, autoplay=True, volume=3)
    congrats = Entity(model="quad", parent=camera.ui, texture="levelComplete.png", collider="box")
def goMenu():
    global gallery, menu, name, menuBG, play, congrats
    if not globals().get("menuBG"): menuBG = Audio("menu.mp3", loop=True, autoplay=True)
    if globals().get("congrats"): destroy(congrats)
    if not menu:
        for block__ in blocks: destroy(block__)
        if globals().get("end"): destroy(end)
    elif menu == "gallery":
        destroy(image)
        destroy(nextImg)
        destroy(prevImg)
    if unlockedMenu:
        play = Entity(model="quad", parent=camera.ui, texture="play.png", scale=0.3, collider="box")
    menu = "main"
    name = Entity(model="quad", parent=camera.ui, texture="name.png", position=(0, 0.3), scale=(1.7, 0.2))
    gallery = Entity(model="quad", parent=camera.ui, texture="galery.png", position=(0, -0.3), scale=(0.2, 0.2), collider="box")
    camera.position = (0, 0, 0)
    camera.rotation = (0, 90, 0)
def loadLevel(_name):
    global ground, end, menu, level, currLevel, levelAudio, name, gallery, play, congrats
    if globals().get("menuBG"): menuBG.stop()
    if globals().get("levelAudio"): levelAudio.stop()
    if globals().get("congrats"):
        destroy(congrats)
    if menu == "main":
        destroy(name)
        destroy(gallery)
        del name, gallery
        if unlockedMenu:
            destroy(play)
            del play
    for block__ in blocks: destroy(block__)
    if globals().get("end"): destroy(end)
    blocks.clear()
    currLevel = _name
    level = json.load(open("level\\" + _name + ".json", "r", encoding="utf-8"))
    levelAudio = Audio(level["song"], autoplay=True)
    camera.position = (-30, 5, 30)
    camera.rotation = (0, 135, 0)
    cube.position = (0, 1, 10)
    ground.position = (0, 0, 0)
    for mapentity in level["entities"]:
        if mapentity[0] == "cube":
            e = Entity(position=(mapentity[1], mapentity[2], mapentity[3]), model="cube", color=color.rgba(.5, .5, .5), collider="box")
            e.model_name = "cube"
            blocks.append(e)
        elif mapentity[0] == "spike":
            e = Entity(position=(mapentity[1], mapentity[2], mapentity[3]), model=Cone(resolution=10, radius=.5, height=1), color=color.rgba(.5, .5, .5), collider="mesh")
            e.model_name = "spike"
            blocks.append(e)
    end = Entity(position=(0, 5, level["end"]), scale=(1, 10, 1), model="cube", color=color.rgba(0, 1, 1), collider="box")
    menu = False
def loadNextLevel():
    global levels
    if len(levels) > 0: loadLevel(levels.pop(0))
    else:
        goMenu()
        levels = ["stereo125", "125out", "level125", "hello125"]
def unfreezeLevel():
    global freezed, levelAudio
    levelAudio.play()
    freezed = False
    camera.position = (-30, 5, 30)
    cube.position = (0, 1, 10)
    ground.position = (0, 0, 0)
creative = False
pause = False
intro = False
freezed = False
baseSpeed = 4
levels = ["stereo125", "125out", "level125", "hello125"]
goIntro()
def update():
    global last_mouse_left, velY, last_held_keys, creative, pause, last_mouse_rig, last_mouse_mid, currPhoto, unlockedMenu, freezed
    if not freezed:
        if not menu:
            if not creative and not pause:
                cube.position -= (0, velY * time.dt, baseSpeed * time.dt)
                ground.position -= (0, 0, baseSpeed * time.dt)
                velY += 17 * time.dt
                camera.position -= (0, 0, baseSpeed * time.dt)
            elif creative:
                selection.position = (round(cube.position[0]), round(cube.position[1]), round(cube.position[2]))
                shift = (20 * int(held_keys["shift"]) + 1)
                subshift = (5 * int(held_keys["shift"]) + 1)
                if held_keys["d"]:
                    cube.position -= (0, 0, baseSpeed * shift * time.dt)
                    ground.position -= (0, 0, baseSpeed * shift * time.dt)
                    camera.position -= (0, 0, baseSpeed * shift * time.dt)
                if held_keys["a"]:
                    cube.position += (0, 0, baseSpeed * shift * time.dt)
                    ground.position += (0, 0, baseSpeed * shift * time.dt)
                    camera.position += (0, 0, baseSpeed * shift * time.dt)
                if held_keys["w"]: cube.position += (0, baseSpeed * subshift * time.dt, 0)
                if held_keys["s"]: cube.position -= (0, baseSpeed * subshift * time.dt, 0)
                if held_keys["up arrow"] and not last_held_keys["up arrow"]: cube.position += (1, 0, 0)
                if held_keys["down arrow"] and not last_held_keys["down arrow"]: cube.position -= (1, 0, 0)
                if not last_held_keys["e"] and held_keys["e"]:
                    e = Entity(position=(round(cube.position[0]), round(cube.position[1]), round(cube.position[2])), model="cube", color=color.rgba(.5, .5, .5), collider="box")
                    e.model_name = "cube"
                    blocks.append(e)
                if not last_held_keys["r"] and held_keys["r"]:
                    e = Entity(position=(round(cube.position[0]), round(cube.position[1]), round(cube.position[2])), model=Cone(resolution=10, radius=.5, height=1), color=color.rgba(.5, .5, .5), collider="mesh")
                    e.model_name = "spike"
                    blocks.append(e)
                if not last_held_keys["i"] and held_keys["i"]:
                    level["end"] -= 1
                    end.position -= (0, 0, 1)
                if not last_held_keys["u"] and held_keys["u"]:
                    level["end"] += 1
                    end.position += (0, 0, 1)
                if not last_held_keys["q"] and held_keys["q"]:
                    for block in blocks:
                        if block.position == (round(cube.position[0]), round(cube.position[1]), round(cube.position[2])):
                            destroy(block)
                            blocks.remove(block)
                            break
                if not last_held_keys["p"] and held_keys["p"]:
                    out = {"entities":[], "end": level["end"]}
                    for block in blocks: out["entities"].append(["cube" if block.model_name == "cube" else "spike", block.position[0], block.position[1], block.position[2]])
                    json.dump(out, open("level\\" + currLevel + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
            if cube.position[2] < level["end"] + 1:
                levelComplete()
                return
            if not last_held_keys["c"] and held_keys["c"]:
                creative = not creative
                selection.visible = creative
            if not last_held_keys["escape"] and held_keys["escape"]: pause = not pause
            if not creative and not pause:
                hit = cube.intersects()
                if hit.hit:
                    normal = hit.world_normal
                    if normal.y > 0.5:
                        velY = 0
                        cube.position[1] = math.ceil(cube.position[1])
                        if mouse.left or held_keys["up arrow"] or held_keys["space"] or held_keys["w"]: velY = -8.5
                    elif normal.z > 0.5:
                        freezed = True
                        levelAudio.stop()
                        Audio("explode_125.ogg", autoplay=True, auto_destroy=True, volume=3)
                        invoke(unfreezeLevel, delay=1.5)
        elif menu == "main":
            if mouse.hovered_entity == gallery and not last_mouse_left and mouse.left: goGallery()
            elif unlockedMenu and mouse.hovered_entity == play and not last_mouse_left and mouse.left: loadNextLevel()
        elif menu == "gallery":
            if mouse.hovered_entity == nextImg and not last_mouse_left and mouse.left:
                currPhoto += 1
                if currPhoto == len(photos):
                    unlockedMenu = True
                    goMenu()
                else: image.texture = "gallery/" + photos[currPhoto]
            elif mouse.hovered_entity == prevImg and not last_mouse_left and mouse.left:
                currPhoto -= 1
                image.texture = "gallery/" + photos[currPhoto]
        elif menu == "complete":
            if mouse.hovered_entity == congrats and not last_mouse_left and mouse.left: loadNextLevel()
    last_mouse_left = copy(mouse.left)
    last_held_keys = copy(held_keys)
    last_mouse_rig = copy(mouse.right)
app.run()