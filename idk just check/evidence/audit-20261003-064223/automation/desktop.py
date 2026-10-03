#!/usr/bin/env python3
"""Visible GNOME/X11 terminal control and unedited desktop captures for this lab.

Commands are pasted into actual terminals. No passwords are stored or supplied.
The output-only `script` logs retain terminal commands/results, not hidden input.
"""
import argparse
import ast
import ctypes
import ctypes.util
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import time
import uuid

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Wnck", "3.0")
from gi.repository import Gdk, Gtk, Wnck
from PIL import Image

BASE = Path("/home/seed/issd-member5")
HERE = BASE / "automation"
STATE = HERE / "desktop-state.json"
TITLES = {"A": "A — Attacker", "B": "B — Victim and results"}


def pump(seconds=0.25):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        time.sleep(0.01)


def windows():
    screen = Wnck.Screen.get_default()
    screen.force_update()
    return screen, screen.get_windows()


def load():
    return json.loads(STATE.read_text())


def save(state):
    STATE.write_text(json.dumps(state, indent=2) + "\n")


def record(action, **details):
    with (HERE / "desktop-actions.jsonl").open("a") as stream:
        stream.write(json.dumps({"time": dt.datetime.now().astimezone().isoformat(),
                                 "action": action, **details}) + "\n")


def window_for(role):
    state = load()
    _, items = windows()
    xid = state["windows"][role]
    return next(w for w in items if w.get_xid() == xid)


def activate(role):
    w = window_for(role)
    timestamp = int(time.monotonic() * 1000) & 0xffffffff
    if w.is_minimized():
        w.unminimize(timestamp)
    w.activate(timestamp)
    pump()
    screen, _ = windows()
    active = screen.get_active_window()
    if not active or active.get_xid() != w.get_xid():
        raise RuntimeError("Requested evidence terminal did not gain focus")
    return w


def keys(names, settle=0.25):
    x = ctypes.CDLL(ctypes.util.find_library("X11"))
    xt = ctypes.CDLL(ctypes.util.find_library("Xtst"))
    x.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x.XOpenDisplay.restype = ctypes.c_void_p
    x.XStringToKeysym.argtypes = [ctypes.c_char_p]
    x.XStringToKeysym.restype = ctypes.c_ulong
    x.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    x.XKeysymToKeycode.restype = ctypes.c_uint
    x.XSync.argtypes = [ctypes.c_void_p, ctypes.c_int]
    x.XCloseDisplay.argtypes = [ctypes.c_void_p]
    xt.XTestFakeKeyEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint,
                                    ctypes.c_int, ctypes.c_ulong]
    display = x.XOpenDisplay(None)
    if not display:
        raise RuntimeError("Cannot open X display")
    codes = [x.XKeysymToKeycode(display, x.XStringToKeysym(n.encode()))
             for n in names]
    if not all(codes):
        raise RuntimeError("Unknown X key")
    for code in codes:
        xt.XTestFakeKeyEvent(display, code, 1, 0)
    for code in reversed(codes):
        xt.XTestFakeKeyEvent(display, code, 0, 0)
    x.XSync(display, 0)
    x.XCloseDisplay(display)
    pump(settle)


def send(role, command, settle=0.25):
    if "\n" in command or "\r" in command:
        raise ValueError("Paste one command line at a time")
    activate(role)
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(command, -1)
    pump(0.1)
    keys(["Control_L", "Shift_L", "v"])
    pump(0.3)
    keys(["Return"], settle=settle)
    record("terminal-command", role=role, command=command)


