import invoke
import livereload
import shutil

server = livereload.Server()


@invoke.task
def clean():
    shutil.rmtree('./build')


@invoke.task(pre=[clean])
def build():
    invoke.run('sphinx-build ./source ./build', pty=True)


@invoke.task(pre=[build])
def serve():
    server.watch('../reqon/', build)
    server.watch('./source/', build)
    server.serve(
        root='./build',
        host='localhost',
        liveport=35729,
        port=8080
    )
