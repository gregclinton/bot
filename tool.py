import chroma
import shell
import switchboard
import answers
import erase

bench = {
    "Database": chroma.invoke,
    "Shell": shell.invoke,
    "Switchboard": switchboard.invoke,
    "Answers": answers.invoke,
    "Erase": erase.invoke,
}
