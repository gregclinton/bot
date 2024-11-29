import chroma
import shell
import switchboard

bench = {
    "Database": chroma.invoke,
    "Shell": shell.invoke,
    "Switchboard": switchboard.invoke,
}
