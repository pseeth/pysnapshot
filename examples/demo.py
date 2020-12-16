import snapshot
import hello_world

# First let's take a snapshot of the 
# hello_world package.

path = snapshot.capture(hello_world, '/tmp/hello_world_snap/', overwrite=True)
hello_world_snap = snapshot.load(path)
print(hello_world_snap.__file__)

# The snapshot is loaded from the specified directory. The code was all copied to
# and is under the snapshot:

print("From original package code", hello_world.func1())
print("From snapshot", hello_world_snap.hello_world.func1())

# You can import from the snapshot as if it were a regular package

from hello_world_snap import hello_world
print("From snapshot, overwriting the original package code", hello_world.func1())
