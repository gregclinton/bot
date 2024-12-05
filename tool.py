import tools.chroma
import tools.shell
import tools.plot

bench = {
    "Database": tools.chroma.invoke,
    "Shell": tools.shell.invoke,
    "Plot": tools.plot.invoke,
}
