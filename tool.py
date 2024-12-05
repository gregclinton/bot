import tools.chroma
import tools.shell
import tools.plot

bench = {
    "chromadb": tools.chroma.invoke,
    "shell": tools.shell.invoke,
    "plot": tools.plot.invoke,
}