def layout():
    state = load()
    screen, items = windows()
    width, height = screen.get_width(), screen.get_height()
    if width < 1600:
        subprocess.run(["xrandr", "--output", "Virtual1", "--mode", "1920x1200"],
                       check=True)
        pump(1)
        screen, items = windows()
        width, height = screen.get_width(), screen.get_height()
    evidence = set(state["windows"].values())
    for w in items:
        if w.get_xid() not in evidence and not w.is_minimized():
            w.minimize()
    left, top = 72, 28
    half = (width - left) // 2
    flags = (Wnck.WindowMoveResizeMask.X | Wnck.WindowMoveResizeMask.Y |
             Wnck.WindowMoveResizeMask.WIDTH | Wnck.WindowMoveResizeMask.HEIGHT)
    for index, role in enumerate(("A", "B")):
        w = window_for(role)
        w.unmaximize()
        w.unminimize(int(time.monotonic() * 1000) & 0xffffffff)
        w.set_geometry(Wnck.WindowGravity.STATIC, flags,
                       left + half * index, top, half, height - top)
        subprocess.run(["xprop", "-id", str(w.get_xid()), "-f", "_NET_WM_NAME",
                        "8u", "-set", "_NET_WM_NAME", TITLES[role]], check=True)
    pump(0.6)
    activate("B")
    record("layout", resolution=[width, height], windows=state["windows"],
           control_minimized=True)


def setup():
    if STATE.exists():
        raise RuntimeError("Existing desktop-state.json: refusing to replace session")
    if os.getuid() != 1000 or os.geteuid() != 1000:
        raise RuntimeError("Run desktop automation as seed")
    session = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    evidence = BASE / "evidence" / ("automation-" + session)
    evidence.mkdir(parents=True, exist_ok=False)
    (evidence / "source-before").mkdir()
    import shutil
    for path in (BASE / "lab-files").iterdir():
        if path.suffix in (".sh", ".c") or path.name == "input.txt":
            shutil.copy2(path, evidence / "source-before" / path.name)
    profile_list = ast.literal_eval(subprocess.check_output(
        ["gsettings", "get", "org.gnome.Terminal.ProfilesList", "list"], text=True))
    _, items = windows()
    original_windows = [{"xid": w.get_xid(), "title": w.get_name(),
                         "geometry": list(w.get_geometry()),
                         "minimized": w.is_minimized()} for w in items]
    profile = str(uuid.uuid4())
    settings = "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:" + profile + "/"
    values = {"visible-name": "Member5 evidence " + session,
              "use-system-font": "false", "font": "Monospace 12",
              "use-theme-colors": "false", "foreground-color": "#eeeeec",
              "background-color": "#17191c", "scrollback-unlimited": "true",
              "scroll-on-output": "true", "audible-bell": "false"}
    for key, value in values.items():
        subprocess.run(["gsettings", "set", settings, key, value], check=True)
    subprocess.run(["gsettings", "set", "org.gnome.Terminal.ProfilesList", "list",
                    repr(profile_list + [profile])], check=True)
    state = {"session": session, "evidence": str(evidence), "profile": profile,
             "original_profiles": profile_list, "original_windows": original_windows,
             "original_xrandr": subprocess.check_output(["xrandr", "--current"], text=True),
             "windows": {}}
    save(state)
    subprocess.run(["xrandr", "--output", "Virtual1", "--mode", "1920x1200"], check=True)
    pump(1)
    for role in ("A", "B"):
        command = shlex.join(["env", "LAB_ROLE=" + role, "LAB_TITLE=" + TITLES[role],
                              "LAB_SESSION=" + session, "LAB_EVIDENCE=" + str(evidence),
                              "bash", "--noprofile", "--rcfile",
                              str(HERE / "terminal-rc.bash"), "-i"])
        subprocess.run(["gnome-terminal", "--window", "--profile=" + profile,
                        "--hide-menubar", "--title=" + TITLES[role],
                        "--working-directory=" + str(BASE / "lab-files"),
                        "--", "script", "-qef", "--timing=" + str(evidence / ("terminal-" + role + ".timing")),
                        "--command", command, str(evidence / ("terminal-" + role + ".typescript"))], check=True)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            pump(0.2)
            _, items = windows()
            matches = [w for w in items if w.get_name() == TITLES[role]]
            if matches:
                state["windows"][role] = matches[-1].get_xid()
                break
        else:
            raise RuntimeError("Evidence terminal was not found")
        save(state)
    layout()
    record("setup", **state)
    print(json.dumps(state, indent=2))


