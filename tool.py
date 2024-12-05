import tools.chroma
import tools.shell
import tools.plot
import tools.install

installed = {"brevity", "install"}

bench = {
    "install": tools.install.invoke,
    "chromadb": tools.chroma.invoke,
    "shell": tools.shell.invoke,
    "plot": tools.plot.invoke,
}
