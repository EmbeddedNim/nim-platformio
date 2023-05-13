from os import makedirs, system, path
from shutil import copyfile
from pathlib import Path

Import("env")

prj_dir = Path(env.subst("$PROJECT_DIR"))
prj_src_dir = Path(env.subst("$PROJECT_SRC_DIR"))

files_to_copy = (
    ("nim.cfg", prj_dir),
    ("panicoverride.nim", prj_src_dir),
)

# Copy a file if it is missing, making the directory if necessary
for fn, dest in files_to_copy:
    if not path.exists(dest):
        makedirs(dest)
    if not path.exists(dest / fn):
        copyfile(Path().parent / fn, dest / fn)

libdeps = env.subst("$PROJECT_LIBDEPS_DIR/$PIOENV")

cpu = "avr"
if "espressif" in env.subst("$PIOPLATFORM"):
    cpu = "esp"

flags = f"--path:{libdeps} " f"--cpu:{cpu} "

result = system(f"nim cpp {flags} {src/'main'}")
if result != 0:
    exit(result)