def capture(stem):
    if not stem or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in stem):
        raise ValueError("Use an alphanumeric/dash/underscore capture stem")
    layout()
    pump(0.5)
    filename = stem + "-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".png"
    path = BASE / "evidence" / filename
    subprocess.run(["gnome-screenshot", "--file=" + str(path)], check=True)
    with Image.open(path) as image:
        size = list(image.size)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    _, items = windows()
    record("original-screenshot", file=str(path), sha256=digest, size=size,
           windows=[{"xid": w.get_xid(), "title": w.get_name(),
                     "geometry": list(w.get_geometry()), "minimized": w.is_minimized()}
                    for w in items])
    print(path)
    print("Original desktop PNG:", size, "sha256=" + digest)


def burst_send(role, command, label):
    """Capture actual root-window pixels quickly enough for a sub-second race.

    Every frame is an original screenshot. PID/start-time checks before and
    after the capture identify frames with both experiment processes still live.
    """
    import lab_runner
    if not label or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in label):
        raise ValueError("Invalid trial label")
    layout()
    send(role, command, settle=0.03)
    good = 0
    def process_states():
        states = {}
        for kind in ("attacker", "monitor"):
            path = BASE / "lab-files/logs" / (label + "-" + kind + "-state.json")
            if path.exists():
                state = json.loads(path.read_text())
                state["live_at_check"] = lab_runner.alive(state)
                states[kind] = state
        return states
    for index in range(12):
        before = process_states()
        root = Gdk.get_default_root_window()
        size = [root.get_width(), root.get_height()]
        path = BASE / "evidence" / ("S08b-task2b-live-frame-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".png")
        pixels = Gdk.pixbuf_get_from_window(root, 0, 0, *size)
        if pixels is None:
            raise RuntimeError("GDK could not read the actual desktop pixels")
        pixels.savev(str(path), "png", ["compression"], ["1"])
        after = process_states()
        both = all(states.get(kind, {}).get("live_at_check", False)
                   for states in (before, after) for kind in ("attacker", "monitor"))
        record("original-screenshot", method="GDK whole-desktop pixels", file=str(path),
               sha256=hashlib.sha256(path.read_bytes()).hexdigest(), size=size,
               trial=label, processes_before=before, processes_after=after,
               both_experiment_processes_live=both)
        print(str(path) + " | both processes live=" + str(both), flush=True)
        if both:
            good += 1
        if good >= 3 or (BASE / "lab-files/logs" / (label + "-result.json")).exists():
            break
        pump(0.05)
    print("Frames with both processes live before and after capture:", good)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("setup")
    sub.add_parser("layout")
    sub.add_parser("windows")
    p = sub.add_parser("send")
    p.add_argument("role", choices=("A", "B"))
    p.add_argument("command")
    p = sub.add_parser("key")
    p.add_argument("role", choices=("A", "B"))
    p.add_argument("keys", nargs="+")
    p = sub.add_parser("capture")
    p.add_argument("stem")
    p = sub.add_parser("burst-send")
    p.add_argument("role", choices=("A", "B"))
    p.add_argument("command")
    p.add_argument("label")
    args = parser.parse_args()
    if args.action == "setup":
        setup()
    elif args.action == "layout":
        layout()
    elif args.action == "send":
        send(args.role, args.command)
    elif args.action == "key":
        activate(args.role)
        keys(args.keys)
        record("terminal-key", role=args.role, keys=args.keys)
    elif args.action == "capture":
        capture(args.stem)
    elif args.action == "burst-send":
        burst_send(args.role, args.command, args.label)
    else:
        _, items = windows()
        print(json.dumps([{"xid": w.get_xid(), "title": w.get_name(),
                           "geometry": list(w.get_geometry()), "minimized": w.is_minimized()}
                          for w in items], indent=2))


if __name__ == "__main__":
    main()
