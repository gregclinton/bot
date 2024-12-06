import tools.install
import tools.chroma
import tools.shell
import tools.plot
import tools.chatbot

bench = {
    "install": tools.install.invoke,
    "chromadb": tools.chroma.invoke,
    "shell": tools.shell.invoke,
    "plot": tools.plot.invoke,
    "chatbot": tools.chatbot.invoke,
}
