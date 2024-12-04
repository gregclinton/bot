import chroma
import shell
import plot

bench = {
    "Database": chroma.invoke,
    "Shell": shell.invoke,
    "Plot": plot.invoke,
}
